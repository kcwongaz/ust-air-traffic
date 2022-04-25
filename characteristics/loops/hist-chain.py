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

chain = np.loadtxt(f"{datadir}/chain_{dstr}.txt")

fig, ax = plt.subplots()


edges = np.arange(-0.5, 7, 1)
centers = (edges[:-1] + edges[1:]) / 2

hist, _ = np.histogram(chain, bins=edges)
print(hist)

ax.bar(centers, hist)
ax.set_xticks(centers)

plt.show()
