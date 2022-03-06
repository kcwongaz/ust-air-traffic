import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from arrivial_rate import arrivial_rate, autocorr_period, autocovar_period


plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

fname = "/home/kc/Research/air_traffic/data/fr24_clean/time_distance.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-03-01"

dt = 60 * 15
year = 2017

# --------------------------------------------------------------------------- #
# Read data

df = pd.read_csv(fname, header=0)
df["year"] = pd.to_datetime(df["t_f"], unit="s").dt.year
df["month"] = pd.to_datetime(df["t_f"], unit="s").dt.month
df = df.loc[df["year"] == year]
# df = df[df["month"].isin([2, 3])]

arr_times = df["t_f"].to_numpy()
lambda_t, _ = arrivial_rate(arr_times, dt, start_hour=16, start_by="cut")
a_matrix = autocorr_period(lambda_t, dt, 86400)


# --------------------------------------------------------------------------- #
# Draw

fig, ax = plt.subplots()
t_axis = np.arange(dt/3600, 24, dt/3600)  # Time axis in hour


im = ax.imshow(a_matrix, cmap="plasma", extent=(0, 24, 0, 24), origin="lower",
               vmin=0, vmax=1)

ax.set_ylabel("Time $t$ (Hours from 00:00)", fontsize=12)
ax.set_xlabel("Forward Time Difference $T$ (Hour)", fontsize=12)

ax.set_xticks(range(0, 25, 2))
ax.set_yticks(range(0, 25, 2))
ax.set_title(f"Arrivial Rate Autocorrelation ({year})", fontsize=14)

cax = plt.axes([0.91, 0.15, 0.02, 0.7])
plt.colorbar(im, cax)

plt.tight_layout()
# plt.savefig(f"{sdir}/autocorrection_{year}.png", dpi=300)


# --------------------------------------------------------------------------- #
plt.show()
