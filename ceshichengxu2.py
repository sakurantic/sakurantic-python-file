#类与对象 有下划线的代表是类里面的私有变量 外界不能随便读取或者访问
# #init是对象诞生石=时候给的初始化数据 self就是你赋值的那个对象 但它现在还没有名字 你只能用self代替了
#.doc可以读取对象里面第一行的文字 就当是一张注释
#可以用对象名称.属性名称来命名
# class a:
#     pass
# b=a()
# isinstance(b,a)
# print(b)
#ininstance可以判断一个对象是否在一个类里面 然后还有
#b现在只有一个分配到的地址所以printb只会显示他现在的地址


# class a:
#     def __init__(self,name=0):
#         self.name=name
# b=a("mynameisbbb")
# isinstance(b,a)
# print(b)
# print(b.name)
#实例（也就是对象）变量的被搜索优先级高于类变量（在类里面同意声明的）
#对象内置属性 .dict or .class
#类的内置方法 __str__ __init__ 这个被内置函数str和print调用
#你知道为什么要用__str__吗 就以这个为例子 如果你用printstr 首先如果你有内部的属性它是无法调用的
#第二 你需要一直修改 而你直接定义str他就可以直接被print或者str所引用非常的舒适
#还可以用__call__(把他变成函数形式）可以在函数里面被调用 __len__在len里面被调用
# __eq__(self other）在外面写对象a==对象b的时候

# def __eq__(self, other):
#     return self.name == other.name # 只要名字一样，== 号就返回 True
#
# class Calculator:
#     def __call__(self, x, y):
#         return x + y
#
# calc = Calculator() # calc 是一个对象
# print(calc(3, 5))   # 🎯 居然可以直接加括号当函数用！输出 8

#重载结构
# class Backpack:
#     def __init__(self, gold):
#         self.gold = gold
#
#     def __add__(self, other):
#         # 定义什么叫“两个背包相加”：金币相加，并生成一个新的背包
#         return Backpack(self.gold + other.gold)
#
# b1 = Backpack(100)
# b2 = Backpack(200)
# b3 = b1 + b2  # 触发了 __add__
# print(b3.gold)  # 输出 300
#
# import random
# #--str--是魔术方法 只有在触发特定条件的时候才会被调用 别的时候普通方法都是强制性顺下去调用的
# class BaseGacha:
#     def __init__(self, name):
#         self.name = name
#         self.pity_count = 0  # 保底水位
#
#     def draw(self):
#         self.pity_count += 1
#         # 基础抽卡逻辑：千分之六的概率
#         if random.randint(1, 1000) <= 6:
#             print(f"[{self.name}] 恭喜！第 {self.pity_count} 抽抽中了五星！")
#             self.pity_count = 0  # 重置水位
#         else:
#             print(f"[{self.name}] 第 {self.pity_count} 抽，蓝天白云。")
#
#
# class UPGacha(BaseGacha):
#     def draw(self):
#         # 1. 委托：先调用父类，把“通用逻辑（加1、抽卡核心计算）”做完
#         super().draw()
#
#         # 2. 扩展：在父类逻辑的基础上，增加“限定池特有的判断”
#         # 比如：如果刚才父类执行完，发现水位到了80，我就做额外处理
#         if self.pity_count >= 80:
#             print(f"[{self.name}] 触发保底机制！")
# # 测试父类
# # basic = BaseGacha("常驻池")
# # basic.draw()
#
# # # 测试子类
# limited = UPGacha("钟离UP池","钟离")
# limited.draw()

#类的封装与多态 多态就是一个同名函数可以执行不同的操作 代码如下:
# class Role:
#     def attack(self):
#         raise NotImplementedError("子类必须实现此方法")
#
# class Warrior(Role):
#     def attack(self):
#         print("战士：挥舞巨剑！")
#
# class Mage(Role):
#     def attack(self):
#         print("法师：释放禁咒！")
#
# # 统一处理接口
# def battle(role_list):
#     for role in role_list:
#         role.attack()  # 多态调用：同名方法，不同行为
#
# roles = [Warrior(), Mage()]
# battle(roles)

#还有类的封装 直白点就是通过__把数据隐藏起来不让外部接口的人直接改