import pandas as pd

from air_traffic.io import read_trajectories_range
from air_traffic.trajectory import distance_hkia


# --------------------------------------------------------------------------- #
datadir = "../data/cleaned"

start = "2017-01-01"
end = "2017-01-31"

# --------------------------------------------------------------------------- #
dataset = read_trajectories_range(datadir, start, end, fname_only=True)

for files in dataset:
    for f in files:

        print(f)
        df = pd.read_csv(f, header=0)

        lat = df["latitude"].to_numpy()
        lon = df["longitude"].to_numpy()
        time = df["time"].to_numpy()

        d = df.apply(distance_hkia, axis=1)

        # Save the result
        df = df.assign(distance=d)
        df.to_csv(f, index=False)
