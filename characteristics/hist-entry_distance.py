import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fname = "/home/kc/Research/air_traffic/data/fr24_stat/time_distance_china.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-02-22"

filters = {"upper_t": False}

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)
# --------------------------------------------------------------------------- #
df = pd.read_csv(fname, header=0)
distances = df["delta_r_km"]

fig, ax = plt.subplots()
ax.hist(distances, 100, color="#8c4351")

# ax.set_xlim(-0.5, 23.5)
# ax.set_ylim(0, 1600)
ax.set_yscale("log")
ax.set_xlabel("Entry Distance (km)", fontsize=18)
ax.set_ylabel("Entry Flight Count", fontsize=18)


ax.tick_params(which="both", direction="out", labelsize=10)

plt.tight_layout()
plt.savefig(f"{sdir}/entry_distance.png", dpi=300)
# plt.show()
