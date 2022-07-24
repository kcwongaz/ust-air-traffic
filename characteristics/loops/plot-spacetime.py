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
# target_start = pd.to_datetime("2017-01-21 16:00", format=r"%Y-%m-%d %H:%M")
# target_end = pd.to_datetime("2017-01-22 16:00", format=r"%Y-%m-%d %H:%M")
target_start = pd.to_datetime("2017-01-22 07:00", format=r"%Y-%m-%d %H:%M")  # 15:00 HKT
target_end = pd.to_datetime("2017-01-22 08:00", format=r"%Y-%m-%d %H:%M")    # 16:00 HKT

# Date to start and end searching
start_date = pd.to_datetime("2017-01-20", format=r"%Y-%m-%d")
end_date = pd.to_datetime("2017-01-22", format=r"%Y-%m-%d")


datadir = f"/home/kc/Research/air_traffic/data/fr24_clean"
savedir = f"/home/kc/Research/air_traffic/figures/2022-03-29"
case = "22"


ncolor = 10

plotmap = True

showfig = False
savefig = True

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

# Coordinates of HKIA
hkia = (22.308046, 113.918480)

# Setting up the loop over dates
delta = pd.Timedelta(1, "D")
working_date = start_date

while working_date <= end_date:
    dstr = working_date.strftime(r"%Y-%m-%d")
    mstr = working_date.strftime(r"%Y-%m")

    for subdir, dirs, files in os.walk(f"{datadir}/{mstr}/{dstr}"):
        for file in files:
            fname = os.path.join(subdir, file)
            print(fname)

            df = pd.read_csv(fname, header=0)

            # Keep only if the flight landed on the target range
            land_date = pd.to_datetime(df["time"].iloc[-1], unit="s")
            if land_date > target_end or land_date < target_start:
                continue

            # Read in data
            lat = df["latitude"].to_numpy()
            lon = df["longitude"].to_numpy()
            time = df["time"].to_numpy()
            callsign = df["callsign"].iloc[0]

            dist = [distance.distance(x, hkia).km for x in zip(lat, lon)]

            # Add mstr to create a unique identifier
            key = callsign + mstr

            data[key] = {}
            data[key]["d"] = np.array(dist)
            data[key]["t"] = time
            data[key]["fname"] = fname
            data[key]["lat0"] = lat[0]  # entry lat

        working_date += delta


# --------------------------------------------------------------------------- #
fig, ax = plt.subplots()
cmap = plt.cm.get_cmap("tab10", ncolor)

count = 0
fnames_plot = []

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

    if case == "21":
        if flight["lat0"] > 21:
            continue

    if case == "22":
        if flight["lat0"] < 21:
            continue

    if case != "all":
        loop_dist = find_first_turning_dist(d)
        if loop_dist > loop_max or loop_dist < loop_min:
            continue

    count += 1
    c = cmap(count % ncolor)

    fnames_plot.append(flight["fname"])

    # Shift the time origin
    t = t - target_start.timestamp()
    t /= 60

    # c = cmap(random.randint(0, ncolor-1))

    ax.plot(t, d, color=c, alpha=0.90)


ax.set_xlabel("Time $t$ (min)", fontsize=14)
ax.set_ylabel("Distance from HKIA $d$ (km)", fontsize=14)


# Now shift UTC to HKT by adding 8 hours
target_start += pd.Timedelta(8*3600, unit="s")
target_end += pd.Timedelta(8*3600, unit="s")

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
if plotmap:

    plt.cla()
    plt.clf()

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([111, 117.5, 19, 25.5], ccrs.PlateCarree())
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

    # Reset counter for getting the same color
    count = 0

    for fname in fnames_plot:
        count += 1
        c = cmap(count % ncolor)

        df = pd.read_csv(fname, header=0)
        lat = df["latitude"].to_numpy()
        lon = df["longitude"].to_numpy()

        ax.plot(lon, lat, transform=ccrs.Geodetic(),
                linewidth=0.8, alpha=0.8, color=c)

        gridlines = ax.gridlines(draw_labels=True, zorder=0,
                                 linestyle="dashed", linewidth=0.5,
                                 color="dimgrey")

        gridlines.top_labels = False
        gridlines.right_labels = False

    plt.tight_layout()

    if savefig:
        start_hour = target_start.strftime("%Y-%m-%d-%H:%M")
        end_hour = target_end.strftime("%Y-%m-%d-%H:%M")
        plt.savefig(f"{savedir}/map{case}_{start_hour}_{end_hour}.png",
                    dpi=600)

    if showfig:
        plt.show()
