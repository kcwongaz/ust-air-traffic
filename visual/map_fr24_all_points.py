import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import os


save_suffix = ""

regions = ["china", "europe", "seasia", "usa"]
colors = {"china": "red", "europe": "blue",
          "seasia": "green", "usa": "darkviolet"}
year = "2020"

datadir = f"/home/kc/Research/air_traffic/data"
savedir = "/home/kc/Research/air_traffic/figures/2022-02-15"

# ---------------------------------------------------------------------------- #
plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)


for r in regions:
    for root, dirs, files in os.walk(f"{datadir}/fr24_{r}"):

        if root[-10:-6] != year:
            continue

        for file in files:
            if not file.endswith(".csv"):
                continue

            fname = os.path.join(root, file)
            df = pd.read_csv(fname, header=0)
            print(fname)

            if len(df) == 0:
                print(f"No data in {fname}")
                continue

            lat = df["latitude"]
            lon = df["longitude"]

            ax.plot(lon, lat, marker="o", color=colors[r], alpha=0.3, ms=0.5,
                    linestyle="none")


# Draw gridlines
gridlines = ax.gridlines(draw_labels=True, zorder=0,
                         linestyle="dashed", linewidth=0.5, color="dimgrey")

gridlines.top_labels = False
gridlines.right_labels = False

plt.tight_layout()
plt.savefig(f"{savedir}/fr24_point_map.png", dpi=300)
