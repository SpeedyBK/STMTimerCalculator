# This is a sample Python script.
from typing import NamedTuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np


class ErrorClass(NamedTuple):
    neg: list
    pos: list


def calc_error(psc, cp, clock_freq, target_freq):
    target_time = 1/target_freq
    timer_periode = (psc * cp) / clock_freq

    error = target_time - timer_periode

    return [error, psc, cp]


def sort_pos_neg(data):
    err = ErrorClass(list(), list())
    for d in data:
        if d[0] >= 0:
            err.pos.append(d)
        else:
            err.neg.append(d)

    return err


def find_min_max(data=ErrorClass(list(), list())):
    pos_min = [10000, 0, 0]
    neg_max = [-10000, 0, 0]
    for p in data.pos:
        if p[0] < pos_min[0]:
            pos_min = p
    for n in data.neg:
        if n[0] > neg_max[0]:
            neg_max = n

    return [pos_min, neg_max]


def plot_error(a, b, data=ErrorClass(list(), list())):
    error = list()
    psc = list()
    counter = list()

    for errP in data.pos:
        error.append(errP[0]*1000)
        psc.append(errP[1])
        counter.append(errP[2])

    for errN in data.neg:
        error.append(errN[0]*1000)
        psc.append(errN[1])
        counter.append(errN[2])

    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection='3d')
    xx, yy = np.meshgrid(range(b-a), range(b-a))
    ax.plot_surface(xx+a, yy+a, (yy - yy - 0), alpha=0.7, color='green')
    ymax = (1 / 512000 * 120000000) / b
    linesp = np.linspace(ymax, b, 1000)
    yline = (1/512000 * 120000000) / linesp
    ax.plot3D(linesp, yline, 0, 'red')

    fig = ax.scatter3D(psc, counter, error)

    ax.set_xlabel('PSC')
    ax.set_ylabel('Counter')
    ax.set_zlabel('Error')
    # ax.set_zlim(-0.01, 0.01)

    plt.show()


err_list = list()

a = 0
b = 25

for i in range(a, b):
    for j in range(a, b):
        err_list.append(calc_error(i, j, 120000000, 512000))

pos_neg_err = sort_pos_neg(err_list)

min_max = find_min_max(pos_neg_err)

if min_max[0][0] == 10000:
    print("*******************************")
    print("No positiv Error")
    print("-------------------------------")
    print("Error =", min_max[1][0])
    print("Prescaler =", min_max[1][1])
    print("Counter Value =", min_max[1][2])
    print("*******************************")
elif min_max[1][0] == -10000:
    print("*******************************")
    print("No negative Error")
    print("-------------------------------")
    print("Error =", min_max[0][0])
    print("Prescaler =", min_max[0][1])
    print("Counter Value =", min_max[0][2])
    print("*******************************")
else:
    print("*******************************")
    print("Error =", min_max[0][0])
    print("Prescaler =", min_max[0][1])
    print("Counter Value =", min_max[0][2])
    print("-------------------------------")
    print("Error =", min_max[1][0])
    print("Prescaler =", min_max[1][1])
    print("Counter Value =", min_max[1][2])
    print("*******************************")

plot_error(a, b, pos_neg_err)
