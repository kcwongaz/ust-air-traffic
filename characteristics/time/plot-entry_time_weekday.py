import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import binned_statistic


fname = "/home/kc/Research/air_traffic/data/fr24_clean/stat_145-165_clustered.txt"
savedir = "/home/kc/Research/air_traffic/figures/2022-03-15"

year = 2021
n_cluster = 5

bins = np.arange(0, 25, 1)

c_names = ["Southeast", "North", "Southwest", "East", "Northwest"]
dow_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
dow_colors = ["blue", "darkviolet", "green", "darkorange", "teal",
              "deeppink", "red"]

statistic = "mean"
savefig = True
showfig = False

# --------------------------------------------------------------------------- #
df = pd.read_csv(fname)
df["year"] = pd.to_datetime(df["t_i"], unit="s").dt.year
df = df.loc[df["year"] == year]


# HKT is UTC+8
datetimes = pd.to_datetime(df["t_i"] + 8*3600, unit="s")
dow = datetimes.dt.day_of_week.to_numpy()  # Monday is 0, Sunday is 6

second = (df["t_i"].to_numpy() + 8*3600) % 86400
hour = second / 3600
delta_t = df["delta_t_sec"].to_numpy() / 60
cluster = df["cluster"].to_numpy()


# --------------------------------------------------------------------------- #
fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))

for ij in range(6):
    ax = axs[ij // 3, ij % 3]

    # First figure contain all clusters
    if ij == 0:
        dow0 = dow
        hour0 = hour
        dt0 = delta_t

        ax.set_title(f"All ({len(dt0)})", fontsize=12)

    # Then do one cluster per subplot
    else:
        index = np.where(cluster == ij - 1)
        dow0 = dow[index]
        hour0 = hour[index]
        dt0 = delta_t[index]

        ax.set_title(f"{c_names[ij-1]} ({len(dt0)})", fontsize=12)

    # Plot the days of week one-by-one
    for k in range(7):
        index = np.where(dow0 == k)
        hour1 = hour0[index]
        dt1 = dt0[index]

        mean, edges, _ = binned_statistic(hour1, dt1, statistic=statistic,
                                          bins=bins)

        centers = (edges[:-1] + edges[1:]) / 2
        ax.plot(centers, mean, marker="o", markersize=1.5, lw=0.75,
                color=dow_colors[k], alpha=0.8)

    # Curve labels and y-axis label
    if ij == 0:
        for k in range(7):
            ax.plot([], [], marker="o", markersize=1.5, lw=0.75,
                    color=dow_colors[k], label=dow_names[k])

        ax.legend(fontsize=8)

        ax.set_ylabel("Hourly average transit time (min)", fontsize=12)

    # x-axis label
    if ij == 4:
        ax.set_xlabel("Entry time (Hour from 00:00 HKT)", fontsize=12)

plt.tight_layout()
if savefig:
    plt.savefig(f"{savedir}/entrytime_weekday_{statistic}_{year}.png", dpi=300)

if showfig:
    plt.show()
