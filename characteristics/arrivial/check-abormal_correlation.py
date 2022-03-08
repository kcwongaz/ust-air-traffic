import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from arrivial_rate import arrivial_rate, autocorr_period, nullify_day


plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

fname = "/home/kc/Research/air_traffic/data/fr24_clean/time_distance.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-03-08"

dt = 60 * 15
year = 2017

save_fig = False

# --------------------------------------------------------------------------- #
# Read data

df = pd.read_csv(fname, header=0)
df["year"] = pd.to_datetime(df["t_f"], unit="s").dt.year
df["month"] = pd.to_datetime(df["t_f"], unit="s").dt.month
df = df.loc[df["year"] == year]
df = df[df["month"].isin([3])]

arr_times = df["t_f"].to_numpy()
lambda_t, _ = arrivial_rate(arr_times, dt, start_hour=16, start_by="cut")
lambda_t = nullify_day(lambda_t, dt)
a_matrix = autocorr_period(lambda_t, dt, 5*86400)


# --------------------------------------------------------------------------- #
# Draw

fig, ax = plt.subplots()
t_axis = np.arange(len(a_matrix[0])) * dt/3600  # Time axis in hour

im = ax.imshow(a_matrix, cmap="plasma", extent=(0, t_axis[-1], 0, t_axis[-1]),
               origin="lower", vmin=0, vmax=1)

ax.set_ylabel("Time $t$ (Hours from 00:00 HKT)", fontsize=12)
ax.set_xlabel("Forward Time Difference $T$ (Hour)", fontsize=12)

# ax.set_xticks(range(0, 25, 2))
# ax.set_yticks(range(0, 25, 2))
ax.set_title(f"Arrivial Rate Autocorrelation ({year})", fontsize=14)

cax = plt.axes([0.91, 0.15, 0.02, 0.7])
plt.colorbar(im, cax)


if save_fig:
    plt.savefig(f"{sdir}/autocorrection_corrected_{year}.png", dpi=300)


# --------------------------------------------------------------------------- #
plt.show()
