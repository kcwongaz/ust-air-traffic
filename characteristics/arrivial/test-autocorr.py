import numpy as np
import matplotlib.pyplot as plt

from arrivial_rate import autocorr_period, autocorr


def test_autocorr_period():

    # Autocorrelation computed by autocorr()
    dt = 1
    period = 100
    t = np.arange(0, 100000+dt, dt)
    s = np.sin(2*np.pi / period * t)
    a = autocorr_period(s, dt, period=period)

    # Autocorrelation computed analytically
    t1 = np.arange(0, period+dt, dt)
    s1 = np.sin(2*np.pi / period * t1)

    # This is just A(t, T) = sin(wt)*sin(w(t+T))
    n = round(period / dt)
    a1 = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            a1[i, j] = s1[i] * s1[(i+j) % n]

    # Check 1: Compute difference
    print("Absolute difference summed: ", np.sum(np.abs(a - a1)))
    print("Maximum difference", np.max(np.abs(a - a1)))

    # Check 2: Compute the heat map
    fig, axs = plt.subplots(ncols=2, figsize=(8, 8))

    ax1 = axs[0]
    ax1.imshow(a, cmap="plasma", extent=(0, period, 0, period), origin="lower",
               vmin=-1, vmax=1)

    ax2 = axs[1]
    ax2.imshow(a1, cmap="plasma", extent=(0, period, 0, period), origin="lower",
               vmin=-1, vmax=1)

    plt.tight_layout()
    plt.show()


def test_autocorr():

    # Autocorrelation computed of X(t) = sin(wt) by autocorr()
    dt = 1
    period = 100
    t = np.arange(0, 100*period+dt, dt)
    s = np.sin(2*np.pi / period * t)
    a = autocorr(s, dt, lag_max=5*period)

    # Autocorrelation computed analytically, given by A(tau) = cos (w*tau)
    t1 = np.arange(0, 5*period+dt, dt)
    a1 = np.cos(2*np.pi / period * t1)

    # Check 1: Compute difference
    print("Absolute difference summed: ", np.sum(np.abs(a - a1)))
    print("Maximum difference", np.max(np.abs(a - a1)))

    # Check 2: Compute the heat map
    fig, ax = plt.subplots()
    ax.plot(t1, a, color="blue")
    ax.plot(t1, a1, color="green")

    plt.tight_layout()
    plt.show()


test_autocorr()
