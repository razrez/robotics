import cv2
import numpy as np

circles = np.zeros((4, 2), np.int32)
counter = 0


def draw_circle(event, x, y, flags, params):
    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        circles[counter] = x, y
        counter += 1
        cv2.circle(img_wrap, (x, y), 3, (255, 255, 0), -1)
        print(circles)


img_wrap = cv2.imread('sourcePics/cards.jpg')

while True:

    cv2.imshow('orig', img_wrap)
    cv2.setMouseCallback('orig', draw_circle)

    if counter == 4:
        height, width = 350, 250
        pts1 = np.float32([circles[0], circles[1], circles[2], circles[3]])
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgOut = cv2.warpPerspective(img_wrap, matrix, (width, height))
        cv2.imshow("Out", imgOut)

    k = cv2.waitKey(20) & 0xFF  # stop on ESC
    if k == 27:
        break
