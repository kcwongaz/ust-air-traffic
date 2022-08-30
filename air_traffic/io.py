import pandas as pd
import numpy as np
import csv
import os

import air_traffic.loop as lp


def read_trajectories_range(datadir, start, end, verbose=False,
                            fname_only=False):

    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)
    dt = pd.Timedelta(1, "D")

    date = start_date
    while date <= end_date:

        if verbose:
            print(f"Now fetching {date}...")

        dstr = date.strftime("%Y-%m-%d")
        mstr = date.strftime(r"%Y-%m")

        date += dt

        # Skip over months with no data
        if not os.path.exists(f"{datadir}/{mstr}"):
            continue

        if fname_only:
            yield fetch_fnames(datadir, dstr)
        else:
            yield read_trajectories(datadir, dstr)


def read_trajectories(datadir, date):

    path = os.path.join(datadir, date[:7], date)

    for subdir, _, files in os.walk(path):
        for file in files:
            fname = os.path.join(subdir, file)
            yield pd.read_csv(fname, header=0)


def fetch_fnames(datadir, date):

    path = os.path.join(datadir, date[:7], date)

    for subdir, _, files in os.walk(path):
        for file in files:
            fname = os.path.join(subdir, file)
            yield fname


def loop_write(dataset, savename):

    with open(savename, mode="w") as f:
        writer = csv.writer(f, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)

        for dfs in dataset:
            for df in dfs:

                df = df.loc[df["distance"] <= 200]
                dist = df["distance"].to_numpy()

                min_loc = lp.locate_loops(dist)

                _, min_time = lp.find_minima_spacetime(dist[:,1], dist[:,0],
                                                       min_loc)

                # Skip if no loop is found
                if len(min_time) == 0:
                    continue

                _, exit_time = lp.find_exitpoint(dist[:,1], dist[:,0], min_loc)

                # Determine entry direction thus the holding area
                if df["longitude"].iloc[0] < 114:
                    area = "CANTO"  # loops in West
                elif df["latitude"].iloc[0] > 21:
                    area = "ABBEY"  # loops in Northeast
                else:
                    area = "BETTY"  # loops in Southeast

                row = [area]
                row.extend(min_time)
                row.append(exit_time)
                writer.writerow(row)


def loop_read(fname, keep_area=True):

    data = []
    with open(fname) as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:

            # Throw away the loop area label
            if not keep_area:
                row = row[1:]
            data.append(row)

    return data


def loop_read_area(fname):

    data_all = loop_read(fname)
    data = {"ABBEY": [], "BETTY": [], "CANTO": []}

    for entry in data_all:
        area = entry[0]

        data[area].append(entry[1:])

    return data
