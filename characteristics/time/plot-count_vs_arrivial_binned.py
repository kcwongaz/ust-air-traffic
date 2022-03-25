import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import binned_statistic


fname = "/home/kc/Research/air_traffic/data/fr24_clean/stat_145-165_clustered.txt"
savedir = "/home/kc/Research/air_traffic/figures/2022-03-22"

year = 2017
n_cluster = 5

bins = np.arange(0, 24.1, 0.25)


statistic = "mean"

savefig = True
showfig = True

# --------------------------------------------------------------------------- #
df = pd.read_csv(fname)
df["year"] = pd.to_datetime(df["t_i"], unit="s").dt.year
df = df.loc[df["year"] == year]


# HKT is UTC+8
datetimes = pd.to_datetime(df["t_i"] + 8*3600, unit="s")
dow = datetimes.dt.day_of_week.to_numpy()  # Monday is 0, Sunday is 6

# Entry times
second = (df["t_i"].to_numpy() + 8*3600) % 86400
hour = second / 3600
delta_t = df["delta_t_sec"].to_numpy() / 60

# Arrivial times
second_f = (df["t_f"].to_numpy() + 8*3600) % 86400
hour_f = second_f / 3600


# --------------------------------------------------------------------------- #
fig, ax = plt.subplots()

count0, edges0, _ = binned_statistic(hour, delta_t, statistic="count",
                                     bins=bins)
count1, edges1, _ = binned_statistic(hour_f, delta_t, statistic="count",
                                     bins=bins)

centers0 = (edges0[:-1] + edges0[1:]) / 2
centers1 = (edges1[:-1] + edges1[1:]) / 2

ax.plot(centers0, count0, marker="o", markersize=2.5, lw=1.0,
        color="green", alpha=1.0, label="Entry")

ax.plot(centers1, count1, marker="o", markersize=2.5, lw=1.0,
        color="deeppink", alpha=1.0, label="Landing")


ax.set_xlabel("Time since 00:00 HKT (hr)", fontsize=14)
ax.set_ylabel("15-min-binned count", fontsize=14)
ax.legend()


ax.set_xticks(np.arange(0, 25, 2))

plt.tight_layout()
if savefig:
    plt.savefig(f"{savedir}/arrivial_vs_count_{year}.png", dpi=300)

if showfig:
    plt.show()
