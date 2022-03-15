import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt


fname = "/home/kc/Research/air_traffic/data/fr24_clean/stat_145-165_clustered.txt"
savedir = "/home/kc/Research/air_traffic/figures/2022-03-15/"

colors = ["blue", "red", "green", "purple", "orange"]
c_names = ["Southeast", "North", "Southwest", "East", "Northwest"]

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

savefig = True
showfig = True

# --------------------------------------------------------------------------- #
df = pd.read_csv(fname)
lat, lon = df["lat_i"].to_numpy(), df["lon_i"].to_numpy()

c_labels = df["cluster"].to_numpy()
c_colors = [colors[i] for i in c_labels]

# Draw the background map
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([111, 117.5, 19, 25.5], ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)


ax.scatter(lon, lat, s=5, c=c_colors, marker="o",
           alpha=0.3, edgecolors="none")

# Cluster labels
for i, name in enumerate(c_names):
    ax.plot([], [], marker="o", linestyle="none", color=colors[i],
            label=f"{i} {name}")

ax.legend()

# Marker for HKG
ax.plot([113.918480], [22.308046], "^", ms=2, color="black", fillstyle="none",
        linestyle="none")

# Draw gridlines
gridlines = ax.gridlines(draw_labels=True, zorder=0,
                         linestyle="dashed", linewidth=0.5, color="dimgrey")
gridlines.top_labels = False
gridlines.right_labels = False

plt.tight_layout()

if savefig:
    plt.savefig(f"{savedir}/entry_clusters.png", dpi=300)

if showfig:
    plt.show()
