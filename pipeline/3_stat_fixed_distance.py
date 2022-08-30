import pandas as pd
import os

from air_traffic.trajectory import *


d_min = 145
d_max = 165

datadir = "../data/cleaned"
savedir = "../data/results"
savename = f"stat_fixed_distance_{d_min}-{d_max}.csv"

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


# Create destination directory if not exist
if not os.path.exists(savedir):
    os.makedirs(savedir, exist_ok=True)

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
        last = find_first_landed(df)

        # Check this later
        # # Skip flights that not landed in the square
        # if (np.abs(last["latitude"] - hkia[0]) > 0.25) and \
        #    (np.abs(last["longitude"] - hkia[1]) > 0.25):
        #     continue

        # Find the first point in the fixed ring
        first = find_first_in_range(df, d_min, d_max)
        if first is None:
            continue

        # Get the date at HK time
        date = pd.Timestamp(first["time"] + 8*3600, unit="s").strftime("%Y-%m-%d")

        # Identifiers
        data["date"].append(date)
        data["callsign"].append(file[:-4])

        last_point = (last["latitude"], last["longitude"])

        # Positional data
        data["lat_i"].append(first["latitude"])
        data["lon_i"].append(first["longitude"])
        data["lat_f"].append(last["latitude"])
        data["lon_f"].append(last["longitude"])
        data["delta_r_km"].append(distance(first, last))
        data["r_i_km"].append(distance_hkia(first))

        # Compute time difference
        data["t_i"].append(first["time"])
        data["t_f"].append(last["time"])
        data["delta_t_sec"].append(last["time"] - first["time"])


df_master = pd.DataFrame(data=data)
df_master.to_csv(f"{savedir}/{savename}", index=False)
