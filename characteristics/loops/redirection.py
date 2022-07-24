import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from loop_helpers import *


# --------------------------------------------------------------------------- #
# Target datetime range to plot flight on; UTC 16:00 is HKT 00:00
target_start = pd.to_datetime("2017-01-01 00:00", format=r"%Y-%m-%d %H:%M")
target_end = pd.to_datetime("2018-12-31 23:59", format=r"%Y-%m-%d %H:%M")
target_start_str = target_start.strftime(r"%Y%m%d_%H%M")
target_end_str = target_end.strftime(r"%Y%m%d_%H%M")
dstr = f"{target_start_str}-{target_end_str}"

datadir = f"/home/kc/Research/air_traffic/data/fr24_clean/spacetime/{dstr}"
savedir = f"/home/kc/Research/air_traffic/data/redirection"
case = "all"

# --------------------------------------------------------------------------- #
# Loop cases
if case == "1":
    min_loc = (70, 80)
if case == "2":
    min_loc = (90, 130)


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

        # if data_arr[0, 3] > 115:
        #     continue

        data[key] = data_arr

# --------------------------------------------------------------------------- #

min_loc = label_flight_loops(data)
flight_min, flight_exit, flight_dist = sort_flight_minima(data, min_loc)

chain = []
time_saved = []
time_single = []
timestamp = []
entrytime = []


for i in range(len(flight_min)):
    time_saved_i = redirect_flight(flight_min, flight_exit, i, tol=30) / 60

    chain.append(len(time_saved_i) - 1)
    time_saved.append(np.sum(time_saved_i))
    time_single.append(time_saved_i[0])
    timestamp.append(flight_exit[i])
    entrytime.append(flight_min[i][0])

# print(chain)
# print(time_saved)

count_sel_prob = detect_selection_problem(flight_min, flight_exit, tol=30)
print(count_sel_prob)

np.savetxt(f"{savedir}/chain_{case}_{dstr}.txt", chain)
np.savetxt(f"{savedir}/ts_{case}_{dstr}.txt", time_saved)
np.savetxt(f"{savedir}/ts1_{case}_{dstr}.txt", time_single)
np.savetxt(f"{savedir}/timestamp_{case}_{dstr}.txt", timestamp)
np.savetxt(f"{savedir}/entrytime_{case}_{dstr}.txt", entrytime)
