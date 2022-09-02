import cv2

def cv_show(name,img):#输出函数
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img=cv2.imread('test.png')


ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

max=0
max1=0
max2=0
min=1000

for i in range(1,len(contours)-1):#从1开始循环
    if(i%2):#只有奇数才是外边界
        cnt = contours[i]
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        x=cv2.arcLength(cnt, True)/radius#齿轮>7,垫片6.55到7，六角螺母6.55以下
        if x>7:#齿轮,绿色
            if radius>max:#找出最大齿轮
                max=radius
                tcenter1=(int(x)+20, int(y))#输出在中心
            res1 = cv2.circle(img, center, radius, (255, 0, 0), 2)

        if x>=6.55 and x<=7:#垫片，橙色
            res1 = cv2.circle(img, center, radius, (0, 255, 0), 2)
            if radius < min:
                min = radius
                tcenter3 = center
            cnt = contours[i-1]
            (x, y), tradius = cv2.minEnclosingCircle(cnt)
            tradius = int(tradius)

        if x<=6.55:#六角螺母，紫色
            res1 = cv2.circle(img, center, radius, (0, 0, 255), 2)
            # 第二大六角螺母
            if radius > max1:#打擂台算法找到第二大
                max1 = radius
            if radius < max1 and radius > max2:
                max2 = radius
                tcenter2 = center

#根据周长与半径比值不同分辨图形类型
#输出结果
cv_show('res1',res1)
cv2.imwrite("res1.jpg", res1);
#拓展
res2=res1

#最大齿轮
text1=str(max)
cv2.putText(res2, text1, tcenter1, cv2.FONT_HERSHEY_COMPLEX, 1.0, (255,144,30), 1)

#第二大螺母

text2=str(max2)
cv2.putText(res2, text2, tcenter2, cv2.FONT_HERSHEY_COMPLEX, 1.0, (255,144,30), 1)

#填充红色，画一大一小两个圆
cv2.circle(res2,tcenter3,min,(0,0,255),-1)#红色填充
cv2.circle(res2,tcenter3,tradius,(255,255,255),-1)#中间白色部分
cv_show('res2',res2)
cv2.imwrite("res2.jpg", res2);
