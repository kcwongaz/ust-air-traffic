import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from loop_helpers import *


# --------------------------------------------------------------------------- #
# Target datetime range to plot flight on; UTC 16:00 is HKT 00:00
target_start = pd.to_datetime("2017-01-01 00:00", format=r"%Y-%m-%d %H:%M")
target_end = pd.to_datetime("2017-01-31 23:59", format=r"%Y-%m-%d %H:%M")
target_start_str = target_start.strftime(r"%Y%m%d_%H%M")
target_end_str = target_end.strftime(r"%Y%m%d_%H%M")
dstr = f"{target_start_str}-{target_end_str}"

datadir = f"/home/kc/Research/air_traffic/data/redirection"
savedir = f"/home/kc/Research/air_traffic/figures/2022-04-26"
case = "1"

# --------------------------------------------------------------------------- #

ts = np.loadtxt(f"{datadir}/ts_{dstr}.txt")
ts = ts[np.nonzero(ts)]

fig, ax = plt.subplots()

bins = np.arange(0, 46, 5)
ax.hist(ts, bins=bins, color="royalblue", rwidth=0.7)
ax.set_xticks(bins)

plt.show()
