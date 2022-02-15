import pandas as pd
import os
from geopy import distance


label = "usa"
datadir = f"/home/kc/Research/air_traffic/data/fr24_{label}/"
savename = f"/home/kc/Research/air_traffic/data/fr24_stat/time_distance_{label}.txt"


# --------------------------------------------------------------------------- #
data = {"date": [],             # Date
        "callsign": [],         # Callsign
        "lat_i": [],            # Entry lat
        "lon_i": [],            # Entry lon
        "h_i": [],              # Entry heading angle
        "lat_f": [],            # Final lat
        "lon_f": [],            # Final lon
        "t_i": [],              # Entry timestamp
        "t_f": [],              # Final timestamp
        "delta_r_km": [],       # Distance between entry and final point in km
        "delta_t_sec": [],      # Time difference in second
        "delta_hkia_km": []}    # Distance between final point and HKIA in km


hkia = (22.308046, 113.918480)

for subdir, dirs, files in os.walk(datadir):
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

        first = df.iloc[0]
        last = df.iloc[-1]

        # Get the date at HK time
        date = pd.Timestamp(first["time"] + 8*3600, unit="s").strftime("%Y-%m-%d")

        # Identifiers
        data["date"].append(date)
        data["callsign"].append(file[:-4])

        # Positional data are easy
        data["lat_i"].append(first["latitude"])
        data["lon_i"].append(first["longitude"])
        data["h_i"].append(first["heading_angle"])

        data["lat_f"].append(last["latitude"])
        data["lon_f"].append(last["longitude"])

        # Compute distance using geopy; the default is the WGS-84 distance
        first_point = (first["latitude"], first["longitude"])
        last_point = (last["latitude"], last["longitude"])
        data["delta_r_km"].append(distance.distance(
                                  first_point, last_point).km)
        data["delta_hkia_km"].append(distance.distance(last_point, hkia).km)

        # Compute time difference by turning things into Pandas timestamps
        data["t_i"].append(first["time"])
        data["t_f"].append(last["time"])
        data["delta_t_sec"].append(last["time"] - first["time"])


df_master = pd.DataFrame(data=data)
print(df_master)

df_master.to_csv(savename, index=False)
