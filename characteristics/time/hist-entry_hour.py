import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fname = "/home/kc/Research/air_traffic/data/fr24_stat/time_distance_china.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-02-15"

filters = {"upper_t": False}

year = 2021

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)
# --------------------------------------------------------------------------- #
df_all = pd.read_csv(fname, header=0)

# Hong Kong time is UTC+8
df_all["t_i"] = df_all["t_i"] + 8*3600
timestamps = pd.to_datetime(df_all["t_i"], unit="s")
df_all = df_all.assign(hour=timestamps.dt.hour)
df_all = df_all.loc[timestamps.dt.year == year]


if filters["upper_t"]:
    df_all = df_all.loc[df_all["delta_t_sec"] / 60 < 800]

hours = df_all["hour"]

fig, ax = plt.subplots()
ax.hist(hours, np.arange(-0.5, 24, 1), edgecolor="white", linewidth=4.0,
        color="#8c4351")

ax.set_xlim(-0.5, 23.5)
# ax.set_ylim(0, 1600)
ax.set_xlabel("Hour (HK Time, UTC+8)", fontsize=18)
ax.set_ylabel("Entry Flight Count", fontsize=18)


ax.tick_params(which="both", direction="out", labelsize=10)
ax.set_xticks(np.arange(24))
ax.set_title(year, fontsize=18)

plt.tight_layout()
plt.savefig(f"{sdir}/entry_hour_{year}.png", dpi=300)
# plt.show()
