import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from loop_helpers import sort_flight_exittime, redirect_flight


# --------------------------------------------------------------------------- #
# Target datetime range to plot flight on; UTC 16:00 is HKT 00:00
target_start = pd.to_datetime("2017-01-22 15:00", format=r"%Y-%m-%d %H:%M")
target_end = pd.to_datetime("2017-01-22 16:00", format=r"%Y-%m-%d %H:%M")
target_start_str = target_start.strftime(r"%Y%m%d_%H%M")
target_end_str = target_end.strftime(r"%Y%m%d_%H%M")

datadir = f"/home/kc/Research/air_traffic/data/fr24_clean/spacetime/{target_start_str}-{target_end_str}"
savedir = f"/home/kc/Research/air_traffic/figures/2022-04-19"
case = "1"

# --------------------------------------------------------------------------- #
# Loop cases
if case == "1":
    min_loc = (70, 80)


# --------------------------------------------------------------------------- #
# Read in trajectory data
data = {}
for subdir, dirs, files in os.walk(datadir):
    for file in files:
        fname = os.path.join(subdir, file)

        if file == "fnames.txt":
            continue

        key = fname[:-4]
        data_arr = np.loadtxt(fname)
        data_arr = data_arr[data_arr[:, 1] <= 200]

        if data_arr[0, 3] > 115:
            continue

        data[key] = data_arr

# --------------------------------------------------------------------------- #

flight_min, flight_exit, flight_dist = sort_flight_exittime(data,
                                               min_loc=min_loc)


for i in range(len(flight_min)):
    print(redirect_flight(flight_min, flight_exit, i, tol=30) / 60)



# --------------------------------------------------------------------------- #
# For test
fig, ax = plt.subplots()

for key, flight in data.items():
    ax.plot(flight[:, 0], flight[:, 1])


for i in range(len(flight_min)):
    ax.vlines(x=flight_exit[i], ymin=0, ymax=200, color="black")

plt.show()
