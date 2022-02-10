import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fname = "/home/kc/Research/air_traffic/data/opensky_clean/time_distance.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-01-18"

filters = {"upper_t": True}

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)
# ---------------------------------------------------------------------------- # 
df_all = pd.read_csv(fname, header=0)
timestamps = pd.to_datetime(df_all["t_i"], unit="s")
df_all = df_all.assign(day_of_week = timestamps.dt.day_of_week)

if filters["upper_t"]:
    df_all = df_all.loc[df_all["delta_t_sec"] / 60 < 800]


for day in range(7):

    df = df_all.loc[df_all["day_of_week"] == day]
    delta_r = df["delta_r_km"].to_numpy()
    delta_t = df["delta_t_sec"].to_numpy() / 60

    day_name = pd.to_datetime(df["t_i"].iloc[0], unit="s").day_name()
    sname = f"time_distance_{day_name}.png"

    fig, ax = plt.subplots()
    ax.scatter(delta_r, delta_t, s=20,
            c="blue", marker="o", alpha=0.12)
        

    ax.set_xlabel("Distance (km)", fontsize=20)
    ax.set_ylabel("Time Difference (min)", fontsize=20)
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 100)

    ax.tick_params(which="both", direction="in", labelsize=14)
    ax.set_title(f"{day_name} ({len(df)})", fontsize=20)

    plt.tight_layout()
    plt.savefig(f"{sdir}/{sname}", dpi=300)
