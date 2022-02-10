import pandas as pd


def fetch_trajectories(client, bucket, start, end, var=None):

    df_time = locate_trajectory(client, bucket, start, end)
    df = pd.DataFrame()
    print(len(df_time))

    if len(df_time) == 0:
        return df

    if len(df_time) > 1000:
        print("Warning: More than 1000 trajectories are found." \
              "Probably not a good idea to use fetch_trajectories().")

    df = df.append([(fetch_trajectory(client, bucket, r[0], r[1], r[2], var=var)) 
            for r in zip(df_time["callsign"], df_time["start"], df_time["end"])])

    return df


def fetch_trajectory(client, bucket, callsign, start, end, var=None):

    if not var:
        var = ["latitude", "longitude", "altitude", "ground_speed", "heading_angle"]

    query_api = client.query_api()
    start = shift_timestamp(start, "60s", "-")
    end = shift_timestamp(end, "60s", "+")

    query = f'from(bucket: "{bucket}")' \
    f'|> range(start: {start}, stop: {end})' \
    f'|> filter(fn: (r) => r["callsign"] == "{callsign}")' \
    f'|> filter(fn: (r) => r["_measurement"] == "Trajectory") ' \
    
    df = query_api.query_data_frame(query)
    df = reshape_traj_df(df, var)

    return df


def locate_trajectory(client, bucket, start, end):

    query_api = client.query_api()
    search_start = shift_timestamp(start, "5d")
    
    query = f'from(bucket: "{bucket}")' \
    f'|> range(start: {search_start}, stop: {end})' \
    f'|> filter(fn: (r) => r["_measurement"] == "Flight") ' \
    f'|> filter(fn: (r) => r["_field"] == "end_time") ' \
    f'|> filter(fn: (r) => time(v: r["_value"]) > {start} and time(v: r["_value"]) < {end})'

    df = query_api.query_data_frame(query)
    df = df[["callsign", "_time", "_value"]]
    df = df.assign(_time=[t.strftime("%Y-%m-%dT%H:%M:%SZ") for t in df["_time"]])
    df = df.rename(columns={"_time": "start", "_value": "end"})

    return df


def shift_timestamp(t, delta, sign="-"):

    fmt = "%Y-%m-%dT%H:%M:%SZ"

    if sign == "+":
        t = (pd.to_datetime(t, format=fmt) +
         pd.Timedelta(delta)).strftime(fmt)
    else:
        t = (pd.to_datetime(t, format=fmt) - 
            pd.Timedelta(delta)).strftime(fmt)

    return t


def reshape_traj_df(df, var, with_callsign=True):
    
    to_be_merged = []
    for v in var:
        df1 = df.loc[df["_field"] == v]
        df1 = df1[["_time", "_value"]]
        df1 = df1.rename(columns={"_time": "time", "_value": v})
        df1 = df1.set_index("time")

        to_be_merged.append(df1)

    merged = pd.concat(to_be_merged, axis=1)

    if with_callsign:
        callsign = df["callsign"].iloc[0]
        merged = merged.assign(callsign=pd.Series(
            [callsign for _ in range(len(merged))]).values)

    return merged
