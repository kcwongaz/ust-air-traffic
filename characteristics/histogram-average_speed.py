import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import linregress


# ["normal", "centered", "stacked"]
mode = "stacked"
filters = {"upper_t": True}
fits = {"lower": False, "upper": True,
        "lower_linear": True, "upper_sqrt": True}

time_windows = [np.arange(1, 8), np.arange(8, 15),
                np.arange(15, 19), np.append(np.arange(19, 24), 0)]

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)


fname = "/home/kc/Research/air_traffic/data/opensky_clean/time_distance.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-01-25"
sname = f"speed_fluctation_{mode}.png"


# --------------------------------------------------------------------------- #
df_all = pd.read_csv(fname, header=0)
df_all["t_i"] = df_all["t_i"] + 8*3600  # Hong Kong time is UTC+8
timestamps = pd.to_datetime(df_all["t_i"], unit="s")
df_all = df_all.assign(hour=timestamps.dt.hour)

if filters["upper_t"]:
    df_all = df_all.loc[df_all["delta_t_sec"] / 60 < 800]

# d_bins = np.arange(0, 600, 50)

# --------------------------------------------------------------------------- #
if mode == "grid":
    fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(8, 8))

    for n, window in enumerate(time_windows):

        i = (int(n // 2), int(n % 2))
        ax = axs[i]
        df = df_all.loc[df_all["hour"].isin(window)]
        df = df.loc[df["delta_r_km"] > 0]
        df = df.loc[df["delta_t_sec"] > 0]

        delta_r = df["delta_r_km"].to_numpy()
        delta_t = df["delta_t_sec"].to_numpy() / 60

        ind = np.where(delta_r >= 10)
        delta_r = delta_r[ind]
        delta_t = delta_t[ind]
        d_over_t = delta_r / delta_t

        alpha = 0.5
        amp = (np.exp(np.mean(np.log(d_over_t) - alpha*np.log(delta_r))))
        offset = amp * (delta_r ** alpha)
        diff = d_over_t - offset

# --------------------------------------------------------------------------- #
        ax.hist(diff, bins=50, range=(-4, 4), density=True)

        if mode == "centered":
            pass

# --------------------------------------------------------------------------- #
        if n == 0:
            ax.set_xlabel(r"Speed Deivation $\delta v = v - \bar{v}(d)$ (km/min)",
                          fontsize=10)
            ax.set_ylabel("P(v)", fontsize=10)

        ax.tick_params(which="both", direction="in", labelsize=8)
        ax.set_title(f"{window[0]}:00 - {window[-1]}:59 ({len(df)})",
                     fontsize=12)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.35)


# --------------------------------------------------------------------------- #
elif mode == "stacked" or "centered":
    fig, ax = plt.subplots()
    colors = ["orange", "green", "red", "blue"]

    for n, window in enumerate(time_windows[::-1]):

        df = df_all.loc[df_all["hour"].isin(window)]
        df = df.loc[df["delta_r_km"] > 0]
        df = df.loc[df["delta_t_sec"] > 0]

        delta_r = df["delta_r_km"].to_numpy()
        delta_t = df["delta_t_sec"].to_numpy() / 60

        ind = np.where(delta_r >= 10)
        delta_r = delta_r[ind]
        delta_t = delta_t[ind]
        d_over_t = delta_r / delta_t

        alpha = 0.5
        amp = (np.exp(np.mean(np.log(d_over_t) - alpha*np.log(delta_r))))
        offset = amp * (delta_r ** alpha)
        diff = d_over_t - offset

        # Centering
        # if mode == "centered":
        #     diff -= np.mean(diff)

        print(colors[n])
        ax.hist(diff, bins=100, range=(-4, 4), density=True, alpha=0.45,
                align="mid", color=colors[n],
                label=f"{window[0]}:00 - {window[-1]}:59")

    ax.set_xlabel(r"Speed Deivation $\delta v = v - \bar{v}(d)$ (km/min)",
                  fontsize=10)
    ax.set_ylabel("P(v)", fontsize=10)
    ax.tick_params(which="both", direction="in", labelsize=8)
    ax.legend()

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.35)


plt.savefig(f"{sdir}/{sname}", dpi=300)
