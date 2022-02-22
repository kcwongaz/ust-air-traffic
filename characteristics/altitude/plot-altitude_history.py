import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


datadir = "/home/kc/Research/air_traffic/data/fr24_clean/2017-01"
savedir = "/home/kc/Research/air_traffic/figures/2022-02-22/"

# --------------------------------------------------------------------------= #

fig, ax = plt.subplots()

for subdir, dirs, files in os.walk(datadir):
    for file in files:
        if not file.endswith(".csv"):
            continue

        fname = os.path.join(subdir, file)
        df = pd.read_csv(fname, header=0)
        print(fname)

        df = df.loc[(df["latitude"] > 19) & (df["latitude"] < 25.5) &
                    (df["longitude"] > 111) & (df["longitude"] < 117.5)]

        if len(df) == 0:
            continue

        alt = df["altitude"].to_numpy()
        time = df["time"].to_numpy()
        timefraction = (time[-1] - time)

        ax.plot(timefraction, alt, color="blue", alpha=0.1, linewidth=1)

plt.show()
