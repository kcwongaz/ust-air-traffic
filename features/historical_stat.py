import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


fname = "/home/kc/Research/air_traffic/data/fr24_clean/stat_145-165_clustered.txt"
label = "145-165"

savedir = "/home/kc/Research/air_traffic/data/fr24_clean"

time_lags = [15, 30, 60]    # Compute history of these minutes before


# --------------------------------------------------------------------------- #
def historic_count(df, lag, t):

    df_window = df.loc[(df["t_f"] < t) & (df["t_f"] > (t - lag))]
    count = len(df_window)

    return count


def historic_mean(df, lag, t):

    df_window = df.loc[(df["t_f"] < t) & (df["t_f"] > (t - lag))]
    if len(df_window) == 0:
        return 0

    mean = np.mean(df_window["delta_t_sec"])

    return mean


# --------------------------------------------------------------------------- #
df = pd.read_csv(fname)
df = df[["t_i", "t_f", "delta_t_sec", "cluster"]]
df = df.sort_values(by=["t_i"])

history = {}

for t in time_lags:
    history[f"count_{t}_min"] = [historic_count(df, 60*t, t_i)
                                 for t_i in df["t_i"]]
    history[f"mean_{t}_min"] = [historic_mean(df, 60*t, t_i)
                                for t_i in df["t_i"]]

df_history = pd.DataFrame(data=history)

df = pd.concat([df, df_history], axis=1)
df.to_csv(f"{savedir}/stat_{label}_history.txt", index=False)
