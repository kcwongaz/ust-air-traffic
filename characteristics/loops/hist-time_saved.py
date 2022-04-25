import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from loop_helpers import *


# --------------------------------------------------------------------------- #
# Target datetime range to plot flight on; UTC 16:00 is HKT 00:00
target_start = pd.to_datetime("2017-01-01 00:00", format=r"%Y-%m-%d %H:%M")
target_end = pd.to_datetime("2017-12-31 23:59", format=r"%Y-%m-%d %H:%M")
target_start_str = target_start.strftime(r"%Y%m%d_%H%M")
target_end_str = target_end.strftime(r"%Y%m%d_%H%M")
dstr = f"{target_start_str}-{target_end_str}"

datadir = f"/home/kc/Research/air_traffic/data/redirection"
savedir = f"/home/kc/Research/air_traffic/figures/2022-04-26"

mode = 3

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

savefig = True

# --------------------------------------------------------------------------- #

if mode == 1:
    ts = np.loadtxt(f"{datadir}/ts_all_{dstr}.txt")
    ts = ts[np.nonzero(ts)]

    fig, ax = plt.subplots()

    bins = np.arange(0, 121, 1)
    ax.hist(ts, bins=bins, color="royalblue", rwidth=0.8)
    ax.set_xticks(np.arange(0, 121, 10))

    ax.set_xlabel("Total Time Saved $S$ (min)", fontsize=14)
    ax.set_ylabel("Count")
    ax.set_title("Histogram of Total Time Saved (2017)", fontsize=16)

    print("Max: ", np.max(ts))
    plt.tight_layout()
    if savefig:
        plt.savefig(f"{savedir}/hist_s.png", dpi=300)
    plt.show()


elif mode == 2:
    ts = np.loadtxt(f"{datadir}/ts1_all_{dstr}.txt")
    ts = ts[np.nonzero(ts)]

    fig, ax = plt.subplots()

    bins = np.arange(0, 41, 1)
    ax.hist(ts, bins=bins, color="mediumpurple", rwidth=0.8)
    ax.set_xticks(np.arange(0, 41, 5))

    ax.set_xlabel("First-step Time Saved $S_1$ (min)", fontsize=14)
    ax.set_ylabel("Count")
    ax.set_title("Histogram of First-step Time Saved (2017)", fontsize=16)

    plt.tight_layout()
    if savefig:
        plt.savefig(f"{savedir}/hist_s1.png", dpi=300)
    plt.show()


elif mode == 3:
    ts = np.loadtxt(f"{datadir}/ts_all_{dstr}.txt")
    ts = ts[np.nonzero(ts)]

    fig, ax = plt.subplots()

    bins = np.arange(0, 251, 5)
    centers = (bins[:-1] + bins[1:]) / 2

    hist, _ = np.histogram(ts, bins=bins)

    ind = np.nonzero(hist)
    hist = hist[ind]
    centers = centers[ind]

    ax.plot(centers, hist, marker="o", color="royalblue", lw=1)

    # ax.set_xticks(np.arange(0, 121, 10))
    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlabel("Total Time Saved $S$ (min)", fontsize=14)
    ax.set_ylabel("Count")
    ax.set_title("Histogram of Total Time Saved (2017)", fontsize=16)

    print("Max: ", np.max(ts))
    plt.tight_layout()
    if savefig:
        plt.savefig(f"{savedir}/hist_s_logscale.png", dpi=300)
    plt.show()