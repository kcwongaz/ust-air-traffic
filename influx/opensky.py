from utilities import check_callsign

from influxdb_client import Point, WritePrecision
from datetime import datetime, timezone
import pandas as pd
import numpy as np


def convert_opensky(df, callsign):

    columns = ["latitude", "longitude", "altitude", "groundspeed", "track"]
    timestamps = [pd.to_datetime(construct_datetime(x)) for x in df["timestamp"]]
    callsign = check_callsign(callsign)

    df1 = df[columns]

    # Properly add dataframe column
    df1 = df1.assign(time=pd.Series(timestamps).values)
    df1 = df1.assign(source=pd.Series(["opensky" for _ in range(len(df1))]).values)
    df1 = df1.assign(callsign=pd.Series([callsign for _ in range(len(df1))]).values)
    df1 = df1.rename(columns={"groundspeed": "ground_speed", "track": "heading_angle"})

    df1 = df1.set_index("time")

    # Pandas NaN gives a lot of problems
    # Ad-hoc solution: Add an extra first column containing np.nan,
    # which somehow makes np.nan writeable afterward
    df1 = df1.assign(a=pd.Series([np.nan for _ in range(len(df1))]).values)

    return df1


def construct_trajectory(df, callsign):
    """
    Construct InfluxDB DataPoint for a trajectory from Pandas dataframe
    """

    fmt = "%Y-%m-%dT%H:%M:%SZ"

    start_time = construct_datetime(df["timestamp"].iloc[0])
    end_time = construct_datetime(df["timestamp"].iloc[-1])
    callsign = check_callsign(callsign)

    
    data = {"measurement": "Flight",
            "tags": {"callsign": callsign, "source": "opensky"},
            "fields": {"start_time": start_time.strftime(fmt), 
                       "end_time": end_time.strftime(fmt)},
            "time": start_time
            }

    point = Point.from_dict(data, WritePrecision.NS)
    return point


def construct_datetime(datestr):
    """
    Construct datetime object from the timestamp column
    The time string format is
        2019-04-30 08:20:20+00:00
        %Y-%m-%d %H:%M:%S

    """

    # Remove the useless +00:00 at the end
    datestr = datestr[:-6]
    
    f = "%Y-%m-%d %H:%M:%S"
    dt = datetime.strptime(datestr, f)
    dt = dt.replace(tzinfo=timezone.utc)

    return dt
