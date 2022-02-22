from matplotlib import axes
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fname = "/home/kc/Research/air_traffic/data/fr24_clean/time_distance_clean.txt"
filters = {"lower_r": False, "upper_t": False}

sdir = "/home/kc/Research/air_traffic/figures/2022-02-22"

# boxes = [(23.2, 23.6, 113.2, 113.4), (22.5, 24.5, 111, 111.2),
#          (20.2, 21.2, 111, 111.2), (25, 25.5, 113, 115),
#          (21.5, 22.9, 117, 117.5), (19.1, 20.1, 117.3, 117.5),
#          (19, 19.2, 112, 113.2), (19, 19.2, 113.9, 114.8)]

boxes = [(23.2, 23.6, 113.2, 113.4), (22.5, 24.5, 111, 111.2),
         (20.2, 21.2, 111, 111.2), (25, 25.5, 113, 115),
         (21.5, 25, 117, 117.5), (19.1, 20.1, 117.3, 117.5),
         (19, 19.2, 111.8, 113.5), (19, 19.2, 113.5, 116.2)]

colors = ["darkviolet", "deeppink", "darkorange", "limegreen",
          "teal", "mediumblue", "goldenrod", "crimson"]

sname = "speed_distance"

# --------------------------------------------------------------------------- #
df = pd.read_csv(fname, header=0)
# df = df.loc[df["delta_t_sec"] / 60 < 800]

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

if sname == "time_distance":
    fig, axes = plt.subplots(ncols=4, nrows=2, figsize=(8, 4))
    for n, box in enumerate(boxes):

        ax = axes[int(n // 4), int(n % 4)]
        df_sub = df.loc[(df["lat_i"] >= box[0]) & (df["lat_i"] <= box[1]) &
                        (df["lon_i"] >= box[2]) & (df["lon_i"] <= box[3])]

        delta_r = df_sub["delta_r_km"].to_numpy()
        delta_t = df_sub["delta_t_sec"].to_numpy() / 60

        ax.scatter(delta_r, delta_t, s=10,
                   c=colors[n], marker="o", alpha=0.15)

        ax.set_ylim(0, 200)

        if n == 0:
            ax.set_xlabel("Distance (km)", fontsize=10)
            ax.set_ylabel("Time Difference (min)", fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{sdir}/{sname}_clusters_sameaxes.png", dpi=300)


elif sname == "speed_distance":
    fig, axes = plt.subplots(ncols=4, nrows=2, figsize=(8, 4))
    for n, box in enumerate(boxes):

        ax = axes[int(n // 4), int(n % 4)]
        df_sub = df.loc[(df["lat_i"] >= box[0]) & (df["lat_i"] <= box[1]) &
                        (df["lon_i"] >= box[2]) & (df["lon_i"] <= box[3])]

        df = df.loc[df["delta_t_sec"] > 0]
        delta_r = df_sub["delta_r_km"].to_numpy()
        delta_t = df_sub["delta_t_sec"].to_numpy() / 60
        speed = delta_r / delta_t

        ax.scatter(delta_r, speed, s=10,
                   c=colors[n], marker="o", alpha=0.15)

        if n == 0:
            ax.set_xlabel("Distance (km)", fontsize=10)
            ax.set_ylabel("Average Speed (km/min)", fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{sdir}/{sname}_clusters.png", dpi=300)


elif sname == "speed_distribution":
    fig, axes = plt.subplots(ncols=4, nrows=2, figsize=(8, 4))
    for n, box in enumerate(boxes):

        ax = axes[int(n // 4), int(n % 4)]
        df_sub = df.loc[(df["lat_i"] >= box[0]) & (df["lat_i"] <= box[1]) &
                        (df["lon_i"] >= box[2]) & (df["lon_i"] <= box[3])]

        df = df.loc[df["delta_t_sec"] > 0]
        delta_r = df_sub["delta_r_km"].to_numpy()
        delta_t = df_sub["delta_t_sec"].to_numpy() / 60
        speed = delta_r / delta_t

        ax.hist(speed, bins=50, range=(0, 15), color=colors[n])
        ax.set_xlim(0, 15)
        ax.set_xticks(np.arange(0, 16, 5))

        if n == 0:
            ax.set_xlabel("Average Speed (km/min)", fontsize=10)
            ax.set_ylabel("Count", fontsize=10)

    plt.tight_layout()
    plt.savefig(f"{sdir}/{sname}_clusters.png", dpi=300)
