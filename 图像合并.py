#conding: utf-8-
#Author:'Jungang'
#Time:2019/4/29


import cv2
from pylab import *

img1 = cv2.imread('0.jpg',cv2.IMREAD_COLOR)
img2 = cv2.imread('1.jpg',cv2.IMREAD_GRAYSCALE)
img3 = cv2.imread('2.jpg',cv2.IMREAD_UNCHANGED)
img4 = cv2.imread('3.jpg')

htitch= np.hstack((img1, img3,img4))
#vtitch = np.vstack((img1, img3))
cv2.imshow("test1",htitch)
#cv2.imshow("test2",vtitch)

cv2.waitKey(0)
cv2.destroyAllWindows()