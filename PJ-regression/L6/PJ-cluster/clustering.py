"""
聚类算法课堂实践代码（教学版）
--------------------------------
学生主要在 main() 中填写：
1. data_path：聚类数据文件路径
2. case_name：案例名称（可不改）
3. PARAM_GRIDS：KMeans 的参数网格（可尝试调整）

GeneralCluster 已封装：
load_case -> run -> collect_data -> plot

默认约定：
- 数据中没有标签列；如果数据中存在 class / target / label 等列，程序会自动剔除。
- 支持 CSV / XLSX / XLS。
- 数值型特征会自动缺失值填补与标准化。
- 分类型特征会自动缺失值填补与 One-Hot 编码。
- 本实践课使用 K-means 聚类方法。

输出目录：
outputs / case_name / model_name / best_parameter_folder
例如：
outputs/customer_segmentation/KMeans/init=k-means++_max_iter=300_n_clusters=4_n_init=10/
"""

from __future__ import annotations

import itertools
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score, silhouette_score
from sklearn.model_selection import ParameterGrid
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


@dataclass
class ClusterConfig:
    case_name: str
    data_path: str
    model_name: str
    output_dir: str = "outputs"
    random_state: int = 42
    scoring: str = "silhouette"
    max_search_samples: int = 3000


def make_onehot_encoder() -> OneHotEncoder:
    """兼容不同 sklearn 版本。"""
    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


class GeneralCluster:
    """通用聚类器：当前教学版支持 KMeans。"""

    SUPPORTED_MODELS = {"KMeans"}
    MAX_PROFILE_FEATURES = 20

    def __init__(self) -> None:
        self.config: Optional[ClusterConfig] = None
        self.df: Optional[pd.DataFrame] = None
        self.X_raw: Optional[pd.DataFrame] = None
        self.feature_cols: List[str] = []
        self.numeric_cols: List[str] = []
        self.categorical_cols: List[str] = []
        self.auto_dropped_cols: List[str] = []
        self.user_dropped_cols: List[str] = []

        self.preprocessor: Optional[ColumnTransformer] = None
        self.best_model: Optional[KMeans] = None
        self.best_pipeline: Optional[Pipeline] = None
        self.best_params_: Optional[Dict[str, Any]] = None
        self.best_score_: Optional[float] = None
        self.grid_results_: Optional[pd.DataFrame] = None

        self.X_processed_: Optional[np.ndarray] = None
        self.cluster_labels_: Optional[np.ndarray] = None
        self.metrics_: Optional[Dict[str, Any]] = None
        self.cluster_sizes_: Optional[pd.DataFrame] = None
        self.cluster_summary_numeric_: Optional[pd.DataFrame] = None
        self.cluster_assignments_: Optional[pd.DataFrame] = None
        self.output_path: Optional[Path] = None

    # ------------------------- basic utilities -------------------------
    def _assert_case_ready(self) -> None:
        if self.config is None or self.df is None or self.X_raw is None:
            raise RuntimeError("尚未加载案例，请先调用 load_case()。")

    def _assert_has_run(self) -> None:
        if self.best_model is None or self.cluster_labels_ is None or self.metrics_ is None:
            raise RuntimeError("模型尚未训练，请先调用 run()。")

    @staticmethod
    def _assert_user_filled(text: str, field_name: str) -> None:
        tokens = {"请填写", "your_", "TODO", "todo", "路径", "path"}
        if not text or any(token in str(text) for token in tokens):
            raise ValueError(f"{field_name} 尚未按要求填写。")

    @staticmethod
    def _sanitize_filename(text: str) -> str:
        text = str(text).replace("+", "plus")
        text = re.sub(r"[^0-9A-Za-z_\-\u4e00-\u9fff=.]+", "_", text)
        text = re.sub(r"_+", "_", text).strip("_")
        return text or "default"

    @staticmethod
    def _as_list(value: Any) -> List[Any]:
        if isinstance(value, (list, tuple, np.ndarray, pd.Series)):
            return list(value)
        return [value]

    @staticmethod
    def _json_default(obj: Any) -> Any:
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        return str(obj)

    def _params_to_folder_name(self, params: Dict[str, Any]) -> str:
        if not params:
            return "default_params"
        parts = []
        for key in sorted(params.keys()):
            val = params[key]
            safe_key = self._sanitize_filename(key)
            safe_val = self._sanitize_filename(str(val))
            parts.append(f"{safe_key}={safe_val}")
        return "_".join(parts)[:180]

    def _build_output_path(self) -> Path:
        param_folder = self._params_to_folder_name(self.best_params_ or {})
        out = Path(self.config.output_dir) / self.config.case_name / self.config.model_name / param_folder
        out.mkdir(parents=True, exist_ok=True)
        self.output_path = out
        return out

    # ------------------------- data loading -------------------------
    @staticmethod
    def _read_data_file(data_file: Path) -> pd.DataFrame:
        suffix = data_file.suffix.lower()
        if suffix == ".csv":
            return pd.read_csv(data_file)
        if suffix in {".xlsx", ".xls"}:
            return pd.read_excel(data_file)
        raise ValueError("仅支持 CSV / XLSX / XLS 文件。")

    def _auto_detect_drop_cols(self, df: pd.DataFrame) -> List[str]:
        """
        自动剔除常见标签列、明显 ID 列和常数列。
        """
        drop_cols: List[str] = []
        n_rows = len(df)
        label_like_names = {"class", "target", "label", "labels", "cluster", "category"}
        id_like_names = {"id", "customerid", "customer_id", "invoiceid", "invoice_id", "invoiceno", "invoice_no"}

        for col in df.columns:
            col_str = str(col).strip()
            col_key = col_str.lower().replace(" ", "_").replace("-", "_")
            nunique = df[col].nunique(dropna=True)
            unique_ratio = nunique / max(n_rows, 1)

            if col_key in label_like_names:
                drop_cols.append(col)
                continue

            if col_key in id_like_names and unique_ratio > 0.80:
                drop_cols.append(col)
                continue

            # 高基数字符串列通常是编号或文本描述，直接 One-Hot 会造成维度爆炸。
            if not pd.api.types.is_numeric_dtype(df[col]) and unique_ratio > 0.80:
                drop_cols.append(col)
                continue

            # 常数列没有聚类信息。
            if nunique <= 1:
                drop_cols.append(col)
                continue

        # 保持顺序且去重。
        seen = set()
        ordered = []
        for c in drop_cols:
            if c not in seen:
                ordered.append(c)
                seen.add(c)
        return ordered

    def load_case(
        self,
        data_path: str,
        case_name: Optional[str] = None,
        model_name: str = "KMeans",
        output_dir: str = "outputs",
        random_state: int = 42,
        scoring: str = "silhouette",
        max_search_samples: int = 3000,
        feature_cols: Optional[Sequence[str]] = None,
        drop_cols: Optional[Sequence[str]] = None,
        auto_drop: bool = True,
    ) -> "GeneralCluster":
        """加载聚类案例。"""
        self._assert_user_filled(data_path, "data_path")
        self._assert_user_filled(model_name, "model_name")

        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(f"model_name 必须为 {sorted(self.SUPPORTED_MODELS)} 之一。")

        if scoring not in {"silhouette", "davies_bouldin", "calinski_harabasz", "inertia"}:
            raise ValueError("scoring 必须为 silhouette / davies_bouldin / calinski_harabasz / inertia 之一。")

        data_file = Path(data_path)
        if not data_file.exists():
            raise FileNotFoundError(f"未找到数据文件：{data_file}")

        if case_name is None or str(case_name).strip() == "":
            case_name = data_file.stem
        self._assert_user_filled(case_name, "case_name")

        df = self._read_data_file(data_file)
        df.columns = [str(c).strip() for c in df.columns]
        df = df.replace({"?": np.nan, "": np.nan})
        df = df.dropna(axis=1, how="all").copy()

        if df.shape[1] < 1:
            raise ValueError("数据至少需要包含 1 列可用特征。")

        user_drop = list(drop_cols or [])
        missing_drop = [c for c in user_drop if c not in df.columns]
        if missing_drop:
            raise ValueError(f"drop_cols 中存在数据里没有的列：{missing_drop}")

        auto_drop_cols = self._auto_detect_drop_cols(df) if auto_drop else []
        all_drop_cols = []
        for c in list(user_drop) + list(auto_drop_cols):
            if c in df.columns and c not in all_drop_cols:
                all_drop_cols.append(c)

        work_df = df.drop(columns=all_drop_cols, errors="ignore").copy()

        if feature_cols is not None:
            missing = [c for c in feature_cols if c not in work_df.columns]
            if missing:
                raise ValueError(f"feature_cols 中存在数据里没有或已被剔除的列：{missing}")
            work_df = work_df[list(feature_cols)].copy()

        # 再次删除常数列。
        nunique = work_df.nunique(dropna=True)
        constant_cols = nunique[nunique <= 1].index.tolist()
        if constant_cols:
            work_df = work_df.drop(columns=constant_cols)
            auto_drop_cols = list(dict.fromkeys(auto_drop_cols + constant_cols))

        work_df = work_df.dropna(axis=0, how="all").reset_index(drop=True)

        if work_df.shape[1] < 1:
            raise ValueError("剔除无效列后，已无可用特征列。")
        if len(work_df) < 3:
            raise ValueError("样本数过少，无法进行聚类。")

        numeric_cols = work_df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = [c for c in work_df.columns if c not in numeric_cols]

        self.config = ClusterConfig(
            case_name=str(case_name),
            data_path=str(data_file),
            model_name=model_name,
            output_dir=output_dir,
            random_state=random_state,
            scoring=scoring,
            max_search_samples=max_search_samples,
        )
        self.df = df.reset_index(drop=True)
        self.X_raw = work_df
        self.feature_cols = list(work_df.columns)
        self.numeric_cols = numeric_cols
        self.categorical_cols = categorical_cols
        self.auto_dropped_cols = [str(c) for c in auto_drop_cols if c not in user_drop]
        self.user_dropped_cols = [str(c) for c in user_drop]
        self.preprocessor = self._build_preprocessor()
        return self

    # ------------------------- preprocessing and model -------------------------
    def _build_preprocessor(self) -> ColumnTransformer:
        numeric_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )
        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", make_onehot_encoder()),
            ]
        )
        return ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, self.numeric_cols),
                ("cat", categorical_transformer, self.categorical_cols),
            ],
            remainder="drop",
            sparse_threshold=0.0,
        )

    def _build_model(self, params: Dict[str, Any]) -> KMeans:
        params = dict(params)
        params.setdefault("random_state", self.config.random_state)
        return KMeans(**params)

    def _make_search_matrix(self, X_processed: np.ndarray) -> np.ndarray:
        max_n = int(self.config.max_search_samples)
        if len(X_processed) <= max_n:
            return X_processed
        rng = np.random.default_rng(self.config.random_state)
        idx = rng.choice(len(X_processed), size=max_n, replace=False)
        return X_processed[idx]

    def _score_labels(self, X: np.ndarray, labels: np.ndarray, inertia: float) -> Dict[str, float]:
        unique_labels = np.unique(labels)
        result = {
            "n_clusters_found": float(len(unique_labels)),
            "inertia": float(inertia),
            "silhouette": np.nan,
            "davies_bouldin": np.nan,
            "calinski_harabasz": np.nan,
        }
        if len(unique_labels) < 2 or len(unique_labels) >= len(X):
            return result
        result["silhouette"] = float(silhouette_score(X, labels))
        result["davies_bouldin"] = float(davies_bouldin_score(X, labels))
        result["calinski_harabasz"] = float(calinski_harabasz_score(X, labels))
        return result

    def _is_better(self, candidate: float, best: Optional[float]) -> bool:
        if np.isnan(candidate):
            return False
        if best is None or np.isnan(best):
            return True
        if self.config.scoring in {"davies_bouldin", "inertia"}:
            return candidate < best
        return candidate > best

    def _default_param_grid(self) -> Dict[str, List[Any]]:
        return {
            "n_clusters": [2, 3, 4, 5, 6],
            "init": ["k-means++", "random"],
            "n_init": [10, 20],
            "max_iter": [300],
        }

    # ------------------------- public API -------------------------
    def run(self, param_grid: Optional[Dict[str, Any]] = None) -> "GeneralCluster":
        """执行参数网格搜索，并用最佳参数在完整数据上训练 KMeans。"""
        self._assert_case_ready()

        if param_grid is None:
            param_grid = self._default_param_grid()
        normalized_grid = {k: self._as_list(v) for k, v in param_grid.items()}

        self.preprocessor = self._build_preprocessor()
        X_processed = np.asarray(self.preprocessor.fit_transform(self.X_raw), dtype=float)
        X_search = self._make_search_matrix(X_processed)

        results: List[Dict[str, Any]] = []
        best_params: Optional[Dict[str, Any]] = None
        best_score: Optional[float] = None

        for params in ParameterGrid(normalized_grid):
            params = dict(params)
            n_clusters = int(params.get("n_clusters", 8))
            row: Dict[str, Any] = {f"param_{k}": v for k, v in params.items()}

            try:
                if n_clusters < 2 or n_clusters >= len(X_search):
                    raise ValueError("n_clusters 必须大于等于 2 且小于样本数。")
                model = self._build_model(params)
                labels = model.fit_predict(X_search)
                score_dict = self._score_labels(X_search, labels, model.inertia_)
                row.update(score_dict)
                row["score_for_selection"] = row.get(self.config.scoring, np.nan)
                row["status"] = "ok"

                candidate_score = float(row["score_for_selection"])
                if self._is_better(candidate_score, best_score):
                    best_score = candidate_score
                    best_params = params
            except Exception as exc:
                row.update(
                    {
                        "n_clusters_found": np.nan,
                        "inertia": np.nan,
                        "silhouette": np.nan,
                        "davies_bouldin": np.nan,
                        "calinski_harabasz": np.nan,
                        "score_for_selection": np.nan,
                        "status": f"failed: {exc}",
                    }
                )
            results.append(row)

        grid_df = pd.DataFrame(results)
        if best_params is None:
            raise RuntimeError("所有参数组合均训练失败，请检查 PARAM_GRIDS 或数据集。")

        self.best_params_ = dict(best_params)
        self.best_score_ = float(best_score)
        self.grid_results_ = grid_df

        self.best_model = self._build_model(self.best_params_)
        self.best_pipeline = Pipeline(
            steps=[
                ("preprocess", self.preprocessor),
                ("model", self.best_model),
            ]
        )
        self.best_pipeline.fit(self.X_raw)
        self.best_model = self.best_pipeline.named_steps["model"]
        self.X_processed_ = np.asarray(self.best_pipeline.named_steps["preprocess"].transform(self.X_raw), dtype=float)
        self.cluster_labels_ = np.asarray(self.best_model.labels_, dtype=int)

        final_scores = self._score_labels(self.X_processed_, self.cluster_labels_, self.best_model.inertia_)
        self.metrics_ = {
            "case_name": self.config.case_name,
            "model_name": self.config.model_name,
            "scoring": self.config.scoring,
            "best_score": float(self.best_score_),
            "best_params": self.best_params_,
            "n_samples": int(len(self.X_raw)),
            "n_features_raw": int(len(self.feature_cols)),
            "n_features_processed": int(self.X_processed_.shape[1]),
            "numeric_cols": self.numeric_cols,
            "categorical_cols": self.categorical_cols,
            "auto_dropped_cols": self.auto_dropped_cols,
            "user_dropped_cols": self.user_dropped_cols,
            **final_scores,
        }

        self._build_result_tables()
        out = self._build_output_path()
        self._save_artifacts(out, normalized_grid)
        return self

    def _build_result_tables(self) -> None:
        assignments = self.X_raw.reset_index(drop=True).copy()
        assignments["cluster"] = self.cluster_labels_
        self.cluster_assignments_ = assignments

        sizes = (
            pd.Series(self.cluster_labels_, name="cluster")
            .value_counts()
            .sort_index()
            .rename_axis("cluster")
            .reset_index(name="count")
        )
        sizes["percentage"] = sizes["count"] / sizes["count"].sum()
        self.cluster_sizes_ = sizes

        if self.numeric_cols:
            summary = assignments.groupby("cluster")[self.numeric_cols].mean().round(4)
            summary.insert(0, "count", assignments.groupby("cluster").size())
            self.cluster_summary_numeric_ = summary.reset_index()
        else:
            self.cluster_summary_numeric_ = pd.DataFrame({"cluster": sorted(np.unique(self.cluster_labels_))})

    def collect_data(self, max_profile_cols: int = 10) -> pd.DataFrame:
        """在控制台输出提交所需的核心数据，并返回完整聚类结果表。"""
        self._assert_case_ready()
        self._assert_has_run()

        print("=" * 80)
        print("聚类模型运行结果")
        print("=" * 80)
        print(f"案例名称: {self.config.case_name}")
        print(f"数据路径: {self.config.data_path}")
        print(f"模型名称: {self.config.model_name}")
        print(f"样本数: {len(self.X_raw)}")
        print(f"原始特征数: {len(self.feature_cols)}")
        print(f"预处理后特征数: {self.X_processed_.shape[1]}")
        print(f"数值型特征数: {len(self.numeric_cols)}")
        print(f"分类型特征数: {len(self.categorical_cols)}")
        print(f"自动剔除列: {self.auto_dropped_cols if self.auto_dropped_cols else '无'}")
        print(f"手动剔除列: {self.user_dropped_cols if self.user_dropped_cols else '无'}")
        print("-" * 80)
        print("最佳参数:")
        for k, v in (self.best_params_ or {}).items():
            print(f"{k}: {v}")
        print("-" * 80)
        print(f"参数选择指标({self.config.scoring}): {self.best_score_:.6f}")
        print(f"Inertia              : {self.metrics_['inertia']:.6f}")
        print(f"Silhouette Score     : {self.metrics_['silhouette']:.6f}")
        print(f"Davies-Bouldin Index : {self.metrics_['davies_bouldin']:.6f}")
        print(f"Calinski-Harabasz    : {self.metrics_['calinski_harabasz']:.6f}")
        print("-" * 80)
        print("各簇样本数:")
        print(self.cluster_sizes_.to_string(index=False, formatters={"percentage": "{:.2%}".format}))
        print("-" * 80)
        if self.numeric_cols:
            print("各簇数值特征均值（前若干列）:")
            display_cols = ["cluster", "count"] + self.numeric_cols[:max_profile_cols]
            display_cols = [c for c in display_cols if c in self.cluster_summary_numeric_.columns]
            print(self.cluster_summary_numeric_[display_cols].to_string(index=False))
            if len(self.numeric_cols) > max_profile_cols:
                print(f"其余 {len(self.numeric_cols) - max_profile_cols} 个数值特征已保存到 cluster_summary_numeric.csv。")
        else:
            print("没有数值型特征，未生成数值特征均值表。")
        print("-" * 80)
        print(f"完整聚类结果已保存: {self.output_path / 'cluster_assignments.csv'}")
        print(f"输出文件夹: {self.output_path.resolve()}")
        print("=" * 80)
        return self.cluster_assignments_.copy()

    def plot(self) -> None:
        """保存聚类可视化图片，统一使用 SVG 格式。"""
        self._assert_case_ready()
        self._assert_has_run()
        out = self.output_path

        self._plot_pca_projection(out)
        self._plot_cluster_sizes(out)
        self._plot_tuning_curves(out)
        self._plot_cluster_profile_heatmap(out)

        print(f"图片已保存至：{out.resolve()}")

    # ------------------------- saving -------------------------
    def _save_artifacts(self, out: Path, normalized_grid: Dict[str, List[Any]]) -> None:
        with open(out / "searched_param_grid.json", "w", encoding="utf-8") as f:
            json.dump(normalized_grid, f, ensure_ascii=False, indent=2, default=self._json_default)

        with open(out / "best_params.json", "w", encoding="utf-8") as f:
            json.dump(self.best_params_, f, ensure_ascii=False, indent=2, default=self._json_default)

        with open(out / "metrics.json", "w", encoding="utf-8") as f:
            json.dump(self.metrics_, f, ensure_ascii=False, indent=2, default=self._json_default)

        self.grid_results_.to_csv(out / "grid_search_results.csv", index=False, encoding="utf-8-sig")
        self.cluster_sizes_.to_csv(out / "cluster_sizes.csv", index=False, encoding="utf-8-sig")
        self.cluster_summary_numeric_.to_csv(out / "cluster_summary_numeric.csv", index=False, encoding="utf-8-sig")
        self.cluster_assignments_.to_csv(out / "cluster_assignments.csv", index=False, encoding="utf-8-sig")
        self.cluster_assignments_.head(50).to_csv(out / "cluster_assignments_preview.csv", index=False, encoding="utf-8-sig")

        try:
            feature_names = self.best_pipeline.named_steps["preprocess"].get_feature_names_out()
            centers = pd.DataFrame(self.best_model.cluster_centers_, columns=feature_names)
            centers.insert(0, "cluster", np.arange(len(centers)))
            centers.to_csv(out / "cluster_centers_processed.csv", index=False, encoding="utf-8-sig")
        except Exception as exc:
            with open(out / "cluster_centers_export_error.txt", "w", encoding="utf-8") as f:
                f.write(str(exc))

        joblib.dump(self.best_pipeline, out / "best_cluster_model.joblib")

    # ------------------------- plotting -------------------------
    def _plot_pca_projection(self, out: Path) -> None:
        if self.X_processed_.shape[1] < 2:
            return
        coords = PCA(n_components=2, random_state=self.config.random_state).fit_transform(self.X_processed_)
        labels = self.cluster_labels_
        n_clusters = len(np.unique(labels))
        cmap = ListedColormap(plt.cm.tab10.colors[: max(3, n_clusters)])

        fig, ax = plt.subplots(figsize=(8, 6.2))
        scatter = ax.scatter(coords[:, 0], coords[:, 1], c=labels, cmap=cmap, alpha=0.86, s=28)
        ax.set_xlabel("PC1", fontsize=12)
        ax.set_ylabel("PC2", fontsize=12)
        ax.set_title(f"K-means Clusters by PCA Projection - {self.config.case_name}", fontsize=14)
        handles, _ = scatter.legend_elements()
        ax.legend(handles, [f"Cluster {i}" for i in sorted(np.unique(labels))], title="Cluster", fontsize=9)
        fig.tight_layout()
        fig.savefig(out / "pca_cluster_projection.svg", format="svg", bbox_inches="tight")
        plt.close(fig)

        pd.DataFrame({"PC1": coords[:, 0], "PC2": coords[:, 1], "cluster": labels}).to_csv(
            out / "pca_coordinates.csv", index=False, encoding="utf-8-sig"
        )

    def _plot_cluster_sizes(self, out: Path) -> None:
        fig, ax = plt.subplots(figsize=(7.5, 5.2))
        ax.bar(self.cluster_sizes_["cluster"].astype(str), self.cluster_sizes_["count"])
        ax.set_xlabel("Cluster", fontsize=12)
        ax.set_ylabel("Count", fontsize=12)
        ax.set_title("Cluster Sizes", fontsize=14)
        for x, y in zip(range(len(self.cluster_sizes_)), self.cluster_sizes_["count"]):
            ax.text(x, y, str(int(y)), ha="center", va="bottom", fontsize=10)
        fig.tight_layout()
        fig.savefig(out / "cluster_sizes.svg", format="svg", bbox_inches="tight")
        plt.close(fig)

    def _plot_tuning_curves(self, out: Path) -> None:
        if self.grid_results_ is None or "param_n_clusters" not in self.grid_results_.columns:
            return
        ok = self.grid_results_[self.grid_results_["status"] == "ok"].copy()
        if ok.empty:
            return
        ok["param_n_clusters"] = ok["param_n_clusters"].astype(int)

        if self.config.scoring in {"davies_bouldin", "inertia"}:
            score_by_k = ok.loc[ok.groupby("param_n_clusters")["score_for_selection"].idxmin()]
        else:
            score_by_k = ok.loc[ok.groupby("param_n_clusters")["score_for_selection"].idxmax()]
        score_by_k = score_by_k.sort_values("param_n_clusters")

        fig, ax = plt.subplots(figsize=(7.5, 5.2))
        ax.plot(score_by_k["param_n_clusters"], score_by_k["score_for_selection"], marker="o", linewidth=2)
        ax.set_xlabel("n_clusters", fontsize=12)
        ax.set_ylabel(self.config.scoring, fontsize=12)
        ax.set_title(f"Tuning Curve by n_clusters ({self.config.scoring})", fontsize=14)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(out / "tuning_score_by_k.svg", format="svg", bbox_inches="tight")
        plt.close(fig)

        inertia_by_k = ok.loc[ok.groupby("param_n_clusters")["inertia"].idxmin()].sort_values("param_n_clusters")
        fig, ax = plt.subplots(figsize=(7.5, 5.2))
        ax.plot(inertia_by_k["param_n_clusters"], inertia_by_k["inertia"], marker="o", linewidth=2)
        ax.set_xlabel("n_clusters", fontsize=12)
        ax.set_ylabel("Inertia", fontsize=12)
        ax.set_title("Elbow Curve by n_clusters", fontsize=14)
        ax.grid(True, alpha=0.3)
        fig.tight_layout()
        fig.savefig(out / "elbow_inertia_by_k.svg", format="svg", bbox_inches="tight")
        plt.close(fig)

    def _plot_cluster_profile_heatmap(self, out: Path) -> None:
        if not self.numeric_cols or self.cluster_summary_numeric_ is None or self.cluster_summary_numeric_.empty:
            return

        profile = self.cluster_summary_numeric_.set_index("cluster")
        profile = profile.drop(columns=["count"], errors="ignore")
        if profile.empty:
            return
        # 最多展示前 MAX_PROFILE_FEATURES 个数值特征，防止图像过于拥挤。
        profile = profile.iloc[:, : self.MAX_PROFILE_FEATURES]
        z = (profile - profile.mean(axis=0)) / profile.std(axis=0).replace(0, np.nan)
        z = z.fillna(0.0)

        height = max(4.5, 0.45 * len(z.index) + 2)
        width = max(8, 0.45 * len(z.columns) + 4)
        fig, ax = plt.subplots(figsize=(width, height))
        im = ax.imshow(z.values, aspect="auto", cmap="coolwarm")
        ax.set_xticks(np.arange(len(z.columns)))
        ax.set_yticks(np.arange(len(z.index)))
        ax.set_xticklabels(z.columns, rotation=45, ha="right", fontsize=9)
        ax.set_yticklabels([f"Cluster {i}" for i in z.index], fontsize=10)
        ax.set_title("Cluster Numeric Profile (z-score of cluster means)", fontsize=14)
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        fig.tight_layout()
        fig.savefig(out / "cluster_profile_heatmap.svg", format="svg", bbox_inches="tight")
        plt.close(fig)


def main() -> None:
    # ==========================================================
    # 学生主要修改本区
    # ==========================================================
    data_path = "data/wine.csv"
    case_name = "clustering_case"
    output_dir = "outputs"

    # 默认自动使用数据中的可用列；若有不希望参与聚类的列，可填写 drop_cols。
    # 例如：drop_cols = ["CustomerID", "Name"]
    drop_cols = None

    # 参数调整区：学生在这里尝试不同参数组合。
    PARAM_GRIDS = {
        "KMeans": {
            "n_clusters": [2,3,4],
            "init": ["k-means++"],
            "n_init": [10],
            "max_iter": [100],
        }
    }

    for model_name, param_grid in PARAM_GRIDS.items():
        clusterer = GeneralCluster()
        clusterer.load_case(
            data_path=data_path,
            case_name=case_name,
            model_name=model_name,
            output_dir=output_dir,
            drop_cols=drop_cols,
            scoring="silhouette",
        )
        clusterer.run(param_grid=param_grid)
        clusterer.collect_data()
        clusterer.plot()
    # ==========================================================


if __name__ == "__main__":
    main()
