import matplotlib.pyplot as plt
import cv2 as cv2


if __name__ == '__main__':
    pic = cv2.imread('spiral_galaxy.jpg')
    resizeScale = 0.25

    # resize and show
    img = cv2.resize(pic, None, fx=resizeScale, fy=resizeScale, interpolation=cv2.INTER_LINEAR)
    cv2.imshow('', img)
    cv2.waitKey()

    # height / 3, width / 2, number of channels
    height, width, channelsN = img.shape
    print(height, width, channelsN)

    h0 = w0 = 1
    picCounter = 1
    h_interval = height // 3
    w_interval = width // 3

    # let's cropp
    for h in range(h_interval-1, height-1, h_interval):
        w0 = 1
        for w in range(w_interval-1, width-1, w_interval):
            print(h0,h,w0,w)
            cropped_pic = img[h0:h, w0:w]
            cv2.imwrite(f"cropped_picture/Cropped Image{picCounter}.jpg", cropped_pic)
            w0 = w
            picCounter += 1
        h0 = h

