from Opensky import convert_opensky, construct_trajectory, construct_datetime

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd
import os


# ---------------------------------------------------------------------------------------------- #
datadir = "/mnt/Passport/Opensky/Full_Track_Data/2019-05-01"
token = "KmirXN2dSLKPATtHRkI150_utLePGFI1XUU8ZhQXvv2FghTdGlLUTed128Ug9O9bgpLg9rpxnSsTuRlAWpYWEA=="
org = "hkust"
bucket = "test_import"

date = "2019-05-01"

with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:

    write_api = client.write_api(write_options=SYNCHRONOUS)

    # for subdir, dirs, files in os.walk(datadir):
    #     for file in files:
    #         fname = os.path.join(subdir, file)
    #         callsign = file[:-4]
    #         print(fname)

    #         # Header row = 0 
    #         df = pd.read_csv(fname, header=0)
    #         write_api.write(bucket, org, construct_trajectory(df, callsign))

            
    query_api = client.query_api()

    start = f"{date}T00:00:00Z"
    end = f"{date}T23:59:59Z"

    # Get all flight landed on the target date 
    query = f'from(bucket: "{bucket}")' \
        f'|> range(start: 2019-01-01T00:00:00Z, stop: {end})' \
        f'|> filter(fn: (r) => r["_measurement"] == "Flight") ' \
        f'|> filter(fn: (r) => r["_field"] == "end_time") ' \
        f'|> filter(fn: (r) => time(v: r["_value"]) > {start} and time(v: r["_value"]) < {end})'
        

    df = query_api.query_data_frame(query)
    print(df.dtypes)
