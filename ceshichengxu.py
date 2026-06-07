#x=100
#print("x= %d"%x) print("x= %d" % x) 等价于：将变量 x 的整数值插入字符串 x= %d 的 %d 位置，然后打印结果
#print("a","b",sep='abc') sep为环境分隔符
#print("a","b",end='abc') end为结束符号，默认值为换行符
#标识符识别函数 类 变量 包含字母数字和_
#import keyword以上两行可以查看保留字
#float int bool complex 复数用j
#print(round(12.3222,1))round 计算近似值
#print("parrot"[0])[0]索引字符串，0为第一位以此类推
#int() float() str()
#集合：用大括号{} 无需不重复 创建空集合：a=set()
#列表：[],[0]返回第一个元素,[-1]返回倒数第一个元素
#元组()用小括号，有序对象并且不可以修改
#a={"a":1,"b":2}
#print[a("a")]
#运算符：=-*/ //整除 %余数 **取幂
#== ！= >= <= ><
#c+=a c=c+a 其他以此类推
#x and y \if x=false xandy=false or xandy=y
#x or y \ if x=true xory=true or xory=y
#notx\ ifx=false notx=true 反之亦然
#a=12;b=24
#print(a and b,a or b,not a,not b)
#@@位运算符
#成员运算符  in 或者not in 身份运算 is或者not is
#print(3.002//3.1) 结果：0.0
#print(type(1),type("a"),type(1.2)) 用type判断数值类型
#a[0]=1
#a[0:1]=[1,2]#把0到1中的数列提取掉
#print(a)
#数列可以相加，相乘。可以用len，max，min
#append放在列表结尾，加入元素，clear清空元素，相当于del a[:]
#copy复制列表，count计算列表中那个值的个数 extend添加列表的值加入进该列表中
#index索引，insert（index，object）在相应位置插入元素
#pop（index）将索引值对应的object删除 remove（value）将对应的object的值删除
#reverse颠倒列表，sort排序
#a=[(x,y,z) for x in range(1,30 ) for y in range(1,30 ) for z in range(1,30) if x**2+y**2==z**2]
#print(a)
#等价于：
# result = []
# for x in range(1, 30):       # 最外层循环
#     for y in range(1, 30):   # 中间层循环（依赖外层 x）
#         for z in range(1, 30):  # 最内层循环（依赖外层 x, y）
#             if x**2 + y**2 == z**2:  # 条件判断（在所有变量确定后执行）
#                 result.append((x, y, z))
#元组和列表类似不能改数值，可以用len，max,min,sum
# aa={1:2,3:4}#元素值可以改，键值前面那个不可以改
# del aa[1]
# print(aa[3])
# # 可以用len str type  注意后面这下前面要加上字典名臣加上. e.g: aa.clear  clear copy
# print(aa.get(5,"a"))#如果不存在，返回逗号后面那个
# #items（）把字典变成元组，keys创建一个键值的列表对象，values创建数值的列表对象popitem去除字典中的最后一个元素
#list把元组转化为列表，tuple把列表转化为元组
# a=("abcdefg")
# print(a[1:3])#含开头不含结尾
# print(a[:3])
# print(a[:])
# a=a[:5]+"a"+a[7:]
# print(a)
#在字符串内使用转义字符：换行\n 双引号\" 单引号\'
#字符串可以相加，相乘，可以逻辑运算，可以用in，not in
#%d可以格式化整数，%s可以格式化字符串
# a="abc%sabc%d"
# b=("a",2)
# print(a%b)#captilize()将字符串的第一个改成大写
# str="abcanbcabc"
# print(str.count("a",0,3))#count 输出字符串中的特定数字出现的次数
# print(str.index("anb",0,8))#索引sub中的内容，如果有，返回start值，如果没有报错
# #maxmin返回字符串中的最大最小值，
# print(str.replace("a","b",1))#替换，count指的是最大替换次数
# x,y,z=1,2,3#也可以a=b=c=1
# x,y=y,x#语句合法
# print(x,y,z)
# r=float(input("input the r"))
# print("The area of the circle is",3.1415*r**2) 计算圆的半径与面积
#print(True+False)#type(True)=bool
# 例子：求和公式：：：while True:
#     a = int(input().strip())  # 读取输入并转换为整数
#     if a == 666:              # 关键检查：如果输入是666
#         break                 # 立即跳出整个循环，结束程序
#     # 以下代码仅在输入非666时执行
#     total = 0                 # 避免使用内置名 sum（已修改为 total）
#     b = 0
#     while b <= a:
#         total += b
#         b += 1
#     print(total)


# # break: 遇到 j=1 时终止内层循环
# for i in range(2):
#     for j in range(3):
#         if j == 1:
#             break
#         print(f"break: i={i}, j={j}")
# # 输出: break: i=0, j=0; break: i=1, j=0
#
# # continue: 遇到 j=1 时跳过当前迭代
# for i in range(2):
#     for j in range(3):
#         if j == 1:
#             continue
#         print(f"continue: i={i}, j={j}")
# # 输出: break: i=0, j=0
# # break: i=1, j=0
# # continue: i=0, j=0
# # continue: i=0, j=2
# # continue: i=1, j=0
# # continue: i=1, j=2


# range（10）：1-9 range(1，9）：1-8 （1，9，2）：1，3，5，7
# answer = 10

# answer=10
# while True:
#     a = int(input("请输入猜测的数字: "))
#
#     if a == answer:
#         print("well done")
#         break  # 猜对了，直接跳出循环
#     else:
#         print("not done")

# def abc():#自定义函数
#
#     return "aaa"
#     return "bbb"
# print(abc())

#None代表没有值，可以理解为每一句后面都默认加上returnnone 类似于理解为每一句while for都隐藏式的以continue收尾
#注意全局变量和局部作用域的变量 后者为调用函数时用到的局部作用域的变量不可以在外部使用 例子：

# def abc():
#     a=1
#     b=2
#     print(a)
# abc()
# print(b)#只会返回1不会返回2

# aaa=2
# def abc():
#     global aaa #global使得aaa被声明为全局变量，故而，可以在局部函数里修改全局函数的值
#     aaa=1
# abc()
# print(aaa)

# def division(a):
#
#     try:
#         return 43/a
#     except ZeroDivisionError:#except 可以让你遇到特定错误输出，并且跳过！
#         return "division error"#确保每个分支都有返回值
#
# print(division(1))
# print(division(0))
# print(division(2))
# p=int(input())
# print(p)
# def mat(p):
#     while True:
#         if p!=1:
#             if p%2==0:
#                 p=p//2
#                 print(p)
#             else:
#                 p=p*3+1
#                 print(p)
#         else:
#             break
#     print(p)
#
# mat(p)

# numbermax=20000
# def cal(p1):
#     q=0
#     p=p1
#     if p==1:
#         list.append([1,1])
#     while p != 1:
#         p = p // 2 if p % 2 == 0 else p * 3 + 1
#         q=q+1
#         if p==1:
#             list.append([p1,q])
# list=[]
# for p1 in range(1,numbermax):
#     cal(p1)
# listexamine=[]
# for i in range(0,numbermax-1):
#     listexamine.append(list[i][1])
#
# print(list)
# print(listexamine)
# print(listexamine.index(max(listexamine))+1)

# numbermax = 2000000
#
# def cal(p1):
#     steps = 0
#     current = p1
#     while current != 1:
#         current = current // 2 if current % 2 == 0 else current * 3 + 1
#         steps += 1
#     return [p1, steps]
#
# results = [cal(i) for i in range(1, numbermax)]
# steps_list = [i[1] for i in results]
#
# print(f"最长步数对应的数字: {steps_list.index(max(steps_list)) + 1}")
# print(f"最大步数: {max(steps_list)}")

# def find_max_steps(limit):
#     """
#     使用记忆化优化的Collatz序列步长查找
#     """
#     # 记忆化字典，存储已计算的数字及其步长
#     memo = {1: 0}
#
#     def get_steps(n):
#         if n in memo:
#             return memo[n]
#
#         original_n = n
#         path = []  # 记录路径上的数字
#
#         # 向下搜索直到遇到已知数字
#         while n not in memo:
#             path.append(n)
#             n = n // 2 if n % 2 == 0 else n * 3 + 1
#
#         # 回溯计算路径上所有数字的步长
#         base_steps = memo[n]
#         for i, num in enumerate(reversed(path)):
#             memo[num] = base_steps + i + 1
#
#         return memo[original_n]
#
#     max_steps = 0
#     result_num = 1
#
#     for i in range(1, limit):
#         steps = get_steps(i)
#         if steps > max_steps:
#             max_steps = steps
#             result_num = i
#
#     return result_num, max_steps
#
#
# # 测试小范围
# print("计算中...")
# target_num, steps = find_max_steps(2000000)
# print(f"200万以内步数最多的数字: {target_num}")
# print(f"步数: {steps}")

# fruits = ["apple", "banana", "cherry"]
# for index, fruit in enumerate(fruits):#enumerate给出列表中的第几个的编号以及其中包含的内容
#     print(f"索引 {index}：水果 {fruit}")

#列表中可以用key-value keys()输出键值 values输出对应的内容值，items把两个作为元组输出
#get（“key“，0）如果所引到，给出value，否则给出你后面给的那个数字
#setdefault（a,b)如果a在字典里，那么把a对应的value给你，否则把对应的a，b加到字典里面去
# message="ashjkdiochioqyxahsdfhashkhqewclhiouquychsahkldchjh akhhwjlkhdewkljcdyas,jwq"
# count={}
# for word in message:
#     count.setdefault(word,0)
#     count[word]+=1
# print(count)

#有用的函数;abs绝对值，

#循环调用函数，如下面这个计算阶乘的函数


# while True:
#     def f(n):
#         if n==1:
#             return 1
#         return n*f(n-1)
#     print(f(int(input())))


# import random
# a=0 #抽卡保底次数
# b=0 #记录大小保底是否是大小保底 1代表已经是大保底
# uptimes=0
# downtimes=0
# c=0
# def posb():#判断是否给歪还是不歪
#     v=random.randint(1,2)
#     global b
#     if v==1 and b==0:
#         b=1
#         return 1#waile
#     else:
#         b=0
#         return 2
# def posa():#判断这次抽卡的概率以及是否成功:
#     v=random.randint(1,1000)
#     global a
#     a=a+1
#     if a<74 and v<7 or a>73 and v<6+60*(a-73)+1 or a==90:
#            return posb()
#     else:
#            return 0
#
# def haveatry():
#     global a, uptimes, c, downtimes
#     while True:
#         p=posa()
#
#         if p==2:
#              print(a,"up")
#              uptimes=uptimes+1
#              c=c+a
#              a=0
#
#              break
#         elif p==1:
#             print(a,"down")
#             downtimes=downtimes+1
#             c=c+a
#             a=0
#             break
#
# for i in range(10000):
#     haveatry()
# print(c/uptimes)
#
import random

# a = 0          # 保底计数（已抽数）
# b = 0          # 大保底标记，1 表示下一抽必出 UP
# up_times = 0   # 累计 UP 次数
# down_times = 0 # 累计歪的次数
# total = 0      # 累计总抽数
import random
import sys


import random


# ---------- 您的原代码（一字不改） ----------
class chouka:
    """这是在进行抽卡模拟"""

    def __init__(self):
        self.baodi_xiao = 0
        self.baodi_da = 0
        self.up_times = 0
        self.down_times = 0
        self.total = 0

    def posbaodi_da(self):
        """判断是否歪，返回 1（歪）或 2（UP）"""
        if self.baodi_da == 1:               # 大保底直接出 UP
            self.baodi_da = 0
            return 2
        if random.randint(1, 2) == 1:   # 50% 歪
            self.baodi_da = 1
            return 1
        else:
            self.baodi_da = 0
            return 2

    def posbaodi_xiao(self):
        """单抽，返回 0(没出五星)、1(歪)、2(UP)"""
        self.baodi_xiao = self.baodi_xiao + 1
        if self.baodi_xiao == 90:               # 硬保底
            return self.posbaodi_da()

        if self.baodi_xiao <= 73:               # 73 抽及以前，基础概率 0.6%
            if random.randint(1, 1000) <= 6:
                return self.posbaodi_da()
        else:                     # 74 抽开始概率线性递增
            prob = 6 + 60 * (self.baodi_xiao - 73)
            if random.randint(1, 1000) <= prob:
                return self.posbaodi_da()
        return 0

    def one_trial(self):
        """进行一次试验：一直抽直到出一个五星"""
        while True:
            result = self.posbaodi_xiao()
            if result == 2:         # UP
                self.up_times += 1
                self.total += self.baodi_xiao
                self.baodi_xiao = 0
                break
            elif result == 1:       # 歪
                self.down_times += 1
                self.total += self.baodi_xiao
                self.baodi_xiao = 0
                break

    def run_times(self, times):
        for i in range(times):
            self.one_trial()
# ---------- 原代码结束 ----------


def print_result(step, code, pity):
    """根据抽卡结果打印彩色信息（五星金，其他蓝色）"""
    if code == 2:
        print(f"\033[33m第{step}抽 ★★★★★ 获得UP五星！ (当前保底计数:{pity})\033[0m")
    elif code == 1:
        print(f"\033[33m第{step}抽 ★★★★★ 获得常驻五星 (歪了) (当前保底计数:{pity})\033[0m")
    else:
        pass



def interactive():
    gacha = chouka()
    print("=" * 50)
    print("原神抽卡模拟器 (基于您的 chouka 类)")
    print("命令：输入抽卡次数(正整数)  |  r 重置进度  |  q 退出")
    print("提示：五星概率0.6%，74抽后递增，90抽硬保底")
    print("=" * 50)

    total_wishes = 0          # 记录本次会话的总抽卡次数
    five_star_count = 0       # 记录出了多少五星（包括歪和UP）
    up_count = 0              # UP五星次数

    while True:
        cmd = input("\n> ").strip().lower()
        if cmd == 'q':
            print("感谢使用，再见！")
            break
        elif cmd == 'r':
            # 重置：重新实例化对象，清空统计变量
            gacha = chouka()
            total_wishes = 0
            five_star_count = 0
            up_count = 0
            print("✓ 已重置保底、UP计数和抽卡记录")
            continue

        # 尝试解析为整数（抽卡次数）
        try:
            num = int(cmd)
            if num <= 0:
                print("抽卡次数必须是正整数")
                continue
        except ValueError:
            print("无效输入，请输入正整数抽卡次数、r 或 q")
            continue

        print(f"\n开始 {num} 连抽...")
        for i in range(1, num + 1):
            # 重要修复：原 posbaodi_xiao 不会自动重置 baodi_xiao，需要手动重置
            result = gacha.posbaodi_xiao()
            # 获取当前的五星保底计数（已经更新后的值，即本次抽卡后的累计数）
            pity = gacha.baodi_xiao
            print_result(total_wishes + i, result, pity)

            # 如果出了五星（result != 0），必须重置保底计数器，否则保底会错误累积
            if result != 0:
                gacha.baodi_xiao = 0
                # 更新统计
                five_star_count += 1
                if result == 2:
                    up_count += 1

        total_wishes += num

        # 输出本次抽卡后的简要统计
        print("\n--- 当前统计 ---")
        print(f"累计抽卡: {total_wishes}")
        print(f"累计五星: {five_star_count}  (UP: {up_count}, 歪: {five_star_count - up_count})")
        if five_star_count > 0:
            avg = total_wishes / five_star_count
            print(f"平均每 {avg:.1f} 抽出一个五星")
        print(f"当前五星保底计数: {gacha.baodi_xiao} / 90")
        print(f"当前大保底状态: {'已触发（下次必UP）' if gacha.baodi_da == 1 else '未触发（小保底）'}")
        print("----------------")


if __name__ == "__main__":
    interactive()