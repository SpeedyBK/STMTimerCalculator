# This is a sample Python script.
from typing import NamedTuple
# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


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


err_list = list()

for i in range(1, 100):
    for j in range(1, 100):
        err_list.append(calc_error(i, j, 120000000, 1024000))

pos_neg_err = sort_pos_neg(err_list)
print(pos_neg_err.neg)
print(pos_neg_err.pos)

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

