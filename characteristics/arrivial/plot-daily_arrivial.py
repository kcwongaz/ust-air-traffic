import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from arrivial_rate import arrivial_rate, fold_timeseries, nullify_day


plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

fname = "/home/kc/Research/air_traffic/data/fr24_clean/time_distance.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-03-08"

dt = 60 * 15
year = 2017

save_fig = True

# --------------------------------------------------------------------------- #
# Read data

df = pd.read_csv(fname, header=0)
df["year"] = pd.to_datetime(df["t_f"], unit="s").dt.year
df["month"] = pd.to_datetime(df["t_f"], unit="s").dt.month
df = df.loc[df["year"] == year]
df = df[df["month"].isin([1, 2, 3])]

arr_times = df["t_f"].to_numpy()
lambda_t, _ = arrivial_rate(arr_times, dt, start_hour=16, start_by="cut")
# lambda_t = nullify_day(lambda_t, dt)
lamdba_folded = fold_timeseries(lambda_t, dt, 86400)

# Get the index for 3:00 to 4:00
window_night = np.arange(3600 * 3 // dt, 3600 * 4 // dt)

# Get the index for 12:00 to 14:00
window_day = np.arange(3600 * 13 // dt, 3600 * 14 // dt)
window_morn = np.arange(3600 * 10 // dt, 3600 * 11 // dt)

# Get the binned counts
daily_total = np.zeros(len(lamdba_folded))
daily_night = np.zeros(len(lamdba_folded))
daily_day = np.zeros(len(lamdba_folded))
daily_morn = np.zeros(len(lamdba_folded))

for i, value in enumerate(lamdba_folded):
    daily_total[i] = np.sum(value)
    daily_night[i] = np.sum(value[window_night])
    daily_day[i] = np.sum(value[window_day])
    daily_morn[i] = np.sum(value[window_morn])

daily_total /= np.nanmax(daily_total)
daily_night /= np.nanmax(daily_night)
daily_day /= np.nanmax(daily_day)
daily_morn /= np.nanmax(daily_morn)


# --------------------------------------------------------------------------- #
# Draw

fig, ax = plt.subplots()
t_axis = np.arange(len(daily_total))

ax.plot(t_axis, daily_total, color="black", label="Whole Day", marker=".")
ax.plot(t_axis, daily_morn, color="green", label="10:00 to 11:00 HKT",
        marker=".")
ax.plot(t_axis, daily_day, color="red", label="13:00 to 14:00 HKT",
        marker=".")
ax.plot(t_axis, daily_night, color="blue", label="03:00 to 04:00 HKT",
        marker=".")

ax.set_ylabel("Normalized Count", fontsize=12)
ax.set_xlabel("Day since 2017-01-01", fontsize=12)

plt.title(f"Daily Arrivial Count ({year}, Jan - Mar)", fontsize=14)
plt.legend(loc="lower left")

plt.tight_layout()
if save_fig:
    plt.savefig(f"{sdir}/daily_count_{year}_absolute.png", dpi=300)


# --------------------------------------------------------------------------- #
plt.show()
