import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature


def draw_map(boundary=[111, 117.5, 19, 25.5]):
    """
    Create plt ax obtject with cartopy map on the given boundary box.
    """

    fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})
    ax.set_extent(boundary, ccrs.PlateCarree())

    # Add map features
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)

    # Draw gridlines
    gridlines = ax.gridlines(draw_labels=True, zorder=0,
                             linestyle="dashed", linewidth=0.5, 
                             color="dimgrey")
    gridlines.top_labels = False
    gridlines.right_labels = False

    return fig, ax


def get_hkia_coordinates():

    lat = 22.308046
    lon = 113.918480

    return lat, lon


def get_fir_corners():

    return [111, 117.5, 19, 25.5]
