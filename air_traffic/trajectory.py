import geopy.distance as gd


def find_first_landed(df):

    # Get through the inital take-off stage
    n = 0
    while df["altitude"].iloc[n] == 0:
        n += 1
        # Also possible that the whole flight record is already landed
        if n == len(df):
            n = 0
            break

    # Locate the last part of the trajectory
    df = df.iloc[n:]
    df = df.loc[df["altitude"] == 0]

    # The first row that has altitude zero is when the flight landed
    return df.iloc[0]


def find_first_in_range(df, d_min, d_max):

    n = 0
    first = df.iloc[0]
    d = distance_hkia(first)

    while d > d_max:
        n += 1
        first = df.iloc[n]
        d = distance_hkia(first)

    # Return None if there are no point within the ring
    if d < d_min:
        return None
    else:
        return first


def distance(row1, row2):

    point1 = (row1["latitude"], row1["longitude"])
    point2 = (row2["latitude"], row2["longitude"])

    d = gd.distance(point1, point2).km
    return d


def distance_hkia(row):

    hkia = (22.308046, 113.918480)
    point = (row["latitude"], row["longitude"])

    d = gd.distance(point, hkia).km
    return d
