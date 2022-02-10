import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fname = "/home/kc/Research/air_traffic/data/opensky_clean/time_distance.txt"
sdir = "/home/kc/Research/air_traffic/figures/2022-01-18"

filters = {"upper_t": True}
time_windows = [np.arange(1, 8), np.arange(8, 15),
                np.arange(15, 19), np.append(np.arange(19, 24), 0)]

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)
# --------------------------------------------------------------------------- #
df_all = pd.read_csv(fname, header=0)
df_all["t_i"] = df_all["t_i"] + 8*3600  # Hong Kong time is UTC+8
timestamps = pd.to_datetime(df_all["t_i"], unit="s")
df_all = df_all.assign(hour=timestamps.dt.hour)

if filters["upper_t"]:
    df_all = df_all.loc[df_all["delta_t_sec"] / 60 < 800]


for i, window in enumerate(time_windows):

    df = df_all.loc[df_all["hour"].isin(window)]
    delta_r = df["delta_r_km"].to_numpy()
    delta_t = df["delta_t_sec"].to_numpy() / 60

    sname = f"time_distance_hour_{window[0]}-{window[-1]}.png"

    fig, ax = plt.subplots()
    ax.scatter(delta_r, delta_t, s=20,
               c="red", marker="o", alpha=0.12)

    ax.set_xlabel("Distance (km)", fontsize=20)
    ax.set_ylabel("Time Difference (min)", fontsize=20)
    ax.set_xlim(0, 500)
    ax.set_ylim(0, 100)

    ax.tick_params(which="both", direction="in", labelsize=14)
    ax.set_title(f"{window[0]}:00 - {window[-1]}:00 ({len(df)})", fontsize=20)

    plt.tight_layout()
    plt.savefig(f"{sdir}/{sname}", dpi=300)
    # plt.show()
