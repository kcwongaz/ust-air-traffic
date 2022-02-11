import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import os


date = "2019-05-10"
save_suffix = ""
filtering = False       # Filter points not within the box
scatter = False         # Draw only points without lines

datadir = f"/mnt/Passport/Opensky/Full_Track_Data/{date}"
savedir = "/home/kc/Research/air_traffic/figures/trajectories/"

# --------------------------------------------------------------------------- #
plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([110, 120, 18, 25], ccrs.PlateCarree())

# To compare with Harry's Fig.8
# ax.set_extent([111.5, 117.5, 20, 23], ccrs.PlateCarree())

# Draw map features
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)


# Get some colors
ncolor = 20
cmap = plt.cm.get_cmap("rainbow", ncolor)


counter = 1
for subdir, dirs, files in os.walk(datadir):
    for file in files:
        fname = os.path.join(subdir, file)
        df = pd.read_csv(fname, header=0, index_col=0)

        if filtering:
            df = df.loc[(df["latitude"] > 19) & (df["latitude"] < 23) &
                        (df["longitude"] > 111) & (df["longitude"] < 117.5)]

        lat = df["latitude"].to_numpy()
        lon = df["longitude"].to_numpy()
        c = cmap(counter % ncolor)

        if not scatter:
            ax.plot(lon, lat, transform=ccrs.Geodetic(),
                    linewidth=0.8, alpha=0.8, color=c)
        else:
            ax.plot(lon, lat, transform=ccrs.Geodetic(),
                    linewidth=0.8, alpha=0.8, color=c,
                    marker=".", ms=1, linestyle="none")

        counter += 1


# Marker for HKG
ax.plot([113.918480], [22.308046], "^", ms=2, color="black", fillstyle="none",
        linestyle="none")

# Draw box bounding [111, 117.5, 19, 25.5]
rect = plt.Rectangle((111, 19), 6.5, 6.5,
                     linewidth=1, edgecolor="black", facecolor="none", zorder=2)
ax.add_patch(rect)


# Draw gridlines
gridlines = ax.gridlines(draw_labels=True, zorder=0,
                         linestyle="dashed", linewidth=0.5, color="dimgrey")

gridlines.top_labels = False
gridlines.right_labels = False

plt.title(f"{date}")
plt.tight_layout()

plt.savefig(f"{savedir}/{date}{save_suffix}.png", dpi=300)
