import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy import distance
import os
import random

from loop_helpers import find_first_turning_dist


# --------------------------------------------------------------------------- #
# Date to start and end searching
start_date = pd.to_datetime("2017-01-01", format=r"%Y-%m-%d")
end_date = pd.to_datetime("2017-02-02", format=r"%Y-%m-%d")


datadir = f"/home/kc/Research/air_traffic/data/fr24_clean"
savedir = f"/home/kc/Research/air_traffic/figures/2022-03-29/201701_30-95"

ncolor = 10
cmap = plt.cm.get_cmap("tab10", ncolor)

showfig = True
savefig = True

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

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

            # Read in data
            lat = df["latitude"].to_numpy()
            lon = df["longitude"].to_numpy()
            time = df["time"].to_numpy()
            callsign = df["callsign"].iloc[0]

            dist = [distance.distance(x, hkia).km for x in zip(lat, lon)]

            # Shift all time by 8 hours to work in HKT
            time = time + 8*3600
            land_date = pd.to_datetime(time[-1], unit="s")
            lstr = land_date.strftime(r"%Y-%m-%d")

            # Add date if not already exist
            if lstr not in data:
                data[lstr] = {}

            # Add mstr to create a unique identifier
            key = callsign + mstr

            data[lstr][key] = {}
            data[lstr][key]["d"] = np.array(dist)
            data[lstr][key]["t"] = time
            data[lstr][key]["fname"] = fname

        working_date += delta


# --------------------------------------------------------------------------- #
for date in data:
    fig, ax = plt.subplots(figsize=(10, 5))
    subdata = data[date]
    datetime = pd.to_datetime(date, format=r"%Y-%m-%d")

    count = 0

    for k, flight in subdata.items():
        t = flight["t"]
        d = flight["d"]

        ind = np.where(flight["d"] <= 200)
        d = d[ind]
        t = t[ind]

        loop_dist = find_first_turning_dist(d)
        if loop_dist > 95 or loop_dist < 30:
            continue

        # Shift the time origin
        t = t - datetime.timestamp()
        t /= 3600

        count += 1
        c = cmap(count % ncolor)
        # c = cmap(random.randint(0, ncolor-1))

        ax.plot(t, d, color=c, alpha=0.90, lw=0.3)

    ax.set_xlim(11.5, 20.5)
    ax.set_xticks(range(12, 21))

    ax.set_xlabel("Time $t$ (hour)", fontsize=14)
    ax.set_ylabel("Distance from HKIA $d$ (km)", fontsize=14)

    # Now shift UTC to HKT by adding 8 hours
    ax.set_title(f"{date} ({count})", fontsize=16)

    plt.tight_layout()

    if savefig:
        plt.savefig(f"{savedir}/{date}.png", dpi=600)

    plt.cla()
    plt.clf()
