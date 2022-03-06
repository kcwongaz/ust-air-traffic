import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

from arrivial_rate import arrivial_rate, fold_timeseries
from detrend import remove_seasonal_mean, seasonal_difference, \
                    seasonal_quotient


fname = "/home/kc/Research/air_traffic/data/fr24_clean/time_distance.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-03-01"

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

year = 2020
dt = 60 * 15
period = 86400

cmap_n = 20
plot_n = -1  # Number of curves to plot; -1 to plot all

save_fig = False

# --------------------------------------------------------------------------- #
# Read data

df = pd.read_csv(fname, header=0)
df["year"] = pd.to_datetime(df["t_f"], unit="s").dt.year
df["month"] = pd.to_datetime(df["t_f"], unit="s").dt.month
df = df.loc[df["year"] == year]
# df = df[df["month"].isin([2])]

arr_times = df["t_f"].to_numpy()
lambda_t, _ = arrivial_rate(arr_times, dt, start_hour=16, start_by="cut")


# --------------------------------------------------------------------------- #
# Draw
fig, ax = plt.subplots()
cmap = plt.get_cmap("Spectral", cmap_n)

# residue = lambda_t
# residue = seasonal_difference(lambda_t, dt, period)
residue = remove_seasonal_mean(lambda_t, dt, period)
# residue = seasonal_quotient(lambda_t, dt, period)


t_axis = np.arange(dt, period + dt, dt) / 3600
print(len(fold_timeseries(residue, dt, period)))

for i, ts in enumerate(fold_timeseries(residue, dt, period)):
    if plot_n != -1 and i > plot_n:
        break

    c = random.randint(0, cmap_n-1)
    # c = i % cmap
    ax.plot(t_axis, ts, color=cmap(c), alpha=1)


# --------------------------------------------------------------------------- #
plt.show()
