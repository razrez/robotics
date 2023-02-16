import colorsys
import tkinter as tk

import cv2
import numpy as np

image_hsv = None
pixel = (0, 0, 0)  # RANDOM DEFAULT VALUE


def check_boundaries(value, tolerance, ranges, upper_or_lower):
    if ranges == 0:
        # set the boundary for hue
        boundary = 180
    elif ranges == 1:
        # set the boundary for saturation and value
        boundary = 255

    if (value + tolerance > boundary):
        value = boundary
    elif (value - tolerance < 0):
        value = 0
    else:
        if upper_or_lower == 1:
            value = value + tolerance
        else:
            value = value - tolerance
    return value


def rgb2lab(inputColor):
    num = 0
    RGB = [0, 0, 0]

    for value in inputColor:
        value = float(value) / 255

        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0, ]

    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    XYZ[0] = float(XYZ[0]) / 95.047  # ref_X =  95.047   Observer= 2°, Illuminant= D65
    XYZ[1] = float(XYZ[1]) / 100.0  # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883  # ref_Z = 108.883

    num = 0
    for value in XYZ:

        if value > 0.008856:
            value = value ** (0.3333333333333333)
        else:
            value = (7.787 * value) + (16 / 116)

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])

    Lab[0] = round(L, 4)
    Lab[1] = round(a, 4)
    Lab[2] = round(b, 4)

    return Lab


def rgb2ycbcr(r, g, b):
    # Y
    y = .299 * r + .587 * g + .114 * b
    # Cb
    cb = 128 - .169 * r - .331 * g + .5 * b
    # Cr
    cr = 128 + .5 * r - .419 * g - .081 * b
    return y, cb, cr


def pick_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y, x]

        # HUE, SATURATION, AND VALUE (BRIGHTNESS) RANGES. TOLERANCE COULD BE ADJUSTED.
        # Set range = 0 for hue and range = 1 for saturation and brightness
        # set upper_or_lower = 1 for upper and upper_or_lower = 0 for lower
        hue_upper = check_boundaries(pixel[0], 10, 0, 1)
        hue_lower = check_boundaries(pixel[0], 10, 0, 0)
        saturation_upper = check_boundaries(pixel[1], 10, 1, 1)
        saturation_lower = check_boundaries(pixel[1], 10, 1, 0)
        value_upper = check_boundaries(pixel[2], 40, 1, 1)
        value_lower = check_boundaries(pixel[2], 40, 1, 0)

        upper = np.array([hue_upper, saturation_upper, value_upper])
        lower = np.array([hue_lower, saturation_lower, value_lower])
        print(lower, upper)

        # A MONOCHROME MASK FOR GETTING A BETTER VISION OVER THE COLORS
        image_mask = cv2.inRange(image_hsv, lower, upper)
        cv2.imshow("Mask", image_mask)

        # normalize
        (h, s, v) = (hue_upper / 255, saturation_upper / 255, value_upper / 179)
        # convert to RGB
        (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
        # expand RGB range
        (r, g, b) = (int(r * 255), int(g * 255), int(b * 255))

        print('HSV invetred into RGB:', (r, g, b))
        print('HSV invetred into LAB:', rgb2lab([r,g,b]))
        print('HSV invetred into LAB:', rgb2ycbcr(r,g,b))


def main():
    global image_hsv, pixel

    # OPEN DIALOG FOR READING THE IMAGE FILE
    root = tk.Tk()
    root.withdraw()  # HIDE THE TKINTER GUI
    # file_path = filedialog.askopenfilename(filetypes = ftypes)
    root.update()
    image_src = cv2.imread('hue_circle.png')
    image_bgr = cv2.cvtColor(image_src, cv2.COLOR_RGB2BGR)
    cv2.imshow("BGR", image_bgr)

    # CREATE THE HSV FROM THE BGR IMAGE
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV", image_hsv)

    # CALLBACK FUNCTION
    cv2.setMouseCallback("HSV", pick_color)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
