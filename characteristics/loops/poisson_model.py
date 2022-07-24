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

    Note that falling_power(x, 0) = 1 following standard definition.
    A falling power of k should contain exactly k factors
    """

    if k > x:
        print("Warning: falling power should be less than the base")
        return falling_power(x, x-1)

    factors = np.arange(x, x-k, -1)
    # print(factors)

    xfk = np.prod(factors)
    return xfk


def pi_x(k, x, lam, lth, n, espilon):
    h = hit_prob(lam, lth, n, espilon)
    sinh = 2 * np.sinh(lam * espilon)

    p = ((sinh/h)**x) * np.exp(-lam*lth*k) * falling_power(k-1, x-1) \
        / np.math.factorial(x-1)
    return p


def pi_2(k, x, lam, lth, n, espilon):
    h = hit_prob(lam, lth, n, espilon)
    sinh = 2 * np.sinh(lam * espilon)

    p = ((sinh/h)**2) * np.exp(-lam*lth*k) * (k-1)
    return p


def s_prob(k, lam, lth, n, espilon):

    h = hit_prob(lam, lth, n, espilon)
    sinh = 2 * np.sinh(lam * espilon)

    p = 0
    for x in range(1, k+1):
        p += falling_power(k-1, x-1) * (sinh ** x) / np.math.factorial(x-1)

    p *= (1-h) / h * np.exp(-lam*lth*k)
    return p


def s_distri(k_max, lam, lth, n, espilon):

    distri = np.zeros(k_max + 1)
    # distri[0] = 1 - hit_prob(lam, lth, n, epsilon)

    for k in range(1, k_max+1):
        distri[k] = s_prob(k, lam, lth, n, espilon)

    return distri


def chain_distri(x_max, lam, lth, n, espilon):

    # h = hit_prob(lam, lth, n, espilon)
    h = 0.5
    x = np.arange(0, x_max+1)
    distri = np.power(h, x) * (1-h)

    return distri

# --------------------------------------------------------------------------- #
# print(s_distri(100, 1, 1, 5, 0.05))

lth = 1
n = 15
lam = 1 / (lth * n)
# lam = 

espilon = 0.25
k_max = 5*n

print(hit_prob(lam, lth, n, espilon))
ps = s_distri(k_max, lam, lth, n, espilon)
print(np.sum(ps))

ps /= np.sum(ps)

ps_first = 2*np.sinh(lam*espilon) * np.exp(-lam*np.arange(n+1)*lth)


# x = 2
# pi = np.zeros(x*n)
# for k in range(1, x*n):
#     pi[k] = pi_2(k, 2, lam, lth, n, espilon)

# print(np.sum(pi))


plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

fig, ax = plt.subplots()

# --------------------------------------------------------------------------- #
# t_axis = np.arange(0, k_max+1) * lth
# ax.bar(t_axis, ps, color="hotpink")
# ax.set_xlabel("Total time Saved in unit of loop length $l$", fontsize=14)
# ax.set_ylabel("Probability", fontsize=14)

# plt.tight_layout()

# plt.savefig("/home/kc/Research/air_traffic/figures/2022-05-03/ps.png", dpi=300)
# plt.show()

# --------------------------------------------------------------------------- #
# t_axis = np.arange(0, n+1) * lth
# ax.bar(t_axis, ps_first, color="hotpink")
# ax.set_xlabel("Total time Saved in unit of loop length $l$", fontsize=14)
# ax.set_ylabel("Probability", fontsize=14)

# plt.tight_layout()

# plt.savefig("/home/kc/Research/air_traffic/figures/2022-05-03/ps1.png", dpi=300)
# plt.show()

# --------------------------------------------------------------------------- #

x_max = 15
x_axis = np.arange(0, x_max+1)
px = chain_distri(x_max, lam, lth, n, espilon)

ax.bar(x_axis, px, color="lightseagreen")


ax.set_xlabel("Chain Length", fontsize=14)
ax.set_ylabel("Probability", fontsize=14)

plt.tight_layout()

plt.savefig("/home/kc/Research/air_traffic/figures/2022-05-03/px.png", dpi=300)
plt.show()
