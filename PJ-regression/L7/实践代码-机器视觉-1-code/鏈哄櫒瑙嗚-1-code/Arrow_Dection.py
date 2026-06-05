import cv2
import numpy as np
import os

def array_detect(mod_img, target_img):
    # 平方差匹配，返回值越小越相似
    result = cv2.matchTemplate(target_img, mod_img, cv2.TM_SQDIFF)
    return result[0][0]

def absDiff(mod_img, target_img):
    diff = np.abs(mod_img - target_img)
    return np.mean(diff)

mod_img_pathes = ["./fig/mod_1.jpg", "./fig/mod_2.jpg", "./fig/mod_3.jpg", "./fig/mod_4.jpg"]
result = ["up", "right", "down", "left"]
target_img_path = "./fig/target_2.jpg"

mod_imgs = []
for path in mod_img_pathes:
    if not os.path.exists(path):
        print(f"跳过不存在的文件: {path}")
        continue
    img = cv2.imread(path)
    if img is None:
        print(f"读取失败: {path}")
        continue
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    norm = np.float32(gray) / 255.0
    mod_imgs.append(norm)

if not mod_imgs:
    print("没有有效的模板图像")
    exit(1)

# 读取目标图像
target = cv2.imread(target_img_path)
if target is None:
    print(f"目标图像读取失败: {target_img_path}")
    exit(1)
target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

scores = []
for mod in mod_imgs:
    h, w = mod.shape
    # 将目标图缩放到与当前模板相同尺寸
    target_resized = cv2.resize(target_gray, (w, h), interpolation=cv2.INTER_LINEAR)
    target_norm = np.float32(target_resized) / 255.0
    score = absDiff(mod, target_norm)
    scores.append(score)

best_idx = np.argmin(scores)
print("各模板匹配分数:", scores)
print("最优分数:", scores[best_idx])
print("匹配结果:", result[best_idx])