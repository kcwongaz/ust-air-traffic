import numpy as np
import matplotlib.pyplot as plt

from loop_helpers import *


def test_find_minima_spacetime():

    t = np.arange(100)
    x = np.sin(t * 2*np.pi / 5)
    loop_loc = (-5, 5)

    min_dist, min_time = find_minima_spacetime(x, t, loop_loc)

    fig, ax = plt.subplots()
    ax.plot(t, x, color="black")
    ax.plot(min_time, min_dist, color="red", marker="o", linestyle="none")
    plt.show()


def test_find_exitpoint():

    t1 = np.arange(0, 10, 0.01)
    t2 = np.arange(10, 20, 0.01)
    t3 = np.arange(20, 30, 0.01)

    loop_loc = (-5, 5)

    x1 = 10 - t1
    x2 = np.sin(t2 * 2*np.pi / 2)
    x3 = 20 - t3

    t = np.concatenate((t1, t2, t3))
    x = np.concatenate((x1, x2, x3))

    min_dist, min_time = find_minima_spacetime(x, t, loop_loc)
    exit_dist, exit_time = find_exitpoint(x, t, loop_loc)

    fig, ax = plt.subplots()
    ax.plot(t, x, color="black")
    ax.plot(min_time, min_dist, color="red", marker="o", linestyle="none")
    ax.plot([exit_time], [exit_dist], color="blue", marker="o", linestyle="none")
    plt.show()



test_find_minima_spacetime()
# test_find_exitpoint()
