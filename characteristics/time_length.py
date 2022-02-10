import numpy as np
import pandas as pd
import os


datadir = "/home/kc/Research/air_traffic/data/opensky_clean/"
# ---------------------------------------------------------------------------- #
def build_timestamp(datestr):
    # Remove the useless +00:00 at the end
    datestr = datestr[:-6]
    
    f = "%Y-%m-%d %H:%M:%S"
    dt = pd.to_datetime(datestr, format=f)

    return dt

# ---------------------------------------------------------------------------- #
delta_all = []
for subdir, dirs, files in os.walk(datadir):
    for file in files:
        fname = os.path.join(subdir, file)

        if fname[-4:] != ".csv":
            continue
        else:
            print(fname)

        df = pd.read_csv(fname, header=0)
        first_time = build_timestamp(df.iloc[0]["timestamp"])
        last_time = build_timestamp(df.iloc[-1]["timestamp"])

        delta = (last_time - first_time) / pd.Timedelta(1, "min")
        delta_all.append(delta)


delta_all = np.sort(delta_all)
np.savetxt("/home/kc/Research/air_traffic/data/time_length.txt", delta_all)
