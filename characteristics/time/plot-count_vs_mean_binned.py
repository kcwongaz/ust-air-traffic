import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import binned_statistic


fname = "/home/kc/Research/air_traffic/data/fr24_clean/stat_145-165_clustered.txt"
savedir = "/home/kc/Research/air_traffic/figures/2022-03-22"

year = 2018
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

mean, edges, _ = binned_statistic(hour, delta_t, statistic=statistic,
                                  bins=bins)
count, _, _ = binned_statistic(hour, delta_t, statistic="count",
                               bins=bins)

centers = (edges[:-1] + edges[1:]) / 2
ax.plot(centers, mean, marker="o", markersize=2.5, lw=1.0,
        color="black", alpha=1.0)

axt = ax.twinx()
axt.plot(centers, count, marker="o", markersize=2.5, lw=1.0,
         color="green", alpha=1.0)


ax.set_ylabel("15-min-averaged transit time (min)", fontsize=14)
axt.set_ylabel("15-min-binned arrival count", fontsize=14, color="green")
axt.tick_params(axis="y", labelcolor="green")
ax.set_xlabel("Time since 00:00 HKT (hr)", fontsize=14)

ax.set_xticks(np.arange(0, 25, 2))

plt.tight_layout()
if savefig:
    plt.savefig(f"{savedir}/{statistic}_vs_count_{year}.png", dpi=300)

if showfig:
    plt.show()
