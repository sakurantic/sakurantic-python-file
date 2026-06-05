import random
a=0 #抽卡保底次数
b=0 #记录大小保底是否是大小保底 1代表已经是大保底
def posb():#判断是否给歪还是不歪
    v=random.randint(1,2)
    global a
    global b
    a=0
    if v==1 and b==0:
        b=1
        return 1#waile
    else:
        b=0
        return 2
def posa():#判断这次抽卡的概率以及是否成功:
    v=random.randint(1,1000)
    global a
    a=a+1
    if a<73 and v<7 or a>73 and v<6+60*(a-73)+1 or a==90:
           return posb()
    else:
           return 0

def haveatry(times):
    for i in range(1,times+1):
        print (posa())

haveatry(80)

