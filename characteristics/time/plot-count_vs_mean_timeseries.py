import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import binned_statistic
from moving_avg import moving_avg, arrivial_rate


fname = "/home/kc/Research/air_traffic/data/fr24_clean/stat_145-165_clustered.txt"
savedir = "/home/kc/Research/air_traffic/figures/2022-03-22"

year = 2018

window = 0.25
bins = np.arange(0, 24.1, window)

# mode: ["mean", "arrival"]
mode = "mean"

savefig = True
showfig = True


# --------------------------------------------------------------------------- #
def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """

    return np.isnan(y), lambda z: z.nonzero()[0]


# --------------------------------------------------------------------------- #
df = pd.read_csv(fname)
df["year"] = pd.to_datetime(df["t_i"], unit="s").dt.year
df = df.loc[df["year"] == year]
df["month"] = pd.to_datetime(df["t_i"], unit="s").dt.month
df = df.loc[df["month"].isin([1, 2, 3])]

# Entry times
second = (df["t_i"].to_numpy() + 8*3600)
hour = second / 3600

# Transit times
delta_t = df["delta_t_sec"].to_numpy() / 60

# Arrivial times
second_f = (df["t_f"].to_numpy() + 8*3600)
hour_f = second_f / 3600


delta_avg, t_axis = moving_avg(delta_t, second, dt=window*60*60,
                               start_hour=0, start_by="cut")
entry_count, _ = arrivial_rate(second, dt=window*60*60,
                               start_hour=0, start_by="cut")
arrivial_count, t_axis_arr = arrivial_rate(second_f, dt=window*60*60,
                                           start_hour=0, start_by="cut")

print(t_axis[0])
print(t_axis[0] % 86400)
t_axis_arr -= t_axis[0]
t_axis -= t_axis[0]

t_axis_arr /= 60
t_axis /= 60

# Remove the nan's by interpolation
# nans, x = nan_helper(delta_avg)
# delta_avg1 = delta_avg.copy()
# # delta_avg1[nans] = np.interp(x(nans), x(~nans), delta_avg1[~nans])
# delta_avg1[nans] = 0


# --------------------------------------------------------------------------- #
fig, ax = plt.subplots()

if mode == "mean":

    axt = ax.twinx()
    ax.plot(t_axis[:300], delta_avg[:300], marker=".",
            color="black", alpha=0.7, lw=1)
    axt.plot(t_axis[:300], entry_count[:300], marker=".",
             color="green", alpha=0.8, lw=1)

    ax.set_xlabel("Time since 2017-01-02 00:00 (min)", fontsize=14)
    axt.set_ylabel("15-min-binned arrival count", fontsize=14, color="green")
    axt.tick_params(axis="y", labelcolor="green")
    ax.set_ylabel("15-min-averaged transit time", fontsize=14)


if mode == "arrival":

    ax.axhline(y=8, color="black")
    ax.plot(t_axis[:300], entry_count[:300], marker=".",
            color="green", alpha=0.7, label="Entry", lw=1)
    ax.plot(t_axis_arr[:300], arrivial_count[:300], marker=".",
            color="deeppink", alpha=0.7, label="Landing", lw=1)

    # ax.bar(t_axis[:300], entry_count[:300], width=1.3,
    #        color="green")

    # ax.bar(t_axis_arr[:300], arrivial_count[:300], width=1.3,
    #        color="purple")

    ax.set_xlabel("Time since 2017-01-02 00:00 (min)", fontsize=14)
    ax.set_ylabel("15-min-binned count", fontsize=14)
    ax.legend()


plt.tight_layout()
if savefig:
    plt.savefig(f"{savedir}/entry_count_vs_{mode}_ts_{year}.png", dpi=300)

if showfig:
    plt.show()
