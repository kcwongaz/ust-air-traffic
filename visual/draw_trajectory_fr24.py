import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import os


dt = pd.Timedelta(1, "D")
start_date = pd.to_datetime("2017-05-31", format=r"%Y-%m-%d")
end_date = pd.to_datetime("2017-12-31", format=r"%Y-%m-%d")

save_suffix = ""
filtering = True       # Filter points not within the box
scatter = False         # Draw only points without lines
draw_box = False         # Draw the boundary box
boundary = [111, 117.5, 19, 25.5]

datadir = f"/home/kc/Research/air_traffic/data/fr24_china"
savedir = "/home/kc/Research/air_traffic/figures/trajectories/fr24"

# ---------------------------------------------------------------------------- #
plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

# Get some colors
ncolor = 25
cmap = plt.cm.get_cmap("rainbow", ncolor)

date = start_date
while date <= end_date:
    dstr = date.strftime(r"%Y-%m-%d")
    mstr = date.strftime(r"%Y-%m")

    # Skip over months with no data
    if not os.path.exists(f"{datadir}/{mstr}"):
        date += dt
        continue

    print(datadir + "/" + dstr)

    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent(boundary, ccrs.PlateCarree())

    # Draw map features
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

    # To keep track of number of flights per day
    counter = 1

    for subdir, dirs, files in os.walk(f"{datadir}/{mstr}/{dstr}"):
        for file in files:
            fname = os.path.join(subdir, file)
            df = pd.read_csv(fname, header=0)

            if filtering:
                df = df.loc[(df["latitude"] > 19) & (df["latitude"] < 25.5) &
                            (df["longitude"] > 111) & (df["longitude"] < 117.5)]

            lat = df["latitude"].to_numpy()
            lon = df["longitude"].to_numpy()
            c = cmap(counter % ncolor)

            if not scatter:
                ax.plot(lon, lat, transform=ccrs.Geodetic(),
                        marker=".", ms=1.5,
                        linewidth=0.5, alpha=0.8, color=c)
            else:
                ax.plot(lon, lat, transform=ccrs.Geodetic(),
                        linewidth=0.8, alpha=0.8, color=c,
                        marker=".", ms=1, linestyle="none")

            counter += 1

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

    ax.set_title(f"{dstr} ({counter})")
    plt.tight_layout()

    if not os.path.exists(f"{savedir}/{mstr}"):
        os.makedirs(f"{savedir}/{mstr}", exist_ok=True)

    plt.savefig(f"{savedir}/{mstr}/{dstr}{save_suffix}.png", dpi=300)

    date += dt
    plt.cla()
    plt.clf()
