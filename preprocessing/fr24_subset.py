import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy import distance
import os
import random


# --------------------------------------------------------------------------- #
# Date to start and end searching
start_date = pd.to_datetime("2017-01-01", format=r"%Y-%m-%d")
end_date = pd.to_datetime("2018-12-31", format=r"%Y-%m-%d")

# Target datetime range to plot flight on, specified in HKT
target_start = pd.to_datetime("2017-01-01 00:00", format=r"%Y-%m-%d %H:%M")
target_end = pd.to_datetime("2018-12-31 23:59", format=r"%Y-%m-%d %H:%M")


datadir = f"/home/kc/Research/air_traffic/data/fr24_clean"
savedir = f"/home/kc/Research/air_traffic/data/fr24_clean/spacetime"

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
            if file == ".csv":
                continue

            df = pd.read_csv(fname, header=0)

            # Read in data
            lat = df["latitude"].to_numpy()
            lon = df["longitude"].to_numpy()
            time = df["time"].to_numpy()
            callsign = df["callsign"].iloc[0]

            dist = [distance.distance(x, hkia).km for x in zip(lat, lon)]

            # Shift all time by 8 hours to work in HKT
            # Get land date in HKT and keep only those in the target window
            time = time + 8*3600
            land_date = pd.to_datetime(time[-1], unit="s")

            if land_date > target_end or land_date < target_start:
                continue

            # Create unique identifier
            key = working_date.strftime(r"%Y%m%d") + callsign

            data[key] = {}
            data[key]["d"] = np.array(dist)
            data[key]["t"] = time
            data[key]["lat"] = lat
            data[key]["lon"] = lon
            data[key]["fname"] = fname

        working_date += delta


# --------------------------------------------------------------------------- #
# Dump the data

# Create target directionary if not already there
target_start_str = target_start.strftime(r"%Y%m%d_%H%M")
target_end_str = target_end.strftime(r"%Y%m%d_%H%M")
targetdir = f"{savedir}/{target_start_str}-{target_end_str}"

if not os.path.exists(targetdir):
    os.makedirs(targetdir, exist_ok=True)
else:
    print("Warning: Target directory already existed. Please check.")


# Save the spacetime curves one by one
# At the same time compile the list of flight file
fname_list = []
for key, flight in data.items():
    dataname = f"{targetdir}/{key}.txt"

    spacetime = np.column_stack((flight["t"], flight["d"],
                                 flight["lat"], flight["lon"]))
    np.savetxt(dataname, spacetime)

    fname_list.append(flight["fname"])

# Save the file list
with open(f"{targetdir}/fnames.txt", "w") as f:
    [f.write(fname + "\n") for fname in fname_list]
