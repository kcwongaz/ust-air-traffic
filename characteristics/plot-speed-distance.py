import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import linregress


# ["grid", "linear", "speed", "overlap"]
mode = "speed"
filters = {"upper_t": True}
fits = {"lower": False, "upper": True,
        "lower_linear": True, "upper_sqrt": True}

time_windows = [np.arange(1, 8), np.arange(8, 15),
                np.arange(15, 19), np.append(np.arange(19, 24), 0)]

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

color = ["#bb9af7", "#7aa2f7", "#7dcfff", "#73daca",
         "#9ece6a", "#ff9e64", "#f7768e"]

fname = "/home/kc/Research/air_traffic/data/opensky_clean/time_distance.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-01-25"
sname = f"time_distance_log_{mode}_allfits.png"


# --------------------------------------------------------------------------- #
df_all = pd.read_csv(fname, header=0)
df_all["t_i"] = df_all["t_i"] + 8*3600  # Hong Kong time is UTC+8
timestamps = pd.to_datetime(df_all["t_i"], unit="s")
df_all = df_all.assign(hour=timestamps.dt.hour)

if filters["upper_t"]:
    df_all = df_all.loc[df_all["delta_t_sec"] / 60 < 800]

# --------------------------------------------------------------------------- #
if mode == "speed":
    fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(8, 8))

    for n, window in enumerate(time_windows):

        i = (int(n // 2), int(n % 2))
        ax = axs[i]
        df = df_all.loc[df_all["hour"].isin(window)]
        df = df.loc[df["delta_r_km"] > 0]
        df = df.loc[df["delta_t_sec"] > 0]

        delta_r = df["delta_r_km"].to_numpy()
        delta_t = df["delta_t_sec"].to_numpy() / 60

        d_over_t = delta_r / delta_t

        ax.scatter(delta_r, d_over_t, s=20,
                   c="red", marker="o", alpha=0.12)

        if n == 0:
            ax.set_xlabel("Distance $d$ (km)", fontsize=10)
            ax.set_ylabel("Average Speed $v$ (km/min)", fontsize=10)

        ax.set_xlim(0.05, 600)
        ax.set_ylim(0.01, 20)
        ax.set_yscale("log")
        ax.set_xscale("log")

        ax.tick_params(which="both", direction="in", labelsize=8)
        ax.set_title(f"{window[0]}:00 - {window[-1]}:59 ({len(df)})",
                     fontsize=12)

        # linear fit
        if fits["lower"]:
            ind = np.where(delta_r <= 1)
            if len(ind[0]) > 1:

                logx = np.log(delta_r[ind])
                logy = np.log(d_over_t[ind])
                slope, intercept, r, p, se = linregress(logx, logy)

                x_axis = np.arange(0.05, 5, 0.01)
                y_axis = np.exp(intercept) * (x_axis ** slope)
                ax.plot(x_axis, y_axis, color="black", linestyle="--")

                ax.annotate(rf"$a = {round(slope, 2)}$", (400, 110), fontsize=9)
                ax.annotate(rf"$r^2 = {round(r*r, 2)}$", (400, 96), fontsize=9)

        if fits["lower_linear"]:
            x_axis = np.arange(0.05, 5, 0.01)
            y_axis = 0.2 * x_axis
            ax.plot(x_axis, y_axis, color="black", linestyle="--")
            ax.annotate(rf"$v = 0.2 d$", (0.8, 0.08),
                        fontsize=11, color="red")

        if fits["upper"]:
            ind = np.where(delta_r >= 10)

            logx = np.log(delta_r[ind])
            logy = np.log(d_over_t[ind])
            slope, intercept, r, p, se = linregress(logx, logy)

            x_axis = np.arange(10, 600, 0.1)
            y_axis = np.exp(intercept) * (x_axis ** slope)
            ax.plot(x_axis, y_axis, color="black", linestyle="--")

            amp = round(np.exp(intercept), 3)
            alpha = round(slope, 3)

            ax.annotate(rf"$v = {amp} \cdot d^{{{alpha}}}$", (10, 10),
                        fontsize=11)


        if fits["upper_sqrt"]:
            ind = np.where(delta_r >= 10)
            logx = np.log(delta_r[ind])
            logy = np.log(d_over_t[ind])

            alpha = 0.5
            amp = (np.exp(np.mean(logy - alpha*logx)))

            x_axis = np.arange(10, 600, 0.1)
            y_axis = amp * (x_axis ** alpha)
            ax.plot(x_axis, y_axis, color="blue", linestyle="--")

            amp = round(amp, 3)
            ax.annotate(rf"$v = {amp} \cdot \sqrt{{t}}$", (20, 0.8),
                        fontsize=11, color="blue")

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.35)
    plt.savefig(f"{sdir}/{sname}", dpi=300)

# --------------------------------------------------------------------------- #
else:
    print(f"Don't know what {mode} means.")
