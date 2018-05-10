import cv2

img =cv2.imread("/home/pdesahb/Pictures/background/Albert Aublet - Selene (1880).jpg", cv2.IMREAD_COLOR)
print(img)
cv2.imshow("lol", img)
cv2.waitKey()
