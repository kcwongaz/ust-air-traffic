import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from loop_helpers import *


# --------------------------------------------------------------------------- #
# Target datetime range to plot flight on; UTC 16:00 is HKT 00:00
target_start = pd.to_datetime("2018-01-01 00:00", format=r"%Y-%m-%d %H:%M")
target_end = pd.to_datetime("2018-12-31 23:59", format=r"%Y-%m-%d %H:%M")
target_start_str = target_start.strftime(r"%Y%m%d_%H%M")
target_end_str = target_end.strftime(r"%Y%m%d_%H%M")
dstr = f"{target_start_str}-{target_end_str}"

datadir = f"/home/kc/Research/air_traffic/data/redirection"
savedir = f"/home/kc/Research/air_traffic/figures/2022-04-26"
mode = 2

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

savefig = False


# --------------------------------------------------------------------------- #

chain = np.loadtxt(f"{datadir}/chain_all_{dstr}.txt")

fig, ax = plt.subplots()


edges = np.arange(-0.5, 16, 1)
centers = (edges[:-1] + edges[1:]) / 2

hist, _ = np.histogram(chain, bins=edges)
print(hist)
print(sum(hist))


# --------------------------------------------------------------------------- #
if mode == 1:
    ax.bar(centers, hist, color="darkorange")
    ax.set_xticks(centers)

    for rect in ax.patches:
        height = rect.get_height()
        ax.annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width()/2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom', fontsize=8, color="darkorange")

    # ax.set_ylim(0, 3500)
    ax.set_xlabel("Length of Redirection Chain", fontsize=14)
    ax.set_ylabel("Count", fontsize=14)

    ax.set_title("Histogram of Redirection Chains (2017)", fontsize=16)

    plt.tight_layout()

    if savefig:
        plt.savefig(f"{savedir}/hist_chains.png", dpi=300)
    plt.show()


# --------------------------------------------------------------------------- #
elif mode == 2:

    hist[1:-1] = hist[1:-1] - hist[2:]
    print(np.sum(np.arange(len(hist)) * hist))

    ax.bar(centers, hist, color="salmon")
    ax.set_xticks(centers)

    for rect in ax.patches:
        height = rect.get_height()
        ax.annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width()/2, height),
                    xytext=(0, 3), textcoords='offset points',
                    ha='center', va='bottom', fontsize=8, color="salmon")

    # ax.set_ylim(0, 3500)
    ax.set_xlabel("Length of Redirection Chain", fontsize=14)
    ax.set_ylabel("Count", fontsize=14)

    ax.set_title("Histogram of Unqiue Chains (2017)", fontsize=16)

    plt.tight_layout()
    if savefig:
        plt.savefig(f"{savedir}/hist_unqiue_chains.png", dpi=300)
    plt.show()
