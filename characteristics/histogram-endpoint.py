import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


fname = "/home/kc/Research/air_traffic/data/opensky_all_endpoints.csv"
sname = "endpoints_all_runway.png"
savedir = "/home/kc/Research/air_traffic/figures/2022-01-11/"

mode = "real"     # "real" for real physcial distance
                  # "pseduo" for pseduo-Euclidean distance

# ---------------------------------------------------------------------------- #
df = pd.read_csv(fname)

if mode == "pseduo":
    data = df["delta_pseduo"].to_numpy()
else:
    data = df["delta_hkia_km"].to_numpy()

    index = np.argwhere(data < 100)
    data = data[index]

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)


hist, bin_edges = np.histogram(data, bins=10, density=False)

fig, ax = plt.subplots()
ax.hist(data, bins=50)


plt.tight_layout()
# plt.savefig(f"{savedir}/{sname}", dpi=300)
plt.show()
