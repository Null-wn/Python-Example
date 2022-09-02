import cv2
import numpy as np

#封装显示函数
def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img0=cv2.imread('ts.png')
img=img0[55:90,0:444]#ROI

#分割每一个数字
img1=cv2.imread('template.png')
x=0
for i in range(0,10):
    timg=img1[0:126,x:x+80]
    x+=80
    timg=cv2.bitwise_not(timg)
    cv2.imwrite(str(i)+'.png',timg)

#变黑白图
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

#膨胀运算
kernel = np.ones((3, 3), np.uint8)
big = cv2.dilate(thresh, kernel, iterations=5)

for i in range(0,10):
    timg=cv2.imread(str(i)+'.png')
    timg=cv2.resize(timg, None, None, fx=0.25, fy=0.25, interpolation=cv2.INTER_LANCZOS4)
    h, w = timg.shape[:2]
    timg = cv2.cvtColor(timg, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(timg, thresh, cv2.TM_CCOEFF_NORMED)
    threshold = 0.6
    # 取匹配程度大于%80的坐标
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):  # *号表示可选参数
        bottom_right = (pt[0] + w, pt[1] + h)
        # cv2.rectangle(img, pt, bottom_right, (0, 0, 255), 2)
        # print(pt)
        # print(bottom_right)
        center=(pt[0],pt[1]+h)
        text = str(i)
        cv2.putText(img0, text, center, cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1.0, (0, 0, 0), 1)

#数字分组框起来
contours, hierarchy = cv2.findContours(big, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
for i in range(0,4):
    cnt = contours[i]
    x,y,w,h = cv2.boundingRect(cnt)
    img0 = cv2.rectangle(img0,(x,y+55),(x+w,y+h+55),(0,255,0),2)

#
cv2.imwrite('res.png',img0)
cv_show('result',img0)
