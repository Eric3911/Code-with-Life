#conding: utf-8-
#Author:'Jungang'
#Time:2019/4/29


#图片拼接代码，子图像必须是正方型才行
import cv2
from pylab import *

img4 = cv2.imread('0.jpg')
img5 = cv2.imread('1.jpg')
img6 = cv2.imread('2.jpg')

#******拼接的图像必须是正方形********
htitch= np.hstack((img4,img5,img6))
cv2.imshow("test1",htitch)

cv2.waitKey(0)
