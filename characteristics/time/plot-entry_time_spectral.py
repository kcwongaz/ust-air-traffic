import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

from scipy.stats import binned_statistic
from moving_avg import moving_avg


fname = "/home/kc/Research/air_traffic/data/fr24_clean/stat_145-165_clustered.txt"
savedir = "/home/kc/Research/air_traffic/figures/2022-03-22"

year = 2017
n_cluster = 5

window = 0.25
bins = np.arange(0, 24.1, window)

statistic = "mean"
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


# HKT is UTC+8
second = (df["t_i"].to_numpy() + 8*3600)
hour = second / 3600
delta_t = df["delta_t_sec"].to_numpy() / 60
cluster = df["cluster"].to_numpy()


delta_avg, t_axis = moving_avg(delta_t, second, dt=15*60,
                               start_hour=-1)
t_axis -= t_axis[0]

# Remove the nan's by interpolation
nans, x = nan_helper(delta_avg)
delta_avg1 = delta_avg.copy()
# delta_avg1[nans] = np.interp(x(nans), x(~nans), delta_avg1[~nans])
delta_avg1[nans] = 0


spectrum = np.abs(np.fft.rfft(delta_avg1 - np.average(delta_avg1)))
spectrum /= np.max(spectrum)
freq = np.fft.rfftfreq(len(delta_avg1), d=15*60) * 3600
# freq = np.fft.rfftfreq(len(delta_avg1))
period = 1 / freq


# --------------------------------------------------------------------------- #
fig, ax = plt.subplots()

# ax.plot(period[40:], spectrum[40:], color="blue", lw=1)
ax.plot(freq, spectrum, color="blue", lw=1)


# ax.plot(t_axis[:500], delta_avg1[:500], marker="o", color="red")
# ax.plot(t_axis[:500], delta_avg[:500], marker="o", color="blue")

# ax.set_xticks(np.arange(0, 25, 2))

# ax.set_xlabel("Period (Hour)", fontsize=14)
ax.set_xlabel("Frequency (1/Hour)", fontsize=14)
ax.set_ylabel("Fourier Spectrum", fontsize=14)

plt.tight_layout()
if savefig:
    plt.savefig(f"{savedir}/spectrum_{statistic}_{year}_freq.png", dpi=300)

if showfig:
    plt.show()
