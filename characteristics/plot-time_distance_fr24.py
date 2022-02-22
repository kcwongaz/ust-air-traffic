import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import linregress


mode = "speed"
filters = {"upper_t": True}
years = [2017, 2018, 2020, 2021]

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

color = ["#bb9af7", "#7aa2f7", "#7dcfff", "#73daca",
         "#9ece6a", "#ff9e64", "#f7768e"]

fname = "/home/kc/Research/air_traffic/data/fr24_clean/time_distance_clean.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-02-22/"
sname = f"fr24_distance_{mode}_filtered.png"


# --------------------------------------------------------------------------- #
df_all = pd.read_csv(fname, header=0)
df_all["t_i"] = df_all["t_i"] + 8*3600  # Hong Kong time is UTC+8
timestamps = pd.to_datetime(df_all["t_f"], unit="s")

if filters["upper_t"]:
    df_all = df_all.loc[df_all["delta_t_sec"] / 60 < 800]


# --------------------------------------------------------------------------- #
if mode == "time":
    fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(8, 8))

    for j, yr in enumerate(years):

        i = (int(j // 2), int(j % 2))
        ax = axs[i]
        df = df_all.loc[timestamps.dt.year == yr]
        delta_r = df["delta_r_km"].to_numpy()
        delta_t = df["delta_t_sec"].to_numpy() / 60

        ax.scatter(delta_r, delta_t, s=20,
                   c="blue", marker="o", alpha=0.15)

        if j == 0:
            ax.set_xlabel("Distance (km)", fontsize=10)
            ax.set_ylabel("Time Difference (min)", fontsize=10)

        ax.set_xlim(0, 600)
        ax.set_ylim(0, 500)

        ax.tick_params(which="both", direction="in", labelsize=8)
        ax.set_title(yr, fontsize=12)

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
elif mode == "inv_speed":
    fig, axs = plt.subplots(ncols=2, nrows=2, figsize=(8, 8))

    for yr, window in enumerate(years):

        i = (int(yr // 2), int(yr % 2))
        ax = axs[i]
        df = df_all.loc[df_all["hour"].isin(window)]
        df = df.loc[df["delta_r_km"] > 0]

        delta_r = df["delta_r_km"].to_numpy()
        delta_t = df["delta_t_sec"].to_numpy() / 60

        t_over_d = delta_t / delta_r

        ax.scatter(delta_r, t_over_d, s=20,
                   c="red", marker="o", alpha=0.12)

        if yr == 0:
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

    for j, yr in enumerate(years):

        i = (int(j // 2), int(j % 2))
        ax = axs[i]
        df = df_all.loc[timestamps.dt.year == yr]
        df = df.loc[df["delta_t_sec"] > 0]

        delta_r = df["delta_r_km"].to_numpy()
        delta_t = df["delta_t_sec"].to_numpy() / 60
        speed = delta_r / delta_t

        ax.scatter(delta_r, speed, s=20,
                   c="crimson", marker="o", alpha=0.15)

        if j == 0:
            ax.set_xlabel("Distance (km)", fontsize=10)
            ax.set_ylabel("Average Speed (km/min)", fontsize=10)

        # ax.set_xlim(1e-2, 800)
        # ax.set_ylim(1e-3, 20)
        # ax.set_yscale("log")
        # ax.set_xscale("log")

        ax.set_xlim(0, 800)
        ax.set_ylim(0, 20)

        ax.tick_params(which="both", direction="in", labelsize=8)
        ax.set_title(yr, fontsize=12)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.35)
    plt.savefig(f"{sdir}/{sname}", dpi=300)

# --------------------------------------------------------------------------- #
else:
    print(f"Don't know what {mode} means.")
