import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import binned_statistic


fname = "/home/kc/Research/air_traffic/data/fr24_clean/stat_145-165_clustered.txt"
savedir = "/home/kc/Research/air_traffic/figures/2022-03-22"

year = 2017
n_cluster = 5

window = 0.25
bins = np.arange(0, 24.1, window)

statistic = "mean"
savefig = False
showfig = True

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


mean, edges, _ = binned_statistic(hour, delta_t, statistic=statistic,
                                  bins=bins)
centers = (edges[:-1] + edges[1:]) / 2

spectrum = np.abs(np.fft.rfft(mean))
spectrum /= np.max(spectrum)
freq = np.fft.rfftfreq(len(mean), d=window)
period = 1 / freq


# --------------------------------------------------------------------------- #
fig, ax = plt.subplots()

ax.plot(freq, spectrum, color="blue")

# ax.set_xticks(np.arange(0, 25, 2))

plt.tight_layout()
if savefig:
    plt.savefig(f"{savedir}/entrytime_weekday_{statistic}_{year}.png", dpi=300)

if showfig:
    plt.show()
