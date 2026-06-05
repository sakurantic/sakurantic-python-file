import cv2
import numpy as np
import os
from os import path

img_dir = "./fig" # 读取图像路径
save_dir = "./result" # 保存图像路径
os.makedirs(save_dir, exist_ok=True)
image_name = "Harris_1.jpg" # 读取图像名称，默认会同名保存到save路径中，可以按照需求自己修改

img = cv2.imread(path.join(img_dir,image_name))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 需要转换为灰度图
gray = np.float32(gray)
# 这三个参数即为本次探索参数，主要探索前两个，具体见ppt
dst = cv2.cornerHarris(gray,3,5,0.04)
img[dst>0.01 * dst.max()] = [0, 0, 255] # 检测到的角点画红色

cv2.imshow('corners', img)
cv2.imwrite(path.join(save_dir,image_name), img)
cv2.waitKey()
cv2.destroyAllWindows()