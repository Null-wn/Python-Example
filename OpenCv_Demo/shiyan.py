import cv2
import numpy as np

img = cv2.imread('xxx.jpg')   #此处用本地图片替代摄像头捕捉的照片
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)		#findContours只能检测二值化后的图片

contours,Hierarchy = cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
print (type(contours))
print (type(contours[0]))

for cnt in range(contours[cnt]):
    cv2.drawContours(frame, contours[cnt],-1,(255,0,0),3)           #画出灯条轮廓
