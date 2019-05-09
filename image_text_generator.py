#conding: utf-8-
#Author:'Fangyu'
#Time:2019/4/29


import cv2
from pylab import *
IMAGE_PATH = './tiny_image/'
IMAGE_SAVE_PATH = './imagedata/'
LABEL_SAVE_PATH = './txtdata/'
# img1 = cv2.imread('0.jpg',cv2.IMREAD_COLOR)
# # img2 = cv2.imread('1.jpg',cv2.IMREAD_GRAYSCALE) #origin
# img2 = cv2.imread('1.jpg')
# img3 = cv2.imread('2.jpg',cv2.IMREAD_UNCHANGED)
# img4 = cv2.imread('3.jpg')

# htitch= np.hstack((img1, img3, img4)) # origin right
# htitch = np.hstack((img1, img2, img3, img4)) #  test
# vtitch = np.vstack((img1, img3))
# cv2.imshow("test1",htitch)
#cv2.imshow("test2",vtitch)

for i in range(2000):
    imglist = []
    label = ''
    for j in range(18):
        num = np.random.randint(0,10)
        temp = num
        label += str(temp)
        text = str(num) + '.jpg'
        path = IMAGE_PATH + text
        img = cv2.imread(path)
        imglist.append(img)
    res = np.hstack((imglist))
    image_data_path = IMAGE_SAVE_PATH + label + '.jpg'
    cv2.imwrite(image_data_path,res)
    label_txt_path = LABEL_SAVE_PATH + label + '.txt'
    f = open(label_txt_path,'w')
    f.write(label)
    f.flush()
    f.close()

# cv2.imshow("test1",res)
# cv2.waitKey(0)
# cv2.destroyAllWindows()