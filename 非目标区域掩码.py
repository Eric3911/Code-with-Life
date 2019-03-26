import cv2
import numpy as np
import os
import glob
def detect_img():

    path = 'E:/code with life/test/*.jpg'
    outdir = 'E:/code with life/3/3_1/'
    for jpgfile in glob.glob(path):

        img = cv2.imread(jpgfile)
        shape = img.shape
        points_704 = np.array([[80, 530], [440, 530], [270, 50], [225, 50]])

        height = shape[1]
        if height != 704:
            continue
        img_origin = img.copy()
        cv2.fillConvexPoly(img, points_704, 1)
        bitwisexor = cv2.bitwise_xor(img, img_origin)
        cv2.imwrite(os.path.join(outdir, os.path.basename(jpgfile)), bitwisexor)
detect_img()

