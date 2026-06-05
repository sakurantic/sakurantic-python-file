import cv2
import numpy as np
import os
from os import path

img_dir = "./fig" # 读取图像路径
save_dir = "./result" # 保存图像路径
os.makedirs(save_dir, exist_ok="True")


image_name = "line1.jpg" # 读取图像名称，默认会同名保存到save路径中，可以按照需求自己修改
img = cv2.imread(path.join(img_dir,image_name))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #将图像转换为灰度图像
cv2.imshow("gray",gray)
cv2.waitKey(0)

image=cv2.GaussianBlur(gray,(25,25),2) #高斯滤波降噪
#cv2.imshow("gaussian",image)
cv2.waitKey(0)

edges = cv2.Canny(gray, 100, 200, apertureSize=3)  #利用Canny进行边缘检测
cv2.imshow("edge",edges)
cv2.waitKey(0)

#*******************************************************************************
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=150,  minLineLength=100, maxLineGap=10)  #自动检测可能的直线，返回的是一条条线段 x1, y1, x2, y2
#推荐取值：
#threshold:50-150
#minLineLength: n*10
#maxLineGap：n*10
#*******************************************************************************

for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    
#lines = cv2.HoughLines(edges, 1, np.pi / 180, 50)
#if lines is not None:
#    for rho, theta in lines[:,0]:
#        a = np.cos(theta)
#        b = np.sin(theta)
#        x0 = a * rho
#        y0 = b * rho
#        x1 = int(x0 + 1000 * (-b))
#        y2 = int(y0 + 1000 * (a))
#        x2 = int(x0 - 1000 * (-b))
#        y1 = int(y0 - 1000 * (a))

#        cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    
cv2.imshow('img', img)
cv2.imwrite(path.join(save_dir,image_name), img)
cv2.waitKey(0)
cv2.destroyAllWindows()






