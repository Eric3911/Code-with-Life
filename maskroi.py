'''
Author:'JungangAn';
_*_ conding: utf-8 -*-
Time:  2019/3/23
'''
#***该掩码是对其他区域像素为0黑色模板区域保持原来像素**********************

import cv2
import numpy as np
import os
import glob
def detect_img():
    # path = "C:/keras/*.jpg"
    # outdir = "C:/keras/"
    path = '*.jpg'
    outdir = 'testdata/'
    for jpgfile in glob.glob(path):
        # img = Image.open(jpgfile)
        img = cv2.imread(jpgfile)
        shape = img.shape
        # #704*576
        points_704 = np.array([[80, 530], [440, 530], [270, 50], [225, 50]])

        height = shape[1]
        if height != 704:
            continue

        img_origin = img.copy()
        cv2.fillConvexPoly(img, points_704, 1)
        bitwisexor = cv2.bitwise_xor(img, img_origin)
        # bitwisexor.save(os.path.join(outdir, os.path.basename(jpgfile)))
        cv2.imwrite(os.path.join(outdir, os.path.basename(jpgfile)), bitwisexor)
detect_img()

