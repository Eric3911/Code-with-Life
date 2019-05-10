'''
Author:'JungangAn';
_*_ conding: utf-8 -*-
Time:  2019/3/20
'''


#图片文件批量重命名
import os

class ImageRename():
    def __init__(self):
        self.path = 'D:/ca/'

    def rename(self):
        filelist = os.listdir(self.path)
        total_num = len(filelist)
        start = 0

        for item in filelist:
            if item.endswith('.jpg'):
                src = os.path.join(os.path.abspath(self.path), item)
#*******************************1为名称[代码缺陷超过1000张后重命名可以多一位0]*************************
                dst = os.path.join(os.path.abspath(self.path), '1' + format(str(i), '0>3s') + '.jpg')
                os.rename(src, dst)
                print('conerting %s to %s ...' %(src,dst))
                i = i + 1
        print( 'total %d to rename & converted %d jpgs'%(total_num, start))

if __name__ == '__main__':
    newname = ImageRename()
    newname.rename()