import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import os


dt = pd.Timedelta(1, "D")
start_date = pd.to_datetime("2017-01-01", format=r"%Y-%m-%d")
end_date = pd.to_datetime("2017-03-31", format=r"%Y-%m-%d")

save_suffix = "_20170103"
filtering = True       # Filter points not within the box
scatter = False         # Draw only points without lines
draw_box = False         # Draw the boundary box
boundary = [111, 117.5, 19, 25.5]

datadir = f"/home/kc/Research/air_traffic/data/fr24_china"
savedir = "/home/kc/Research/air_traffic/figures/2022-03-15"

# ---------------------------------------------------------------------------- #
plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent(boundary, ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)


date = start_date
while date <= end_date:
    dstr = date.strftime(r"%Y-%m-%d")
    mstr = date.strftime(r"%Y-%m")

    # Skip over months with no data
    if not os.path.exists(f"{datadir}/{mstr}"):
        date += dt
        continue

    print(datadir + "/" + dstr)

    for subdir, dirs, files in os.walk(f"{datadir}/{mstr}/{dstr}"):
        for file in files:
            fname = os.path.join(subdir, file)
            df = pd.read_csv(fname, header=0)

            df = df.loc[(df["latitude"] > 19) & (df["latitude"] < 25.5) &
                        (df["longitude"] > 111) & (df["longitude"] < 117.5)]

            lat = df["latitude"].to_numpy()
            lon = df["longitude"].to_numpy()

            ax.plot(lon, lat, transform=ccrs.Geodetic(),
                    linewidth=0.1, alpha=0.1, color="blue")
    date += dt

# Draw gridlines
gridlines = ax.gridlines(draw_labels=True, zorder=0,
                         linestyle="dashed", linewidth=0.5, color="dimgrey")

gridlines.top_labels = False
gridlines.right_labels = False
plt.tight_layout()
plt.savefig(f"{savedir}/trajectory_density{save_suffix}.png", dpi=300)
plt.show()
