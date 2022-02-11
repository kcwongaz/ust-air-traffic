import pandas as pd
import plotly.graph_objects as go
import os


date = "2019-05-01"
datadir = f"/mnt/Passport/Opensky/Full_Track_Data/{date}"

fig = go.Figure()

for subdir, dirs, files in os.walk(datadir):
    for file in files:
        fname = os.path.join(subdir, file)
        df = pd.read_csv(fname, header=0, index_col=0)

        lat = df["latitude"].to_numpy()
        lon = df["longitude"].to_numpy()

        fig.add_trace(go.Scattergeo(
            lat=lat, lon=lon, mode="lines",
            line={"width": 1, "color": "black"},
            opacity=0.7, name=file
            ))



# Center around Hong Kong
fig.update_geos(lataxis_range=[18, 25], lonaxis_range=[110, 120],
                resolution=50, projection_type = "equirectangular")

# Draw lat-lon grid
axis_attr = {"showgrid": True, 
             "dtick": 0.5, 
             "gridcolor": "rgb(102, 102, 102)",
             "gridwidth": 0.5}

fig.update_geos(lataxis=axis_attr)
fig.update_geos(lonaxis=axis_attr)


# Remove legend
fig.update_layout(showlegend=False)


# fig.show(renderer="iframe")
fig.show()
