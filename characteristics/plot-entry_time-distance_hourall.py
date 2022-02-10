import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import linregress


# ["grid", "linear", "speed", "overlap"]
mode = "speed"
filters = {"upper_t": True}
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
sname = f"time_distance_hour_{mode}_noramlscale.png"


# --------------------------------------------------------------------------- #
df_all = pd.read_csv(fname, header=0)
df_all["t_i"] = df_all["t_i"] + 8*3600  # Hong Kong time is UTC+8
timestamps = pd.to_datetime(df_all["t_i"], unit="s")
df_all = df_all.assign(hour=timestamps.dt.hour)

if filters["upper_t"]:
    df_all = df_all.loc[df_all["delta_t_sec"] / 60 < 800]


# --------------------------------------------------------------------------- #
if mode == "grid" or mode == "linear":
    fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(8, 8))

    for n, window in enumerate(time_windows):

        i = (int(n // 2), int(n % 2))
        ax = axs[i]
        df = df_all.loc[df_all["hour"].isin(window)]
        delta_r = df["delta_r_km"].to_numpy()
        delta_t = df["delta_t_sec"].to_numpy() / 60

        ax.scatter(delta_r, delta_t, s=20,
                   c="red", marker="o", alpha=0.12)

        if n == 0:
            ax.set_xlabel("Distance (km)", fontsize=10)
            ax.set_ylabel("Time Difference (min)", fontsize=10)

        ax.set_xlim(0, 500)
        ax.set_ylim(0, 120)

        ax.tick_params(which="both", direction="in", labelsize=8)
        ax.set_title(f"{window[0]}:00 - {window[-1]}:59 ({len(df)})",
                     fontsize=12)

        # linear fit
        if mode == "linear":
            slope, intercept, r, p, se = linregress(delta_r, delta_t)

            x_axis = np.arange(0, 500, 0.1)
            y_axis = slope * x_axis + intercept
            ax.plot(x_axis, y_axis, color="black", linestyle="--")

            ax.annotate(rf"$a = {round(slope, 2)}$", (400, 110), fontsize=9)
            ax.annotate(rf"$b = {round(intercept, 2)}$", (400, 103), fontsize=9)
            ax.annotate(rf"$r^2 = {round(r*r, 2)}$", (400, 96), fontsize=9)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.35)
    plt.savefig(f"{sdir}/{sname}", dpi=300)
    # plt.show()

# --------------------------------------------------------------------------- #
elif mode == "overlap":
    fig, ax = plt.subplots()

    for n, window in enumerate(time_windows):

        df = df_all.loc[df_all["hour"].isin(window)]
        delta_r = df["delta_r_km"].to_numpy()
        delta_t = df["delta_t_sec"].to_numpy() / 60

        ax.scatter(delta_r, delta_t, s=20, c=color[2*n % 7],
                   marker="o", alpha=0.50)

        # For legend
        ax.scatter([], [], s=20, color=color[2*n % 7], marker="o", alpha=0.50,
                   label=f"{window[0]}:00 - {window[-1]}:59")

    ax.set_xlabel("Distance (km)", fontsize=20)
    ax.set_ylabel("Time Difference (min)", fontsize=20)
    ax.set_xlim(0, 600)
    ax.set_ylim(0, 600)

    ax.tick_params(which="both", direction="in", labelsize=14)
    ax.legend(loc="upper right", fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{sdir}/{sname}", dpi=300)
    # plt.show()


# --------------------------------------------------------------------------- #
elif mode == "inv_speed":
    fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(8, 8))

    for n, window in enumerate(time_windows):

        i = (int(n // 2), int(n % 2))
        ax = axs[i]
        df = df_all.loc[df_all["hour"].isin(window)]
        df = df.loc[df["delta_r_km"] > 0]

        delta_r = df["delta_r_km"].to_numpy()
        delta_t = df["delta_t_sec"].to_numpy() / 60

        t_over_d = delta_t / delta_r

        ax.scatter(delta_r, t_over_d, s=20,
                   c="red", marker="o", alpha=0.12)

        if n == 0:
            ax.set_xlabel("Distance (km)", fontsize=10)
            ax.set_ylabel("Inverse Average Speed (min/km)", fontsize=10)

        # ax.set_xlim(0, 500)
        ax.set_ylim(0, 2.5)
        # ax.set_yscale("log")
        # ax.set_xscale("log")

        ax.tick_params(which="both", direction="in", labelsize=8)
        ax.set_title(f"{window[0]}:00 - {window[-1]}:59 ({len(df)})",
                     fontsize=12)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.35)
    plt.savefig(f"{sdir}/{sname}", dpi=300)


# --------------------------------------------------------------------------- #
elif mode == "speed":
    fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(8, 8))

    for n, window in enumerate(time_windows):

        i = (int(n // 2), int(n % 2))
        ax = axs[i]
        df = df_all.loc[df_all["hour"].isin(window)]
        df = df.loc[df["delta_t_sec"] > 0]

        delta_r = df["delta_r_km"].to_numpy()
        delta_t = df["delta_t_sec"].to_numpy() / 60

        d_over_t = delta_r / delta_t

        ax.scatter(delta_r, d_over_t, s=20,
                   c="red", marker="o", alpha=0.12)

        if n == 0:
            ax.set_xlabel("Distance (km)", fontsize=10)
            ax.set_ylabel("Average Speed (km/min)", fontsize=10)

        ax.set_xlim(0, 550)
        ax.set_ylim(0, 15)
        # ax.set_yscale("log")
        # ax.set_xscale("log")

        ax.tick_params(which="both", direction="in", labelsize=8)
        ax.set_title(f"{window[0]}:00 - {window[-1]}:59 ({len(df)})",
                     fontsize=12)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.35)
    plt.savefig(f"{sdir}/{sname}", dpi=300)

# --------------------------------------------------------------------------- #
else:
    print(f"Don't know what {mode} means.")
