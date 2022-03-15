import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans
import cartopy.crs as ccrs
import cartopy.feature as cfeature


fname = "/home/kc/Research/air_traffic/data/fr24_clean/stat_145-165.txt"
label = "145-165"

figdir = "/home/kc/Research/air_traffic/figures/2022-03-15/"
savedir = "/home/kc/Research/air_traffic/data/fr24_clean"

n_clusters = 5
colors = ["blue", "red", "green", "purple", "orange"]

savefig = False
showfig = True
savecluster = True

plt.rcParams.update({
    "font.family": "serif",
    "font.sans-serif": ["Helvetica"]}
)

# --------------------------------------------------------------------------- #
# Clustering calculation
df = pd.read_csv(fname)
lat, lon = df["lat_i"].to_numpy(), df["lon_i"].to_numpy()

coords = np.column_stack((lon, lat))

kmeans = KMeans(init="random", n_clusters=n_clusters,
                n_init=50, max_iter=300)

kmeans.fit(coords)
c_labels = kmeans.labels_


# --------------------------------------------------------------------------- #
# Draw the resulting clusters

# Draw the background map
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([111, 117.5, 19, 25.5], ccrs.PlateCarree())
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)

# Build the color array
c_colors = [colors[i] for i in c_labels]

# Draw
ax.scatter(lon, lat, s=5, c=c_colors, marker="o",
           alpha=0.3, edgecolors="none")

gridlines = ax.gridlines(draw_labels=True, zorder=0,
                         linestyle="dashed", linewidth=0.5, color="dimgrey")
gridlines.top_labels = False
gridlines.right_labels = False

plt.tight_layout()
if showfig:
    plt.show()

if savecluster:
    df = df.assign(cluster=c_labels)
    df.to_csv(f"{savedir}/stat_{label}_clustered.txt", index=False)
