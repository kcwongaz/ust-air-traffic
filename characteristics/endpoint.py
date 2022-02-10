import numpy as np
import pandas as pd
import os
from geopy import distance


# datadir = "/home/kc/Research/air_traffic/data/opensky_clean/"
datadir = f"/mnt/Passport/Opensky/Full_Track_Data"

savename = "/home/kc/Research/air_traffic/data/opensky_all_endpoints.csv"


# ---------------------------------------------------------------------------- #
def distance_euclidean(lat, lon):
    # Coordinate of HKIA
    hklat = 22.308046
    hklon = 113.918480

    dx = lat - hklat
    dy = lon - hklon

    d = np.sqrt(dx*dx + dy*dy)
    return d


# ---------------------------------------------------------------------------- #
hkia = (22.308046, 113.918480)

data = {"lat_f": [],            # Final lat
        "lon_f": [],            # Final lon
        "delta_hkia_km": [],    # Distance between final point and HKIA in km
        "delta_pseduo": []      # pseudo-Euclidean distance between final point and HKIA
}


for subdir, dirs, files in os.walk(datadir):
    for file in files:
        fname = os.path.join(subdir, file)

        if fname[-4:] != ".csv":
            continue
        else:
            print(fname)

        df = pd.read_csv(fname, header=0)
        last = df.iloc[-1]
        last_point = (last["latitude"], last["longitude"])

        data["lat_f"].append(last["latitude"])
        data["lon_f"].append(last["longitude"])
        data["delta_hkia_km"].append(distance.distance(last_point, hkia).km)
        data["delta_pseduo"].append(distance_euclidean(last["latitude"], last["longitude"]))


df_master = pd.DataFrame(data=data)
print(df_master)

df_master.to_csv(savename, index=False)
