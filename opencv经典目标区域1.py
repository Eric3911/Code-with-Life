'''
Author:'JungangAn';  c车牌目标检测
_*_ conding: utf-8 -*-
Time:  2019/3/21
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

# 读取图片
img = cv2.imread('Anjungang.png')

# opencv默认的imread是以BGR的方式进行存储的
lenna_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 灰度图像处理
GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(u"读入lenna图的shape为", GrayImage.shape)

# 直方图均衡化
# equ = cv2.equalizeHist(gray)

# 高斯平滑 去噪
Gaussian = cv2.GaussianBlur(GrayImage, (3, 3), 0, 0, cv2.BORDER_DEFAULT)
# Gaussian = cv2.GaussianBlur(GrayImage, (9, 9),0)

# 中值滤波
Median = cv2.medianBlur(Gaussian, 5)

# Sobel算子 XY方向求梯度 cv2.CV_8U
x = cv2.Sobel(Median, cv2.CV_32F, 1, 0, ksize=3)  # X方向
y = cv2.Sobel(Median, cv2.CV_32F, 0, 1, ksize=3)  # Y方向
# absX = cv2.convertScaleAbs(x)   # 转回uint8
# absY = cv2.convertScaleAbs(y)
# Sobel = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
gradient = cv2.subtract(x, y)
Sobel = cv2.convertScaleAbs(gradient)
cv2.imshow('dilation2', Sobel)
cv2.waitKey(0)

# 二值化处理 周围像素影响
blurred = cv2.GaussianBlur(Sobel, (9, 9), 0)  # 再进行一次高斯去噪
# 注意170可以替换的
ret, Binary = cv2.threshold(blurred, 170, 255, cv2.THRESH_BINARY)
cv2.imshow('dilation2', Binary)
cv2.waitKey(0)

# 膨胀和腐蚀操作的核函数
element1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
element2 = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 7))
# 膨胀一次，让轮廓突出
Dilation = cv2.dilate(Binary, element2, iterations=1)
# 腐蚀一次，去掉细节
Erosion = cv2.erode(Dilation, element1, iterations=1)
# 再次膨胀，让轮廓明显一些
Dilation2 = cv2.dilate(Erosion, element2, iterations=3)
cv2.imshow('Dilation2 ', Dilation2)
cv2.waitKey(0)

##########################################

# 建立一个椭圆核函数
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (25, 25))
# 执行图像形态学, 细节直接查文档，很简单
closed = cv2.morphologyEx(Binary, cv2.MORPH_CLOSE, kernel)
closed = cv2.erode(closed, None, iterations=4)
closed = cv2.dilate(closed, None, iterations=4)
cv2.imshow('erode dilate', closed)
cv2.waitKey(0)

##########################################


# 显示图形
titles = ['Source Image', 'Gray Image', 'Gaussian Image', 'Median Image',
          'Sobel Image', 'Binary Image', 'Dilation Image', 'Erosion Image', 'Dilation2 Image']
images = [lenna_img, GrayImage, Gaussian,
          Median, Sobel, Binary,
          Dilation, Erosion, closed]
for i in range(9):
    plt.subplot(3, 3, i + 1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]), plt.yticks([])
plt.show()

cv2.imshow('Gray', GrayImage)
cv2.waitKey(0)

"""
接下来使用Dilation2图片确定车牌的轮廓
这里opencv3返回的是三个参数
  参数一：二值化图像
  参数二：轮廓类型 检测的轮廓不建立等级关系
  参数三：处理近似方法  例如一个矩形轮廓只需4个点来保存轮廓信息
"""
(_, cnts, _) = cv2.findContours(closed.copy(),
                                cv2.RETR_LIST,  # RETR_TREE
                                cv2.CHAIN_APPROX_SIMPLE)

# 画出轮廓
c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
print(c)

# compute the rotated bounding box of the largest contour
rect = cv2.minAreaRect(c)
print('rectt', rect)

Box = np.int0(cv2.boxPoints(rect))
print('Box', Box)

# draw a bounding box arounded the detected barcode and display the image
Final_img = cv2.drawContours(img.copy(), [Box], -1, (0, 0, 255), 3)

cv2.imshow('Final_img', Final_img)
cv2.waitKey(0)

