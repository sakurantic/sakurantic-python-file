import cv2
import numpy as np
import os
from os import path

img_dir = "./fig" # 读取图像路径
save_dir = "./result" # 保存图像路径
os.makedirs(save_dir, exist_ok="True")
image_name = "five.jpg" # 读取图像名称
image = cv2.imread(path.join(img_dir,image_name))

# hsvim：将BGR（蓝色，绿色，红色）图像更改为HSV（色相，饱和度，值）。
hsvim = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imshow('HSV Image', hsvim)
cv2.waitKey(0)

lower = np.array([0, 48, 80], dtype = "uint8") #HSV中的肤色范围较小
upper = np.array([20, 255, 255], dtype = "uint8") #HSV中皮肤颜色的上限
skinRegionHSV = cv2.inRange(hsvim, lower, upper)  #在HSV色彩空间的上下像素值范围内检测皮肤
blurred = cv2.blur(skinRegionHSV, (2,2)) #使图像模糊以改善遮罩
ret,thresh = cv2.threshold(blurred,0,255,cv2.THRESH_BINARY) # 二值化
cv2.imshow("thresh", thresh)
cv2.waitKey(0)
                             
# 找到轮廓
contours, hierarchy= cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contour_img = image.copy()
cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 3)
cv2.imshow('Contours', contour_img)
cv2.waitKey(0)


if contours:
    # 找到最大轮廓
    max_contour = max(contours, key=cv2.contourArea)
     #计算凸包
    hull = cv2.convexHull(max_contour)
    cv2.drawContours(image, [hull], -1, (255, 0, 0), 3)
    cv2.imshow('Convex Hull', image)
    cv2.waitKey(0)
    
    #凸缺陷
    hull = cv2.convexHull(max_contour, returnPoints=False)
    defects = cv2.convexityDefects(max_contour, hull)
    
    if defects is not None:
        cnt=0
        for i in range(defects.shape[0]): #使用余弦定理识别手指
              s, e, f, d = defects[i][0]
              start = tuple(max_contour[s][0])
              end = tuple(max_contour[e][0])
              far = tuple(max_contour[f][0])
              a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
              b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
              c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
              angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) # cosine theorem
             
#*****************************************请你填写下一行*****************************************
              if angle <= np.pi/2:  # 或者填写 1.57 (即90度的弧度值)
#****************************************************************************************************
                                 cnt += 1
                                 cv2.circle(image, far, 4, [0, 0, 255], -1)
#*****************************************请你填写下一行*****************************************
        number_of_fingers = cnt + 1
#****************************************************************************************************
        
        cv2.putText(image, str(number_of_fingers), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Final Result', image)
        cv2.waitKey(0)
        
else:
    print("No contours found")

cv2.destroyAllWindows()




