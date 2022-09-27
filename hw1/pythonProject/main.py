import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde
import seaborn as sns  # Seaborn is a library for making statistical graphics in Python
from sklearn.neighbors import KernelDensity


def kde(x):
    eval_points = np.linspace(np.min(x), np.max(x))  # returns evenly spaced numbers over a specified interval
    # раввномерно распределенные числа на указанном интервале

    kde_sk = KernelDensity(bandwidth=1.0, kernel='gaussian')  # Kernel Density Estimation with the default bandwidth=1.0
    kde_sk.fit(x.reshape([-1, 1]))  # Fits the Kernel Density model on the data
    y_sk = np.exp(
        kde_sk.score_samples(eval_points.reshape(-1, 1)))  # Calculates exponential of all elements in the input array

    kde_sp = gaussian_kde(x,
                          bw_method=1.0)  # estimates the probability density function (PDF) of a random variable in a non-parametric way
    y_sp = kde_sp.pdf(eval_points)  # evaluates the estimated pdf on a provided set of points

    sns.kdeplot(x)
    plt.plot(eval_points, y_sk)
    plt.plot(eval_points, y_sp)
    plt.legend(['seaborn rawdata', 'scikit KernelDensity', 'scipy gaussian_kde'])
    plt.show()


def task1():
    n = 500000
    dist_frac = 0.1

    x1 = np.random.normal(-5, 2, int(n * dist_frac))  # 1st distribution with mu=-5, sigma=2
    x2 = np.random.normal(5, 3, int(n * (1 - dist_frac)))  # 2nd distribution with mu= 5, sigma=3

    x = np.concatenate((x1, x2))  # concatinate x1 and x2 in one array, where x1 : x2 relation is 1:9
    np.random.shuffle(x)  # shuffling the content of x array to change the input values sequence
    kde(x)

    #
    samples = np.reshape(x, (5000, 100))
    mean_samples = np.array([np.mean(x) for x in samples])
    kde(mean_samples)
    plt.hist(mean_samples, bins=100, color="purple")
    plt.show()


def task2():
    plt.style.use('seaborn-poster')
    # generate x and y
    x = np.linspace(0, 1, 101)
    y = datetime.datetime.now().second + x**3 + x * np.random.random(len(x))

    # assemble matrix A
    # объединение подмассивов в матрицу
    # np.ones создает одномерный массив из единиц
    A = np.vstack([x, np.ones(len(x))]).T

    # turn y into a column vector
    # преобразование в одномерную матрицу [[1.], [1.01358]...]
    y = y[:, np.newaxis]

    # Direct least square regression
    # np.dot - скалярное произведение векторов
    alpha = np.dot((np.dot(np.linalg.inv(np.dot(A.T, A)), A.T)), y)
    print(alpha)
    print(np.linalg.lstsq(A, y, rcond=None)[0])

    # plot the results
    plt.figure(figsize=(10, 8))
    plt.plot(x, y, 'b.')
    plt.plot(x, alpha[0] * x**3 + alpha[1], 'r')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


if __name__ == '__main__':
    task2()
