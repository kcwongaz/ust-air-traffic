import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt


fname = "/home/kc/Research/air_traffic/data/fr24_stat/time_distance_china.txt"
savedir = "/home/kc/Research/air_traffic/figures/2022-02-15/"

mode = "full"   # one of ["full", "close", "runway"]
sname = f"entrypoints_{mode}.png"
# ---------------------------------------------------------------------------- #
df = pd.read_csv(fname)
lat, lon = df["lat_i"].to_numpy(), df["lon_i"].to_numpy()


plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

ax = plt.axes(projection=ccrs.PlateCarree())

if mode == "full":
    ax.set_extent([111, 117.5, 19, 25.5], ccrs.PlateCarree())
elif mode == "close":
    ax.set_extent([113, 115, 21, 23], ccrs.PlateCarree())
elif mode == "runway":
    ax.set_extent([113.918480-0.25, 113.918480+0.25, 
                   22.308046-0.25, 22.308046+0.25], ccrs.PlateCarree())
else: 
    ax.set_extent([111, 117.5, 19, 25.5], ccrs.PlateCarree())

ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)


ax.scatter(lon, lat, s=5, c="blue", marker="o",
           alpha=0.3, edgecolors="none")


hklat = 22.308046
hklon = 113.918480

# Marker for HKG
ax.plot([hklon], [hklat], "^", ms=2, color="black", fillstyle="none",
        linestyle="none")

# # Box around the filter region
rect = plt.Rectangle((hklon - 0.25, hklat - 0.25), 0.5, 0.5,
                     linewidth=1, edgecolor="black", facecolor="none", zorder=2)
ax.add_patch(rect)


# Draw gridlines
gridlines = ax.gridlines(draw_labels=True, zorder=0,
                         linestyle="dashed", linewidth=0.5, color="dimgrey")
gridlines.top_labels = False
gridlines.right_labels = False

plt.tight_layout()
plt.savefig(f"{savedir}/{sname}", dpi=300)
