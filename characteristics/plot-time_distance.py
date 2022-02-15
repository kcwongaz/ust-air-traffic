import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fname = "/home/kc/Research/air_traffic/data/fr24_stat/time_distance_china_filtered.txt"
filters = {"lower_r": False, "upper_t": False}

sdir = "/home/kc/Research/air_traffic/figures/2022-02-15"
sname = "time_distance"

# --------------------------------------------------------------------------- #
df = pd.read_csv(fname, header=0)

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

delta_r = df["delta_r_km"].to_numpy()
delta_t = df["delta_t_sec"].to_numpy() / 60


if filters["lower_r"]:
    index = np.argwhere(delta_r > 10)
    delta_r = delta_r[index]
    delta_t = delta_t[index]

if filters["upper_t"]:
    index = np.argwhere(delta_t < 100)
    delta_r = delta_r[index]
    delta_t = delta_t[index]


fig, ax = plt.subplots()
ax.scatter(delta_r, delta_t, s=20,
           c="blue", marker="o", alpha=0.12)

if not filters["upper_t"]:
    ax.axhline(y=1440, color="black")

# ax.grid(linestyle="--")

ax.set_xlabel("Distance (km)", fontsize=20)
ax.set_ylabel("Time Difference (min)", fontsize=20)
ax.tick_params(which="both", direction="in", labelsize=14)

ax.set_ylim(0, 1250)


plt.tight_layout()
plt.savefig(f"{sdir}/{sname}_test.png", dpi=300)
