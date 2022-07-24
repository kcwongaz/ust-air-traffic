import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm


# --------------------------------------------------------------------------- #
dstr = "20170101_0000-20171231_2359"
case = "all"

datadir = f"/home/kc/Research/air_traffic/data/redirection"
savedir = f"/home/kc/Research/air_traffic/figures/2022-05-12"

mode = "tdiff"

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

# --------------------------------------------------------------------------- #
c = np.loadtxt(f"{datadir}/chain_{case}_{dstr}.txt")
s = np.loadtxt(f"{datadir}/ts_{case}_{dstr}.txt")
t = np.loadtxt(f"{datadir}/timestamp_{case}_{dstr}.txt")
t_ = np.loadtxt(f"{datadir}/entrytime_{case}_{dstr}.txt")

t0 = pd.to_datetime("2017-01-01").timestamp()
t -= t0
t /= 3600

t_ -= t0
t_ /= 3600


# --------------------------------------------------------------------------- #
def count_loops(t, t0, te):
    """
    Count the number of active loops at time t.
    """

    ind = np.where((t0 < t) & (te > t))[0]
    count = len(ind)
    # print(count)

    return count


def extract_by_x(x0, x, y):

    x = np.array(x)
    ind = np.where(x == x0)
    y = y[ind]

    return y


# --------------------------------------------------------------------------- #
fig, ax = plt.subplots()

if mode == "ts":

    # Show only the first month
    # ind = np.where((t < 15*24) & (t > 14*24))
    ind = np.where(t < 30*24)
    t = t[ind]
    s = s[ind]

    markerline, stemlines, baseline = ax.stem(t, s, linefmt="-")
    baseline.set_linewidth(0)
    markerline.set_markersize(2.5)
    markerline.set_color("blue")
    stemlines.set_linewidth(1)
    stemlines.set_color("gray")
    stemlines.set_alpha(0.7)

    plt.show()


elif mode == "sdiff":

    diff = s[1:] - s[:-1]  # s in unit of minutes

    print(len(diff[np.abs(diff) <= 20]) / len(diff))

    # Remove extreme events
    # diff = diff[np.abs(diff) < 100]

    bins = np.arange(-201, 201, 2)
    ax.hist(diff, bins=bins, density=True, color="blue", alpha=0.8,
            label="Data")

    mean, std = norm.fit(diff)
    x = np.linspace(np.min(diff), np.max(diff), 1000)
    y = norm.pdf(x, mean, std)
    ax.plot(x, y, color="red", label="Gaussian Fit")

    print(np.mean(diff))
    print(np.std(diff))
    ax.legend(fontsize=10)
    ax.set_xlabel("$\Delta S$ (min)", fontsize=14)
    ax.set_ylabel("$P(\Delta S)$", fontsize=14)
    ax.set_title("Distribution of Nearest Neighbor Difference in $S$", fontsize=16)
    ax.set_xlim(-100, 100)
    ax.set_xticks(np.arange(-100, 101, 20))
    ax.set_xticklabels(np.arange(-100, 101, 20), fontsize=8)

    ax.annotate(f"Mean = {np.round(mean, 2)} min", (-90, 0.15), fontsize=12)
    ax.annotate(f"SD = {np.round(std, 2)} min", (-90, 0.135), fontsize=12)

    plt.tight_layout()
    plt.savefig(f"{savedir}/hist_sdiff.png", dpi=300)

    plt.show()


elif mode == "tdiff":

    # ind = np.where(t < 30*24)
    # t = t[ind]
    # s = s[ind]

    ind = np.where(s > 0)
    t = t[ind]
    s = s[ind]

    # time in minutes
    t *= 60

    diff = t[1:] - t[:-1]
    print(len(diff[np.abs(diff) <= 10]) / len(diff))

    # Anything greater than 24 hours are noise
    diff = diff[diff < 24*60]

    ax.hist(diff, bins=np.linspace(0, 200, 100), density=True,
            color="blue", alpha=0.8,
            label="Data")

    mean = np.mean(diff)
    std = np.std(diff)

    # ax.set_yscale("log")
    ax.set_xlabel("$\Delta T$ (min)", fontsize=14)
    ax.set_ylabel("$P(\Delta T)$", fontsize=14)
    ax.set_title("Distribution of Distance to Nearest Positive Saved Time", fontsize=14)

    # ax.annotate(f"Mean = {np.round(mean, 2)} min", (200, 0.06), fontsize=14)
    # ax.annotate(f"SD = {np.round(std, 2)} min", (200, 0.055), fontsize=14)

    plt.tight_layout()
    plt.savefig(f"{savedir}/hist_tdiff.png", dpi=300)

    plt.show()


elif mode == "loop":

    loops = [count_loops(s, t_, t) for s in t_]

    ax.plot(loops, s, linestyle="none", marker="o", color="red", alpha=0.1)

    plt.ylabel("Time Saved (min)")
    plt.xlabel("Number of Active Loops")
    plt.show()


elif mode == "loop_violin":

    loops = [count_loops(s, t_, t) for s in t_]

    data = [extract_by_x(i, loops, s) for i in range(16)]
    pos = range(16)

    [print(len(data[i])) for i in range(16)]

    # quantiles = [[0.25, 0.5, 0.75] for i in range(16)]

    vp = ax.violinplot(data, pos, showmeans=True, showextrema=True,
                       points=1000)
    ax.set_xticks(pos)

    ax.set_ylabel("Time Saved (min)", fontsize=14)
    ax.set_xlabel("Number of Active Loops", fontsize=14)

    cmap = plt.get_cmap("viridis")
    for i, b in enumerate(vp["bodies"]):
        b.set_edgecolor("black")
        b.set_facecolor(cmap(i/16))
        b.set_lw(0.5)


    vp["cmeans"].set_color("blue")
    vp["cmaxes"].set(lw=0.5, color="black")
    vp["cmins"].set(lw=0.5, color="black")
    vp["cbars"].set(lw=0.5, color="black")

    ax.plot([], [], color="blue", label="Mean")
    ax.legend()

    plt.savefig(f"{savedir}/s_loop_correlation.png", dpi=300)
    plt.show()


elif mode == "loop_mean":

    loops = [count_loops(s, t_, t) for s in t_]
    data = [extract_by_x(i, loops, s) for i in range(16)]

    means = [np.mean(data[i]) for i in range(16)]
    count = [len(data[i]) for i in range(16)]

    ax.plot(range(16), means, marker="o", color="blue", label="Mean")

    axt = ax.twinx()
    axt.plot(range(16), count, marker="o", color="green")
    ax.plot([], [], marker="o", color="green", label="Data Count")

    ax.set_xlabel("Number of Active Loops", fontsize=14)
    ax.set_ylabel("Mean Saved Time (min)", fontsize=14)
    axt.set_ylabel("Number of Data Point", fontsize=14)

    ax.legend(loc="center left")
    plt.tight_layout()
    plt.savefig(f"{savedir}/s_loop_mean.png", dpi=300)
    plt.show()
