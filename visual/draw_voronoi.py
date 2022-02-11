import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from voronoi_finite_polygons_2d import voronoi_finite_polygons_2d


mode = "rect"

fname = "/home/kc/Research/air_traffic/data/significant_points.csv"
sname = f"/home/kc/Research/air_traffic/figures/voronoi_{mode}.png"


if mode == "full":
    boundary = [110, 118, 18, 26]
elif mode == "rect":
    boundary = [111, 117.5, 19, 25.5]
elif mode == "close":
    boundary = [113, 115, 21.5, 22.5]
elif mode == "tiny":
    boundary = [113.72, 113.74, 22.19, 22.21]
else:
    boundary = [110, 118, 18, 23]


plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)


# Read data 
df = pd.read_csv(fname, header=0)
lat = df["Lat"].to_numpy()
lon = df["Lon"].to_numpy()

# Compute Voronoi
vor = Voronoi(list(zip(lon, lat)))
regions, vertices = voronoi_finite_polygons_2d(vor)


ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent(boundary, ccrs.PlateCarree())
# ax.set_extent([100, 125, 15, 30], ccrs.PlateCarree())

# Draw map features
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)


for region in regions:
    polygon = vertices[region]
    ax.fill(*zip(*polygon), color="none", edgecolor="orangered", alpha=0.5)
ax.scatter(lon, lat, s=2, color="black")

# Marker for HKG
ax.plot([113.918480], [22.308046], "^", ms=2, color="blue", fillstyle="none",
        linestyle="none")

# Draw box bounding [111, 117.5, 19, 25.5]
rect = plt.Rectangle((111, 19), 6.5, 6.5,
                     linewidth=1.5, edgecolor="black", facecolor="none", zorder=2)
ax.add_patch(rect)


# Draw gridlines
if mode != "tiny":
    gridlines = ax.gridlines(draw_labels=True, zorder=0,
                            linestyle="dashed", linewidth=0.5, color="dimgrey")
    gridlines.top_labels = False
    gridlines.right_labels = False

plt.tight_layout()
# plt.show()
plt.savefig(sname, dpi=300)
