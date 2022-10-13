import cv2
import numpy as np

def cv_show(name,img):#输出函数
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#检测蓝色
vc = cv2.VideoCapture('shibie1.mp4')

while True:
    ret, frame = vc.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    bimg,ging,rimg=cv2.split(frame)
    img=cv2.subtract(bimg, rimg)
    ret,img=cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)

    kernel = np.ones((1, 10), np.uint8)
    img = cv2.dilate(img, kernel, iterations=5)
    max_color = img & thresh
    contours, Hierarchy = cv2.findContours(max_color, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for i in range(0,len(contours)):
        for j in range(0,i):
            ok=False
            cnt = contours[i]
            tcnt= contours[j]
            x, y, w, h = cv2.boundingRect(cnt)
            tx,ty,tw,th=cv2.boundingRect(tcnt)
            if tx < x:
                tx, x = x, tx
            if 2*w>h or 2*tw>th:   #灯条长小于宽
                break
            if abs(y-ty)>2*w or abs(h-th)>2*w:  #两个灯条高度相差过大
                break
            if w*h-tw*th>500:  #两个灯条面积相差过大
                break
            frame = cv2.rectangle(frame, (x, y), (tx + tw, ty + th), (0, 255, 0), 2)

    cv2.imshow('res', frame)
    if cv2.waitKey(0) & 0xFF == 27:
        break
