import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


fname = "/home/kc/Research/air_traffic/data/opensky_clean/time_distance.txt"
fdir = "/home/kc/Research/air_traffic/data/opensky_clean/"

sdir = "/home/kc/Research/air_traffic/figures/2022-01-18"
sname = "outliner_trajectory_close.png"

# --------------------------------------------------------------------------- #
df = pd.read_csv(fname, header=0)
df["delta_t_sec"] = df["delta_t_sec"] / 60
df = df.loc[(df["delta_t_sec"] < 800) & (df["delta_t_sec"] >= 80)]
date = df["date"].to_numpy()
callsign = df["callsign"].to_numpy()


plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

# Draw map
ax = plt.axes(projection=ccrs.PlateCarree())
# ax.set_extent([111, 117.5, 19, 25.5], ccrs.PlateCarree())
ax.set_extent([113, 116, 20.5, 23.5], ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)

# Get some colors
ncolor = 20
cmap = plt.cm.get_cmap("rainbow", ncolor)
stat = {}

counter = 1
for n in range(len(date)):
    df_traj = pd.read_csv(f"{fdir}/{date[n]}/{callsign[n]}.csv", header=0)

    lat = df_traj["latitude"].to_numpy()
    lon = df_traj["longitude"].to_numpy()
    c = cmap(counter % ncolor)

    ax.plot(lon, lat, transform=ccrs.Geodetic(),
            linewidth=0.8, alpha=0.8, color=c)

    if date[n] not in stat:
        stat[date[n]] = 1
    else:
        stat[date[n]] += 1

    counter += 1

[print(d, stat[d]) for d in stat]
print()
print(counter)

# Draw gridlines
gridlines = ax.gridlines(draw_labels=True, zorder=0,
                         linestyle="dashed", linewidth=0.5, color="dimgrey")

gridlines.top_labels = False
gridlines.right_labels = False

plt.tight_layout()
# plt.savefig(f"{sdir}/{sname}", dpi=300)
# plt.show()
