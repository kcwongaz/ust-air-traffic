import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fname = "/home/kc/Research/air_traffic/data/opensky_clean/time_distance.txt"
sname = "entrypoint_distance.png"
savedir = "/home/kc/Research/air_traffic/figures/2022-01-25/"

# "real" for real physcial distance
# "pseduo" for pseduo-Euclidean distance
mode = "real"

# --------------------------------------------------------------------------- #
df = pd.read_csv(fname)

data = df["delta_r_km"].to_numpy()
index = np.argwhere(data < 50)
data = data[index]

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

fig, ax = plt.subplots()
ax.hist(data, bins=50, edgecolor="black", linewidth=1.0,
        color="#7aa2f7")

ax.set_xticks(np.arange(0, 51, 5))
ax.set_xlabel("Distance from Final Point (km)", fontsize=18)
ax.set_ylabel("Entry Flight Count", fontsize=18)

plt.tight_layout()
plt.savefig(f"{savedir}/{sname}", dpi=300)
plt.show()
