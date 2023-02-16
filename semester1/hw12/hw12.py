import numpy as np
import cv2 as cv
import glob
from matplotlib import pyplot as plt

# chessboardSize = (9, 9)
# frameSize = (1280, 960)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7, 3), np.float32)
objp[:,:2] = np.mgrid[0:7,  0:6].T.reshape(-1,2)


size_of_chessboard_squares_mm = 20
objp = objp * size_of_chessboard_squares_mm

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

images = glob.glob('*.png')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (7, 6), None)

    # If found, add object points, image points (after refining them)
    if ret:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (7, 6), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(500)
cv.destroyAllWindows()

############## CALIBRATION #######################################################
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

############## UNDISTORTION #####################################################

img = cv.imread('objectOnBoard.png')
h, w = img.shape[:2]
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# Undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
#cv.imwrite('results/calibresult.png', dst)

# Undistort with Remapping
mapx, mapy = cv.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

# crop the image
x, y, w, h = roi
dst = dst[y:y + h, x:x + w]
#cv.imwrite('results/caliResult2.png', dst)

# CoinDetect

# blur to optimise edge finding
coins_blurred = cv.GaussianBlur(dst, (5, 5), cv.BORDER_DEFAULT)
#cv.imwrite("results/coins_blurred.png", coins_blurred)

thresh = 75
maxValue = 76

th, threshInv = cv.threshold(coins_blurred, thresh, maxValue, cv.THRESH_BINARY)
# Cany
canny = cv.Canny(threshInv, 0, 255)
kernel = np.ones((3, 3), 'uint8')
dilate = cv.dilate(canny, kernel=kernel, iterations=1)
erosion = cv.erode(dilate, kernel=kernel, iterations=1)
plt.subplot(221), plt.imshow(img, cmap = 'gray')
plt.subplot(222), plt.imshow(canny, cmap = 'gray')
plt.subplot(223), plt.imshow(dilate, cmap = 'gray')
plt.subplot(224), plt.imshow(erosion, cmap = 'gray')
plt.show()

# Reprojection Error
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error
print( "total error: {}".format(mean_error/len(objpoints)) )
