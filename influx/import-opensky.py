from opensky import convert_opensky, construct_trajectory, construct_datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import pandas as pd


# ---------------------------------------------------------------------------------------------- #
datadir = "/mnt/Passport/Opensky/Full_Track_Data/"
token = "KmirXN2dSLKPATtHRkI150_utLePGFI1XUU8ZhQXvv2FghTdGlLUTed128Ug9O9bgpLg9rpxnSsTuRlAWpYWEA=="
org = "hkust"
bucket = "AirTraffic"


with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:

    write_api = client.write_api(write_options=SYNCHRONOUS)

    for subdir, dirs, files in os.walk(datadir):
        for file in files:
            fname = os.path.join(subdir, file)
            callsign = file[:-4]
            print(fname)

            # Header row = 0 
            df = pd.read_csv(fname, header=0)
            write_api.write(bucket, org, construct_trajectory(df, callsign))

            # df = convert_opensky(df, callsign)
            # write_api.write(bucket=bucket, record=df,
            #                 data_frame_tag_columns=["callsign", "source"],
            #                 data_frame_measurement_name="Trajectory")
