import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt


filtering = True         # Filter points not within the box
scatter = False          # Draw only points without lines
draw_box = False         # Draw the boundary box
boundary = [111, 117.5, 19, 25.5]

fdir = "/home/kc/Research/air_traffic/data/fr24_china/2017-02/2017-02-01"
name = "EZD1264"
savedir = "/home/kc/Research/air_traffic/figures/trajectories/fr24"

save_fig = False
show_fig = True


# ---------------------------------------------------------------------------- #
plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)


ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent(boundary, ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)

df = pd.read_csv(f"{fdir}/{name}.csv", header=0)

if filtering:
    df = df.loc[(df["latitude"] > 19) & (df["latitude"] < 25.5) &
                (df["longitude"] > 111) & (df["longitude"] < 117.5)]

lat = df["latitude"].to_numpy()
lon = df["longitude"].to_numpy()

if not scatter:
    ax.plot(lon, lat, transform=ccrs.Geodetic(),
            marker=".", ms=1.5,
            linewidth=1, alpha=0.8, color="blue")
else:
    ax.plot(lon, lat, transform=ccrs.Geodetic(),
            linewidth=1, alpha=0.8, color="blue",
            marker=".", ms=1, linestyle="none")


# Marker for HKG
ax.plot([113.918480], [22.308046], "^", ms=2, color="black", fillstyle="none",
        linestyle="none")

# Draw box bounding [111, 117.5, 19, 25.5]
if draw_box:
    rect = plt.Rectangle((111, 19), 6.5, 6.5,
                         linewidth=1, edgecolor="black", facecolor="none", zorder=2)
    ax.add_patch(rect)

# Draw gridlines
gridlines = ax.gridlines(draw_labels=True, zorder=0,
                         linestyle="dashed", linewidth=0.5, color="dimgrey")

gridlines.top_labels = False
gridlines.right_labels = False

ax.set_title(name)
plt.tight_layout()


if save_fig:
    plt.savefig(f"{savedir}/{name}.png", dpi=300)

if show_fig:
    plt.show()
