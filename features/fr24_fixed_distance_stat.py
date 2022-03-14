import pandas as pd
import os
import numpy as np
from geopy import distance


label = "clean"
d_min = 145
d_max = 165


datadir = f"/home/kc/Research/air_traffic/data/fr24_{label}/"
savedir = "/home/kc/Research/air_traffic/data/fr24_clean"
savename = f"{savedir}/stat_{d_min}-{d_max}.txt"

# --------------------------------------------------------------------------- #
data = {"date": [],             # Date
        "callsign": [],         # Callsign
        "lat_i": [],            # Entry lat
        "lon_i": [],            # Entry lon
        "lat_f": [],            # Final lat
        "lon_f": [],            # Final lon
        "t_i": [],              # Entry timestamp
        "t_f": [],              # Final timestamp
        "r_i_km": [],           # Entry distance from HKIA in km
        "delta_r_km": [],       # Distance between entry and final point in km
        "delta_t_sec": []}      # Time difference in second


hkia = (22.308046, 113.918480)

for subdir, dirs, files in os.walk(datadir):

    # Process in sorted order for easy tracking
    dirs.sort()
    files.sort()

    for file in files:
        fname = os.path.join(subdir, file)

        if fname[-4:] != ".csv":
            continue
        else:
            print(fname)

        df = pd.read_csv(fname, header=0)
        df = df.loc[(df["latitude"] > 19) & (df["latitude"] < 25.5) &
                    (df["longitude"] > 111) & (df["longitude"] < 117.5)]

        # Skip if there is no useable data
        if len(df) == 0:
            continue

        # Find the first landing point
        # Get through the inital take-off stage
        n = 0
        while df["altitude"].iloc[n] == 0:
            n += 1
            # Also possible that the whole flight record is already landed
            if n == len(df):
                n = 0
                break
        df_last = df.iloc[n:]
        df_last = df_last.loc[df_last["altitude"] == 0]
        last = df_last.iloc[0]

        # Skip flights that not landed in the square
        if (np.abs(last["latitude"] - hkia[0]) > 0.25) and \
           (np.abs(last["longitude"] - hkia[1]) > 0.25):
            continue

        last_point = (last["latitude"], last["longitude"])

        # Find the first point in the fixed ring
        n = 0
        first = df.iloc[0]
        first_point = (first["latitude"], first["longitude"])
        d = distance.distance(first_point, hkia).km

        # Loop until reaching the first point within the ring
        while d > d_max:
            n += 1
            first = df.iloc[n]
            first_point = (first["latitude"], first["longitude"])
            d = distance.distance(first_point, hkia).km

        # If there are no point within the ring, skip
        if d < d_min:
            continue

        # Get the date at HK time
        date = pd.Timestamp(first["time"] + 8*3600, unit="s").strftime("%Y-%m-%d")

        # Identifiers
        data["date"].append(date)
        data["callsign"].append(file[:-4])

        # Positional data
        data["lat_i"].append(first["latitude"])
        data["lon_i"].append(first["longitude"])
        data["lat_f"].append(last["latitude"])
        data["lon_f"].append(last["longitude"])
        data["delta_r_km"].append(distance.distance(first_point, last_point).km)
        data["r_i_km"].append(d)

        # Compute time difference
        data["t_i"].append(first["time"])
        data["t_f"].append(last["time"])
        data["delta_t_sec"].append(last["time"] - first["time"])


df_master = pd.DataFrame(data=data)
print(df_master)

df_master.to_csv(savename, index=False)
