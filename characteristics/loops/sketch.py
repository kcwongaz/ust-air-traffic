import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from loop_helpers import *


# --------------------------------------------------------------------------- #
# Target datetime range to plot flight on; UTC 16:00 is HKT 00:00
target_start = pd.to_datetime("2017-01-22 15:00", format=r"%Y-%m-%d %H:%M")
target_end = pd.to_datetime("2017-01-22 16:00", format=r"%Y-%m-%d %H:%M")
target_start_str = target_start.strftime(r"%Y%m%d_%H%M")
target_end_str = target_end.strftime(r"%Y%m%d_%H%M")

datadir = f"/home/kc/Research/air_traffic/data/fr24_clean/spacetime/{target_start_str}-{target_end_str}"
savedir = f"/home/kc/Research/air_traffic/figures/thesis"
case = "1"

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Palatino"]
    }
)
# --------------------------------------------------------------------------- #
# Loop cases
if case == "1":
    min_loc = (70, 80)


# --------------------------------------------------------------------------- #
# Read in trajectory data
data = {}
for subdir, dirs, files in os.walk(datadir):
    for file in files:
        fname = os.path.join(subdir, file)

        if file == "fnames.txt":
            continue

        key = fname[:-4]
        data_arr = np.loadtxt(fname)
        data_arr = data_arr[data_arr[:, 1] <= 200]

        if data_arr[0, 3] > 115:
            continue

        data[key] = data_arr

# --------------------------------------------------------------------------- #
keys, flight_exit = sort_flight_keys(data, min_loc)


# --------------------------------------------------------------------------- #
# For test
fig, ax = plt.subplots()

flight = data[keys[2]]

# The spacetime curve
t = (flight[:, 0] - flight[0, 0]) / 60
d = flight[:, 1]
ax.plot(t, d, color="royalblue")


# The minima
min_dist, min_time = find_minima_spacetime(d, t, min_loc)
exit_dist, exit_time = find_exitpoint(d, t, min_loc)

for i in range(len(min_dist)):
    ax.plot(min_time[i], min_dist[i], color="black", marker="o",
            linestyle="none", ms=3)

ax.plot(exit_time, exit_dist, color="red", marker="o",
        linestyle="none", ms=3)



# Loop area
# ax.fill_between(np.arange(-3, 69), y1=min_loc[0], y2=min_loc[1], color="pink")


# Redirection
ax.vlines(x=34.0, ymin=-2.5, ymax=200, color="black", lw=1)
ax.axvspan(34-1, 34+1, color="darkgray", alpha=0.7)


# Figure details
ax.set_xlabel("Time (min)", fontsize=14)
ax.set_ylabel("Distance (km)", fontsize=14)
ax.set_xlim(-3, 68)
ax.set_ylim(-2.5, 200)

plt.tight_layout()
# plt.savefig(f"{savedir}/fig2.pdf", dpi=300)

np.savetxt(f"{savedir}/4-3_t.txt", t)
np.savetxt(f"{savedir}/4-3_d.txt", d)

plt.show()
