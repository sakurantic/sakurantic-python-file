import cv2
import numpy as np
import os
from os import path

img_dir = "./fig" # 读取图像路径
save_dir = "./result" # 保存图像路径
os.makedirs(save_dir, exist_ok="True")

image_name = "circle2.jpg" # 读取图像名称，默认会同名保存到save路径中，可以按照需求自己修改
img = cv2.imread(path.join(img_dir,image_name))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #将图像转换为灰度图像
cv2.imshow("gray",gray)
cv2.waitKey(0)

image=cv2.GaussianBlur(gray,(25,25),2) #高斯滤波降噪
cv2.imshow("gaussian",image)
cv2.waitKey(0)

#edges = cv2.Canny(gray, 100, 200, apertureSize=3)  #利用Canny进行边缘检测
#cv2.imshow("edge",edges)

#********************探究param1、param2、minRadius、maxRadius值对不同图片实验效果的影响***********************************************************
circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 2, 100,
                           param1=100, param2=100, minRadius=30, maxRadius=60)
#  param1：100-200
# param2: 20-100
# minRadius: n*10
# maxRadius: n*10
 #*******************************************************************************
                          
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        center = (i[0], i[1])
        # circle center
        cv2.circle(img, center, 1, (0, 100, 100), 3)
        # circle outline
        radius = i[2]
        cv2.circle(img, center, radius, (255, 0, 255), 3)
    
cv2.imshow('img', img)
cv2.imwrite(path.join(save_dir,image_name), img)
cv2.waitKey(0)
cv2.destroyAllWindows()




