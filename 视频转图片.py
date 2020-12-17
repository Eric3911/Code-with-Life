import cv2


# WMV视频转为ipg

vc = cv2.VideoCapture("D:\\YOLOv3_A\\video\\input_video\\Video@2020_0818_090800.wmv")
# 第一张开始命名
c = 3000
if vc.isOpened():
  rval, frame = vc.read()
else:
  rval = False


while rval:
  rval, frame = vc.read()
  if rval:
    cv2.imwrite('D:\\YOLOv3_A\\video\\output_video\\'+str(c)+'.jpg',frame)
    c = c+1
    print(c)
    cv2.waitKey(1)
vc.release()
