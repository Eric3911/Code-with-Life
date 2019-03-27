
import cv2

img = cv2.imread('C:/Users/Administrator/Desktop/pic/mask/Mark/mask/Mask21.jpg')

#均值滤波
blur = cv2.blur(img,(5,5))
#中值滤波，脉冲噪声和椒盐噪声滤除作用明显
median= cv2.medianBlur(img,5)
#高斯滤波
gauss = cv2.GaussianBlur(img,(5,5),1)
#双边滤波
shuangBian = cv2.bilateralFilter(img,7,50,50)

cv2.imwrite('blur.jpg',blur)
cv2.imwrite('median.jpg',median)
cv2.imwrite('gauss.jpg',gauss)
cv2.imwrite('bilatera.jpg',shuangBian)
cv2.waitKey()