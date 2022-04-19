import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# from scipy.stats import binned_statistic


fname = "/home/kc/Research/air_traffic/data/fr24_clean/stat_145-165_history.txt"
savedir = "/home/kc/Research/air_traffic/figures/2022-03-15"

year = 2021
n_cluster = 5

bins = np.arange(0, 25, 1)

c_names = ["Southeast", "North", "Southwest", "East", "Northwest"]

stat_name = "mean"
lag = 15
color = "blue"

savefig = True
showfig = True

# --------------------------------------------------------------------------- #
df = pd.read_csv(fname)
df["year"] = pd.to_datetime(df["t_i"], unit="s").dt.year
df = df.loc[df["year"] == year]
df = df.loc[df[f"{stat_name}_{lag}_min"] > 0]   # Information-less points

# Remove point from mid-nights; those have different statistics
df = df.loc[(df["t_i"] + 8*3600) % 86400 > 9*3600]
# df = df.loc[(df["t_i"] + 8*3600) % 86400 < 21*3600]


# HKT is UTC+8
datetimes = pd.to_datetime(df["t_i"] + 8*3600, unit="s")
cluster = df["cluster"].to_numpy()

# Use unit of minutes
delta_t = df["delta_t_sec"].to_numpy() / 60
stat = df[f"{stat_name}_{lag}_min"].to_numpy() / 60


# --------------------------------------------------------------------------- #
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))

for ij in range(6):
    ax = axs[ij // 3, ij % 3]

    # First figure contain all clusters
    if ij == 0:
        y = delta_t
        x = stat
        alpha = 0.015

        r = np.around(np.corrcoef(x, y)[0, 1], 4)

        ax.set_title(f"All; $r={r}$", fontsize=12)
        ax.set_ylabel("Transit time (min)", fontsize=12)

    # Then do one cluster per subplot
    else:
        index = np.where(cluster == ij - 1)
        y = delta_t[index]
        x = stat[index]
        alpha = 0.05

        r = np.round(np.corrcoef(x, y)[0, 1], 4)

        ax.set_title(f"{c_names[ij-1]}; $r={r}$", fontsize=12)

    ax.scatter(x, y, s=5, c=color, alpha=alpha)

    # x-axis label
    if ij == 4:
        ax.set_xlabel(f"Mean transit time in past {lag} min (min)", fontsize=12)

plt.tight_layout()
if savefig:
    plt.savefig(f"{savedir}/history_{stat_name}{lag}_{year}.png", dpi=300)

if showfig:
    plt.show()
