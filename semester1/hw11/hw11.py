import cv2
import numpy as np
from random import random
import matplotlib.pyplot as plt


def add_salt_pepper_noise(img, probability):
    output = np.zeros(img.shape, np.uint8)
    h, w = img.shape[:2]
    for i in range(h):
        for j in range(w):
            rnd = random()
            prob = probability / 2.0
            inverse_prob = 1 - prob
            output[i, j] = 255 if rnd < prob else 0 if rnd > inverse_prob else img[i, j]
    return output


def median_blur(img, kernel_size):
    return cv2.medianBlur(img, kernel_size)


def gaussian_blur(img, kernel_size):
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), sigmaX=0, sigmaY=0)


def bilateral_filter(img, kernel_size, sigma_color, sigma_space):
    return cv2.bilateralFilter(img, kernel_size, sigma_color, sigma_space)


# frequency filters
def mean_filter(img, kernel_size):
    return cv2.blur(img, (kernel_size, kernel_size))


def mag_spectrum(img):
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    return 20 * np.log(np.abs(fshift))


noise = 0
img = cv2.imread('home.jpg')
window_name = 'Noisy photo'


def on_slide(value):
    global noise
    print(value)
    noise = value
    salted = add_salt_pepper_noise(img, float(noise) / 100.0)
    cv2.imshow(window_name, salted)
    plt.imshow(mag_spectrum(cv2.imread('home.jpg', 0)), cmap='gray')
    plt.show()
    cv2.waitKey(1)


while True:
    salted = add_salt_pepper_noise(img, float(noise) / 100.0)
    cv2.imshow(window_name, salted)
    cv2.createTrackbar('Noise gain', window_name, noise, 100, on_slide)
    k = cv2.waitKey(0)
    if k == 27:
        break
cv2.destroyAllWindows()
