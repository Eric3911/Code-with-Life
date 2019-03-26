
import cv2

if __name__ == '__main__':

    img = cv2.imread('E:/code with life/1.jpg')

    height, width = img.shape[:2]
    # 缩小图像到原来的1/2倍
    size = (int(width*0.5), int(height*0.5))
    #INTER_NEAREST | 最近邻插值
    shrink_NEAREST = cv2.resize(img, size, interpolation=cv2.INTER_NEAREST)
    #INTER_LINEAR | 双线性插值（默认设置）
    shrink_LINEAR = cv2.resize(img, size, interpolation=cv2.INTER_LINEAR)
    #INTER_AREA | 使用像素区域关系进行重采样
    shrink_AREA = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
    #INTER_CUBIC  | 4x4像素邻域的双三次插值
    shrink_CUBIC = cv2.resize(img, size, interpolation=cv2.INTER_CUBIC)
    #INTER_LANCZOS4 |  8x8像素邻域的Lanczos插值
    shrink_LANCZOS4 = cv2.resize(img, size, interpolation=cv2.INTER_LANCZOS4)

    # 放大图像到原来2倍
    fx = 2
    fy = 2
    enlarge_NEAREST = cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_NEAREST)
    enlarge_LINEAR = cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)
    enlarge_AREA = cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_AREA)
    enlarge_CUBIC = cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)
    enlarge_LANCZOS4 = cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_LANCZOS4)

    # 保存图像
    cv2.imwrite("shrink_NEAREST.jpg", shrink_NEAREST)
    cv2.imwrite("shrink_LINEAR.jpg", shrink_LINEAR)
    cv2.imwrite("shrink_AREA.jpg", shrink_AREA)
    cv2.imwrite("shrink_CUBIC.jpg", shrink_CUBIC)
    cv2.imwrite("shrink_LANCZOS4.jpg", shrink_LANCZOS4)
    cv2.imwrite("enlarge_NEAREST.jpg", enlarge_NEAREST)
    cv2.imwrite("enlarge_LINEAR.jpg", enlarge_LINEAR)
    cv2.imwrite("enlarge_AREA.jpg", enlarge_AREA)
    cv2.imwrite("enlarge_CUBIC.jpg", enlarge_CUBIC)
    cv2.imwrite("enlarge_LANCZOS4.jpg", enlarge_LANCZOS4)
cv2.waitKey(0)
