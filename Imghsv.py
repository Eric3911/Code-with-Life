#conding: utf-8-
#Author:'Jungang'
#Time:2019/5/10


import cv2 as cv
import numpy as np
def color():
#***********色彩空间转换分析光斑****************
    src = cv.imread("E:/cade_data/123.png")
    cv.imshow("rgbimage",src)
    hsv = cv.cvtColor(src,cv.COLOR_BGR2HSV)
#**********通过HSV色彩通道读取图片**************
    cv.imshow("hsvimage",hsv)
    cv.imwrite('HSV.jpg',hsv)
    cv.waitKey(0)
#    cv.destroyAllWindows()
color()