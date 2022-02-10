import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import linregress


mode = "linear"
filters = {"upper_t": True}

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

color = ["#bb9af7", "#7aa2f7", "#7dcfff", "#73daca",
         "#9ece6a", "#ff9e64", "#f7768e"]

fname = "/home/kc/Research/air_traffic/data/opensky_clean/time_distance.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-01-18"
sname = f"time_distance_week_{mode}.png"

# --------------------------------------------------------------------------- #
df_all = pd.read_csv(fname, header=0)
timestamps = pd.to_datetime(df_all["t_i"], unit="s")
df_all = df_all.assign(day_of_week=timestamps.dt.day_of_week)

if filters["upper_t"]:
    df_all = df_all.loc[df_all["delta_t_sec"] / 60 < 800]


# --------------------------------------------------------------------------- #
if mode == "grid" or mode == "linear" or mode == "linear0":
    fig, axs = plt.subplots(ncols=4, nrows=2, figsize=(13, 6))
    axs[-1, -1].axis("off")

    for day in range(7):

        i = (int(day // 4), int(day % 4))
        ax = axs[i]
        df = df_all.loc[df_all["day_of_week"] == day]
        delta_r = df["delta_r_km"].to_numpy()
        delta_t = df["delta_t_sec"].to_numpy() / 60

        day_name = pd.to_datetime(df["t_i"].iloc[0], unit="s").day_name()
        ax.scatter(delta_r, delta_t, s=20,
                   c="blue", marker="o", alpha=0.12)

        if day == 0:
            ax.set_xlabel("Distance (km)", fontsize=10)
            ax.set_ylabel("Time Difference (min)", fontsize=10)

        ax.set_xlim(0, 500)
        ax.set_ylim(0, 120)

        ax.tick_params(which="both", direction="in", labelsize=8)
        ax.set_title(f"{day_name} ({len(df)})", fontsize=12)

        # linear fit
        if mode == "linear":
            # df = df.loc[df["delta_t_sec"] / 60 <= 80]
            # delta_r = df["delta_r_km"].to_numpy()
            # delta_t = df["delta_t_sec"].to_numpy() / 60

            slope, intercept, r, p, se = linregress(delta_r, delta_t)

            x_axis = np.arange(0, 500, 0.1)
            y_axis = slope * x_axis + intercept
            ax.plot(x_axis, y_axis, color="black", linestyle="--")
           
            ax.annotate(rf"$a = {round(slope, 2)}$", (385, 110), fontsize=9)
            ax.annotate(rf"$b = {round(intercept, 2)}$", (385, 100), fontsize=9)
            ax.annotate(rf"$r^2 = {round(r*r, 2)}$", (385, 90), fontsize=9)

        # Zero intercept fit
        elif mode == "linear0":
            # df = df.loc[df["delta_t_sec"] <= 80]
            # delta_r = df["delta_r_km"].to_numpy()
            # delta_t = df["delta_t_sec"].to_numpy()

            slope, sum_res, _, _ = np.linalg.lstsq(delta_r[:, np.newaxis], delta_t)
            sum_seq = np.sum((delta_t - np.average(delta_t))**2)
            r2 = 1 - sum_res[0] / sum_seq

            x_axis = np.arange(0, 500, 0.1)
            y_axis = slope * x_axis
            ax.plot(x_axis, y_axis, color="black", linestyle="--")
            ax.annotate(rf"$a = {round(slope[0], 2)}$", (385, 110), fontsize=9)
            ax.annotate(rf"$r^2 = {round(r2, 2)}$", (385, 100), fontsize=9)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.5)
    plt.savefig(f"{sdir}/{sname}", dpi=300)
    # plt.show()

# --------------------------------------------------------------------------- #
elif mode == "overlap":
    fig, ax = plt.subplots()

    for day in range(7):

        df = df_all.loc[df_all["day_of_week"] == day]
        delta_r = df["delta_r_km"].to_numpy()
        delta_t = df["delta_t_sec"].to_numpy() / 60

        day_name = pd.to_datetime(df["t_i"].iloc[0], unit="s").day_name()

        ax.scatter(delta_r, delta_t, s=20, c=color[day], marker="o",
                   alpha=0.50)

        # For legend
        ax.scatter([], [], s=20, color=color[day], marker="o", alpha=0.50,
                   label=day_name)

    ax.set_xlabel("Distance (km)", fontsize=20)
    ax.set_ylabel("Time Difference (min)", fontsize=20)
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 120)

    ax.tick_params(which="both", direction="in", labelsize=14)
    ax.legend(loc="upper right", fontsize=8)

    plt.tight_layout()
    plt.savefig(f"{sdir}/{sname}", dpi=300)
    # plt.show()


# --------------------------------------------------------------------------- #
else:
    print(f"Don't know what {mode} means.")
