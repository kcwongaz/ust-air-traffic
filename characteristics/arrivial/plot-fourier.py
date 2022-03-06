import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from arrivial_rate import arrivial_rate


fname = "/home/kc/Research/air_traffic/data/fr24_clean/time_distance.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-03-01"

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

dt = 60 * 15
year = 2018

# Frequency domain or period domain; ["freq", "period"]
mode = "period"

# The number of largest period Fourier componemt omitted
# 0 to keep all components
f_omit = 0


remove_avg = True
save_fig = False

# --------------------------------------------------------------------------- #
# Read data

df = pd.read_csv(fname, header=0)
df["year"] = pd.to_datetime(df["t_f"], unit="s").dt.year
df["month"] = pd.to_datetime(df["t_f"], unit="s").dt.month
df = df.loc[df["year"] == year]
df = df[df["month"].isin([3])]

arr_times = df["t_f"].to_numpy()
lambda_t, t_axis = arrivial_rate(arr_times, dt, start_hour=16, start_by="cut")


# --------------------------------------------------------------------------- #
# Draw
fig, ax = plt.subplots()

# Remove average
if remove_avg:
    lambda_avg = np.average(lambda_t)
    lambda_t = lambda_t - lambda_avg

# Copmute Fourier spectrum
spectrum = np.abs(np.fft.rfft(lambda_t))
spectrum /= np.max(spectrum)
freq = np.fft.rfftfreq(len(lambda_t), d=dt) * 3600


# Frequency domain
if mode == "freq":
    ax.plot(freq, spectrum, color="blue")
    ax.set_xlabel("Frequency $f$ (1/Hour)", fontsize=16)
    ax.set_ylabel(r"Spectral Component $|\tilde{\lambda}(f)|$", fontsize=16)

    if save_fig:
        plt.savefig(f"{sdir}/spectrum_frequency_{year}.png", dpi=300)


# Period domain
if mode == "period":
    period = 1 / freq

    ax.plot(period[f_omit:], spectrum[f_omit:], color="blue")
    ax.set_xlabel("Period $T$ (Hour)", fontsize=16)
    ax.set_ylabel(r"Spectral Component $|\tilde{\lambda}(T)|$", fontsize=16)

    ax.set_title(f"Fourier Spectrum ({year})", fontsize=20)

    if save_fig:
        plt.savefig(f"{sdir}/spectrum_period_{year}.png", dpi=300)


# --------------------------------------------------------------------------- #
plt.show()
