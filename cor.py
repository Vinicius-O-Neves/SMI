from cv2 import cv2
import numpy as np
import os
import sys

def nothing(x):
    pass

cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")

cv2.createTrackbar("L – H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L – S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L – V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U – H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U – S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U – V", "Trackbars", 255, 255, nothing)

while True:
    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L – H", "Trackbars")
    l_s = cv2.getTrackbarPos("L – S", "Trackbars")
    l_v = cv2.getTrackbarPos("L – V", "Trackbars")
    u_h = cv2.getTrackbarPos("U – H", "Trackbars")
    u_s = cv2.getTrackbarPos("U – S", "Trackbars")
    u_v = cv2.getTrackbarPos("U – V", "Trackbars")

    low_blue = np.array([l_h, l_s, l_v])
    high_blue = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, low_blue, high_blue)
 
    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("result", result)

    with open('low_blue.txt', 'w') as arquivo1:
        for valor1 in low_blue:
            arquivo1.write(str(valor1) + '\n')
             
    with open('high_blue.txt', 'w') as arquivo2:
        for valor2 in high_blue:
            arquivo2.write(str(valor2) + '\n')

 
    key = cv2.waitKey(1)
    if key == 13:
       os.startfile('config.ini')
       break

cap.release()
cv2.destroyAllWindows()