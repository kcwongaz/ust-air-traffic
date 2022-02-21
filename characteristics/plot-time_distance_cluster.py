from matplotlib import axes
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fname = "/home/kc/Research/air_traffic/data/fr24_stat/time_distance_china_filtered.txt"
filters = {"lower_r": False, "upper_t": False}

sdir = "/home/kc/Research/air_traffic/figures/2022-02-22"

boxes = [(23.2, 23.6, 113.2, 113.4), (22.5, 24.5, 111, 111.2),
         (20.2, 21.2, 111, 111.2), (25, 25.5, 113, 115),
         (21.5, 22.9, 117, 117.5), (19.1, 20.1, 117.3, 117.5)]

sname = "time_distance"

# --------------------------------------------------------------------------- #
df = pd.read_csv(fname, header=0)
df = df.loc[df["delta_t_sec"] / 60 < 800]

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

if sname == "time_distance":
    fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(8, 5))
    for n, box in enumerate(boxes):

        ax = axes[int(n // 3), int(n % 3)]
        df_sub = df.loc[(df["lat_i"] >= box[0]) & (df["lat_i"] <= box[1]) &
                        (df["lon_i"] >= box[2]) & (df["lon_i"] <= box[3])]

        delta_r = df_sub["delta_r_km"].to_numpy()
        delta_t = df_sub["delta_t_sec"].to_numpy() / 60

        ax.scatter(delta_r, delta_t, s=20,
                   c="blue", marker="o", alpha=0.12)

        ax.set_ylim(0, 200)

        if n == 0:
            ax.set_xlabel("Distance (km)", fontsize=10)
            ax.set_ylabel("Time Difference (min)", fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{sdir}/{sname}_clusters_sameaxes.png", dpi=300)


elif sname == "speed_distance":
    fig, axes = plt.subplots(ncols=3, nrows=2, figsize=(8, 5))
    for n, box in enumerate(boxes):

        ax = axes[int(n // 3), int(n % 3)]
        df_sub = df.loc[(df["lat_i"] >= box[0]) & (df["lat_i"] <= box[1]) &
                        (df["lon_i"] >= box[2]) & (df["lon_i"] <= box[3])]

        df = df.loc[df["delta_t_sec"] > 0]
        delta_r = df_sub["delta_r_km"].to_numpy()
        delta_t = df_sub["delta_t_sec"].to_numpy() / 60
        speed = delta_r / delta_t

        ax.scatter(delta_r, speed, s=20,
                   c="red", marker="o", alpha=0.12)

        if n == 0:
            ax.set_xlabel("Distance (km)", fontsize=10)
            ax.set_ylabel("Average Speed (km/min)", fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{sdir}/{sname}_clusters.png", dpi=300)
