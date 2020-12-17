import cv2


# WMV视频转为JPG

vc = cv2.VideoCapture("D:\\video\\input_video\\Video@2020_01.wmv")
# 第一张开始命名
c = 3000
if vc.isOpened():
  rval, frame = vc.read()
else:
  rval = False


while rval:
  rval, frame = vc.read()
  if rval:
    cv2.imwrite('D:\\video\\output_video\\'+str(c)+'.jpg',frame)
    c = c+1
    print(c)
    cv2.waitKey(1)
vc.release()
