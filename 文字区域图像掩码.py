
import numpy as np
import cv2

img = cv2.imread('C:/c/2.jpg')
roi_list = list()

#*******************对除过文字非目标区域进行掩码*****
rois = np.array([
    
#*******************这里可以写多个目标区域************
     [[300, 140], [700, 140], [700, 200], [300, 200]],
     [[100, 180], [440, 180], [440, 200], [100, 200]],
     
   

])
for roi in rois:
    xmin = np.min([coordinates[0] for coordinates in roi])
    xmax = np.max([coordinates[0] for coordinates in roi])
    ymin = np.min([coordinates[1] for coordinates in roi])
    ymax = np.max([coordinates[1] for coordinates in roi])
    roi_list.append((xmin, xmax, ymin, ymax))

result = np.zeros_like(img)
for roi in roi_list:
    result[roi[2]:roi[3], roi[0]:roi[1]] = img[roi[2]:roi[3], roi[0]:roi[1]]

cv2.imshow("result", result)
cv2.imwrite('3.jpg',result)
cv2.waitKey(0)

