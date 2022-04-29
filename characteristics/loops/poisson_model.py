import numpy as np
import matplotlib.pyplot as plt


def hit_prob(lam, lth, n, espilon):

    k = np.arange(1, n+1)
    h = np.sum(np.exp(-lam*k*lth))
    h *= 2 * np.sinh(lam * espilon)

    return h


def falling_power(x, k):
    """
    Compute the falling power x(x-1)...(x-k)
    """

    if k >= x:
        print("Warning: falling power should be less than the base")
        return falling_power(x, x-1)

    factors = np.arange(x, x-k-1, -1)
    print(factors)

    xfk = np.prod(factors)
    return xfk


def s_prob(k, lam, lth, n, espilon):

    h = hit_prob(lam, lth, n, espilon)
    sinh = 2 * np.sinh(lam * espilon)

    p = 0
    for x in range(1, k+1):
        p += falling_power(k-1, x-1) * (sinh ** x)

    p *= (1-h) * np.exp(-lam*lth*k)
    return p


def s_distri(k_max, lam, lth, n, espilon):

    distri = np.zeros(k_max + 1)

    for k in range(1, k_max+1):
        distri[k] = s_prob(k, lam, lth, n, espilon)

    return distri


# --------------------------------------------------------------------------- #
print(s_distri(20, 1, 1, 5, 0.05))
