# Little commandline calculator to find optimal settings for STM32 timers.
# Author: Benjamin Lagershausen-Keßler (BLagershausen@uni-kassel.de)
# All rights reserved.

from typing import NamedTuple
import matplotlib.pyplot as plt
import numpy as np

# Parsing command line arguments:
import argparse


def parse_cmd_line():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--lb', metavar='a', dest='a_in', type=int, required=True,
                        help='lower boundry for psc and counter values')
    parser.add_argument('--ub', metavar='b', dest='b_in', type=int, required=True,
                        help='upper boundry for psc and counter values')
    parser.add_argument('--baseclock', metavar='baseclock', dest='bc_in', type=int, required=True,
                        help='base timer clock frequency')
    parser.add_argument('--targetfreq', metavar='targetfrq', dest='tf_in', type=int, required=True,
                        help='1/targetfreq will be the counting periode of your timer')

    args = parser.parse_args()
    print("Lower Boundry: ", args.a_in)
    print("Upper Boundry: ", args.b_in)
    print("Baseclock: ", args.bc_in)
    print("Target Frequency: ", args.tf_in)

    return [args.a_in, args.b_in, args.bc_in, args.tf_in]


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


def plot_error(a_val, b_val, baseclock_, targetfrq_, data=ErrorClass(list(), list())):
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
    xx, yy = np.meshgrid(range(b_val-a_val), range(b_val-a_val))
    ax.plot_surface(xx+a_val, yy+a_val, (yy - yy - 0), alpha=0.7, color='green')
    ymax = (1 / targetfrq_ * baseclock_) / b_val
    linesp = np.linspace(ymax, b_val, 1000)
    yline = (1/targetfrq_ * baseclock_) / linesp
    ax.plot3D(linesp, yline, 0, 'red')

    ax.scatter3D(psc, counter, error)

    ax.set_xlabel('PSC')
    ax.set_ylabel('Counter')
    ax.set_zlabel('Error')

    plt.show()


# Main Script:
inputs = parse_cmd_line()

err_list = list()

a = inputs[0]
b = inputs[1]
baseclock = inputs[2]
targetfrq = inputs[3]

for i in range(a, b):
    for j in range(a, b):
        err_list.append(calc_error(i, j, baseclock, targetfrq))

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

if a - b > -1000:
    plot_error(a, b, baseclock, targetfrq, pos_neg_err)
else:
    print("lb/ub difference is to large for plotting! Max value for plotting is lb - ub = -1000.")
