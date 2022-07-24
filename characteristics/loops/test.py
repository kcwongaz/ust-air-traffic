from re import L
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy import distance
import os
import random
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from loop_helpers import find_first_turning_dist


# --------------------------------------------------------------------------- #
# Target datetime range to plot flight on; UTC 16:00 is HKT 00:00
target_start = pd.to_datetime("2017-01-22 15:00", format=r"%Y-%m-%d %H:%M")
target_end = pd.to_datetime("2017-01-22 16:00", format=r"%Y-%m-%d %H:%M")
target_start_str = target_start.strftime(r"%Y%m%d_%H%M")
target_end_str = target_end.strftime(r"%Y%m%d_%H%M")

datadir = f"/home/kc/Research/air_traffic/data/fr24_clean/spacetime/{target_start_str}-{target_end_str}"
savedir = f"/home/kc/Research/air_traffic/figures/2022-04-19"
case = "all"


ncolor = 10

showfig = True
savefig = False

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

# --------------------------------------------------------------------------- #
# Loop cases
if case == "31":
    loop_max = 95
    loop_min = 30
elif case == "21":
    loop_max = 150
    loop_min = 95
elif case == "22":
    loop_max = 150
    loop_min = 95


# --------------------------------------------------------------------------- #
# Read in trajectory data

data = {}
for subdir, dirs, files in os.walk(datadir):
    for file in files:
        fname = os.path.join(subdir, file)
        print(fname)

        if file == "fnames.txt":
            continue

        spacetime = np.loadtxt(fname)
        key = fname[:-4]

        data[key] = {}
        data[key]["t"] = spacetime[:, 0]
        data[key]["d"] = spacetime[:, 1]


# --------------------------------------------------------------------------- #
fig, ax = plt.subplots()
cmap = plt.cm.get_cmap("tab10", ncolor)

count = 0

# To ensure flight nearby in time has different color, sort the flights first
keys = []
land_times = []
for k, flight in data.items():
    keys.append(k)
    land_times.append(flight["t"][-1])

ind = np.argsort(land_times)
keys = np.array(keys)
keys = keys[ind]


for k in keys:
    flight = data[k]
    t = flight["t"]
    d = flight["d"]

    ind = np.where(flight["d"] <= 200)
    d = d[ind]
    t = t[ind]

    if case != "all":
        loop_dist = find_first_turning_dist(d)
        if loop_dist > loop_max or loop_dist < loop_min:
            continue

    count += 1
    c = cmap(count % ncolor)

    # Shift the time origin
    t = t - target_start.timestamp()
    t /= 60

    # c = cmap(random.randint(0, ncolor-1))

    ax.plot(t, d, color=c, alpha=0.90)


ax.set_xlabel("Time $t$ (min)", fontsize=14)
ax.set_ylabel("Distance from HKIA $d$ (km)", fontsize=14)


title_date = target_start.strftime("%Y-%m-%d")
title_time = target_start.strftime("%H:%M")
ax.set_title(f"{title_date}; $t=0$ at {title_time}", fontsize=16)

plt.tight_layout()

if savefig:
    start_hour = target_start.strftime("%Y-%m-%d-%H%M")
    end_hour = target_end.strftime("%Y-%m-%d-%H%M")
    plt.savefig(f"{savedir}/spacetime{case}_{start_hour}_{end_hour}.png",
                dpi=300)

if showfig:
    plt.show()


# --------------------------------------------------------------------------- #
