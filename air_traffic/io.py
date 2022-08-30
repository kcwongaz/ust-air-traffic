import pandas as pd
import os


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
            yield fetch_fnames(datadir, date)
        else:
            yield read_trajectories(datadir, dstr)


def read_trajectories(datadir, date):

    path = os.path.join(datadir, date[:7], date)

    for subdir, _, files in os.walk(path):
        for file in files:
            fname = os.path.join(subdir, file)
            yield pd.read_csv(fname, header=0, index_col=0)


def fetch_fnames(datadir, date):

    path = os.path.join(datadir, date[:7], date)

    for subdir, _, files in os.walk(path):
        for file in files:
            fname = os.path.join(subdir, file)
            yield fname
