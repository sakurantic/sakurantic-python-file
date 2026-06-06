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

a = 0          # 保底计数（已抽数）
b = 0          # 大保底标记，1 表示下一抽必出 UP
up_times = 0   # 累计 UP 次数
down_times = 0 # 累计歪的次数
total = 0      # 累计总抽数

def posb():
    """判断是否歪，返回 1（歪）或 2（UP）"""
    global b
    if b == 1:               # 大保底直接出 UP
        b = 0
        return 2
    if random.randint(1, 2) == 1:   # 50% 歪
        b = 1
        return 1
    else:
        b = 0
        return 2

def posa():
    """单抽，返回 0(没出)、1(歪)、2(UP)"""
    global a
    a += 1
    if a == 90:               # 硬保底
        return posb()

    if a <= 73:               # 73 抽及以前，基础概率 0.6%
        if random.randint(1, 1000) <= 6:
            return posb()
    else:                     # 74 抽开始概率线性递增
        prob = 6 + 60 * (a - 73)
        if random.randint(1, 1000) <= prob:
            return posb()
    return 0

def one_trial():
    """进行一次试验：一直抽直到出一个五星"""
    global a, b, up_times, down_times, total
    a = 0   # 重置保底计数，大保底标记 b 跨试验继承
    while True:
        result = posa()
        if result == 2:         # UP
            up_times += 1
            total += a
            break
        elif result == 1:       # 歪
            down_times += 1
            total += a
            break

# ---------- 主程序 ----------
if __name__ == "__main__":
    trials = 10_000
    for _ in range(trials):
        one_trial()
    print(f"模拟 {trials} 次")
    print(f"UP 次数: {up_times}, 歪次数: {down_times}")
    print(f"平均每个 UP 五星需要抽数: {total / up_times:.2f}")