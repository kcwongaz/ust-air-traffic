import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fname = "/home/kc/Research/air_traffic/data/fr24_clean/time_distance.txt"

sdir = "/home/kc/Research/air_traffic/figures/2022-03-01"

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)


# --------------------------------------------------------------------------- #
def partition(timeseries, part_size, window):

    n = round(part_size / window)
    total_len = int(len(timeseries) / n)

    partitioned = [timeseries[k*n:(k+1)*n] for k in range(total_len)]
    return partitioned


def autocorr(timeseries, dt, period):

    n = round(period / dt)
    n_period = int(len(timeseries) / n)
    c_matrix = np.zeros((n, n))

    mean = np.zeros(n)
    var = np.zeros(n)
    for i in range(n):
        sample = [timeseries[m*n + i] for m in range(n_period-1)]
        mean[i] = np.mean(sample)
        var[i] = np.var(sample) * len(sample) / (len(sample) - 1)

    for i in range(n):
        for j in range(n):
            sample = [timeseries[m*n + i] * timeseries[m*n + i + j]
                      for m in range(n_period-1)]

            # c_matrix[i, j] = np.mean(sample)

            j_mod = (i+j) % n
            c_matrix[i, j] = np.mean(sample) - mean[i]*mean[j_mod]
            c_matrix[i, j] /= np.sqrt(var[i] * var[j_mod])

    return c_matrix


# --------------------------------------------------------------------------- #
# Time window size to commute the Possion rate (in unit of second)
window = 60 * 15
year = 2017


df = pd.read_csv(fname, header=0)
df["year"] = pd.to_datetime(df["t_f"], unit="s").dt.year
df["month"] = pd.to_datetime(df["t_f"], unit="s").dt.month
df = df.loc[df["year"] == year]
# df = df[df["month"].isin(range(1, 6))]


arrivial_time = df["t_f"].to_numpy()
arrivial_time.sort()
print(pd.to_datetime(df["t_f"].iloc[0], unit="s"))


# t0 = pd.to_datetime(f"{year}-01-01", format="%Y-%m-%d").timestamp()
# t_axis = np.arange(t0 + window, arrivial_time[-1], window)
# bins = np.insert(t_axis, 0, t0)
# rate, _ = np.histogram(arrivial_time, bins)


t_axis = np.arange(arrivial_time[0] + window, arrivial_time[-1], window)
bins = np.insert(t_axis, 0, arrivial_time[0])
rate, _ = np.histogram(arrivial_time, bins)


fig, ax = plt.subplots()

# # --------------------------------------------------------------------------- #
# rate_day = partition(rate, 3600*24, window)
# day_axis = np.arange(len(rate_day[0])) / 4

# cmap = plt.cm.get_cmap("rainbow", 20)
# for i, curve in enumerate(rate_day):

#     if np.sum(curve) == 0:
#         continue
#     ax.plot(day_axis, curve, color=cmap(i % 20), alpha=0.75)

# ax.set_xticks(range(0, 25, 2))
# ax.set_xlabel("Time mod 24 Hour (Hour)", fontsize=14)
# ax.set_ylabel("Arrivial Count", fontsize=14)
# ax.set_title(f"{year}", fontsize=18)
# ax.set_ylim(-0.5, 12)
# ax.vlines(16.5, ymin=-0.5, ymax=12, color="black", lw=2.5)

# plt.savefig(f"{sdir}/timeseries_{year}.png", dpi=300)
# plt.tight_layout()

# --------------------------------------------------------------------------- #
r_avg = np.average(rate)
# print(r_avg)
# rate = rate - r_avg


# spectrum = np.abs(np.fft.rfft(rate))
# spectrum /= np.max(spectrum)
# freq = np.fft.rfftfreq(len(rate), d=window) * 3600
# period = 1/(freq)

# # Frequency domain
# ax.plot(freq, spectrum, color="blue")
# ax.set_xlabel("Frequency $f$ (1/Hour)", fontsize=16)
# ax.set_ylabel(r"Spectral Component $|\tilde{\lambda}(f)|$", fontsize=16)

# plt.savefig(f"{sdir}/spectrum_frequency_{year}.png", dpi=300)


# Period domain
# n = 50
# ax.plot(period[n:], spectrum[n:], color="blue")
# ax.set_xlabel("Period $T$ (Hour)", fontsize=16)
# ax.set_ylabel(r"Spectral Component $|\tilde{\lambda}(T)|$", fontsize=16)

# ax.set_title(f"Fourier Spectrum ({year})", fontsize=20)
# plt.savefig(f"{sdir}/spectrum_period_{year}.png", dpi=300)


# --------------------------------------------------------------------------- #

corr = autocorr(rate, dt=window, period=86400)
t_axis = np.arange(0, 24, window/3600)
# ax.plot(t_axis, corr[0])


# for i in range(len(corr[0])):
#     ax.plot(t_axis, corr[i])

im = ax.imshow(corr, cmap="plasma", extent=(0, 24, 0, 24), origin="lower",
               vmin=0, vmax=1)

ax.set_xlabel("Time $t$ (Hours from 00:00)", fontsize=12)
ax.set_ylabel("Forward Time $T$ (Hour)", fontsize=12)

ax.set_xticks(range(0, 25, 2))
ax.set_yticks(range(0, 25, 2))
ax.set_title(f"Arrivial Rate Autocorrection ({year})", fontsize=14)

cax = plt.axes([0.91, 0.15, 0.02, 0.7])
plt.colorbar(im, cax)

plt.tight_layout()
# plt.savefig(f"{sdir}/autocorrection_{year}.png", dpi=300)


# --------------------------------------------------------------------------- #
plt.show()
