from flight_radar24 import convert_fr24

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import json


# ---------------------------------------------------------------------------------------------- #
datadir = "/mnt/Passport/Lishuai_data/china/2017/201703"
token = "KmirXN2dSLKPATtHRkI150_utLePGFI1XUU8ZhQXvv2FghTdGlLUTed128Ug9O9bgpLg9rpxnSsTuRlAWpYWEA=="
org = "hkust"
bucket = "AirTraffic"


# Last time stopped at 
# /mnt/Passport/Lishuai_data/china/2017/201701/

excluded = []
# excluded = ["fr24_China_2017010" + str(i) for i in range(1, 10)]
# [excluded.append("fr24_China_201701" + str(i)) for i in range(10, 20)]

with InfluxDBClient(url="http://localhost:8086", token=token, org=org) as client:

    write_api = client.write_api(write_options=SYNCHRONOUS)
    badfile = []

    for subdir, dirs, files in os.walk(datadir):
        for file in files:
            fname = os.path.join(subdir, file)

            # Skip all non-json files
            if fname[-4:] != ".txt":
                continue

            if file[:19] in excluded:
                print(f"Excluded: {fname}")
                continue


            print(fname)
            with open(fname) as f:
                try:
                    js = json.load(f)
                except Exception as error:
                    print(error)
                    badfile.append(fname)
                    continue

                df = convert_fr24(js)
                write_api.write(bucket=bucket, record=df,
                                 data_frame_tag_columns=["callsign", "source"],
                                 data_frame_measurement_name="Trajectory")

print()
print("Completed !!")
print("Bad files:")
print(badfile)
