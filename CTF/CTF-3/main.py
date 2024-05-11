import cv2

image1 = cv2.imread('first.png')
image2 = cv2.imread('second.png')

cv2.imwrite("flag.png", image1+image2)
