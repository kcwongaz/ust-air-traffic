import numpy as np
import matplotlib.pyplot as plt

from detrend import seasonal_difference


def test_seasonal_difference():

    dt = 1
    period = 100
    t = np.arange(0, 10*period + dt, dt)
    x = np.sin(2*np.pi / period * t + 5)

    detrended = seasonal_difference(x, dt, period)
    print(np.sum(np.abs(detrended)))

    fig, ax = plt.subplots()
    ax.plot(t, x, color="blue")
    ax.plot(dt*np.arange(len(detrended)) + period, detrended, color="red")
    plt.show()


test_seasonal_difference()
