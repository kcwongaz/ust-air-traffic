import numpy as np
import pandas as pd


def check_arrivial(df, last_n=1, tol_lat=0.25, tol_lon=0.25):
    """
    Check if the trajectory lands around HK, return True if it does. 
    """

    # Coordinate of HKIA
    hklat = 22.308046
    hklon = 113.918480

    lat = df["latitude"].iloc[-last_n:].to_numpy()
    lon = df["longitude"].iloc[-last_n:].to_numpy()

    value = np.all(np.abs(lat - hklat) < tol_lat) and \
            np.all(np.abs(lon - hklon) < tol_lon)

    return value


def check_nondeparture(df, first_n=1, tol_lat=0.25, tol_lon=0.25):
    """
    Check if the trajectory departs from HK, return True if it does not.
    """

    # Coordinates of HKIA
    hklat = 22.308046
    hklon = 113.918480

    lat = df["latitude"].iloc[:first_n + 1].to_numpy()
    lon = df["longitude"].iloc[:first_n + 1].to_numpy()

    value = np.all(np.abs(lat - hklat) > tol_lat) or \
            np.all(np.abs(lon - hklon) > tol_lon)

    return value


def check_stayhk(df, n=10):
    """
    Check if the trajectory stay in HKTMA once it is inside.

    This is determined by check if the trajectory leave HKTMA again once it is
    insider for a certain number of time steps.

    Return True if it does stay.
    """

    lat = df["latitude"].to_numpy()
    lon = df["longitude"].to_numpy()

    in_zone_now = is_in_zone(lat[0], lon[0])
    counter = 0

    for i in range(0, len(lat) - 1):

        if in_zone_now:
            counter += 1
        else:
            counter = 0

        in_zone_next = is_in_zone(lat[i], lon[i])

        if counter >= n and not in_zone_next:
            return False
        else:
            in_zone_now = in_zone_next

    return True


def is_in_zone(lat, lon):
    """
    Check if the coordinate point (lat, lon) is within HKTMA
    """

    lat_min = 19
    lat_max = 25.5
    lon_min = 111
    lon_max = 117.5

    value = (lat > lat_min) and (lat < lat_max) and \
            (lon > lon_min) and (lon < lon_max)

    return value


def check_uniquetime(df):
    """
    Check if the trajectory has unique timestamp, return True if it does.
    """

    n = len(pd.unique(df["time"]))
    if n < len(df):
        return False
    else:
        return True


def check_noskiptime(df, n=1):
    """
    Check if the trajectory contains large jump in time, i.e. time gap with no data.
    Return True if it does not.
    """

    times = df["time"]
    delta = times[1:] - times[:-1]

    # If there are time skip bigger than n hours
    if np.max(delta) >= n*3600:
        return False
    else:
        return True


def check_notbanded(df, tol=20, n=10):
    """
    Detect banded trajectory by checking if the trajectory has an abnormal number
    of large jumps. This is not a perfect detection criteria, but I think is enough
    for the moment.

    Return True if it has fewer than n large jumps.
    """

    lat = df["latitude"].to_numpy()
    lon = df["longitude"].to_numpy()

    dlat = np.abs(lat[1:] - lat[:-1])
    dlon = np.abs(lon[1:] - lon[:-1])

    count = max(np.sum(dlat > tol), np.sum(dlon > tol))

    if count >= n:
        return False
    else:
        return True


def check_landed(df):
    """
    Detect if the flight landed (altitude down to zero) eventually.
    Return True if it did land.
    """

    if df["altitude"].iloc[-1] == 0:
        return True
    else:
        return False


def check_landedhk(df, tol_lat=0.25, tol_lon=0.25):
    """
    Check if the first point the flight has zero height is around HK.
    Return True if the first landed point is around HK.
    """

    # Get through the inital take-off stage
    n = 0
    while df["altitude"].iloc[n] == 0:
        n += 1
        # Also possible that the whole flight record is already landed,
        # then we don't cut the record
        if n == len(df):
            n = 0
            break
    df = df.iloc[n:]

    df_landed = df.loc[df["altitude"] == 0]

    # Flight did not land --> return immediately
    if len(df_landed) == 0:
        return

    # Extract first landed point
    lat = df_landed["latitude"].iloc[0]
    lon = df_landed["longitude"].iloc[0]

    # Coordinate of HKIA
    hklat = 22.308046
    hklon = 113.918480

    value = np.abs(lat - hklat) < tol_lat \
        and np.abs(lon - hklon) < tol_lon

    return value
