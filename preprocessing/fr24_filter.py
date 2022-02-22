import numpy as np
import pandas as pd
import os

from fr24_checkers import *


# --------------------------------------------------------------------------- #

# Will apply filter to all trajectories within this date range
start_date = "2016-12-31"
end_date = "2021-04-28"


# (!) Change the following to appropriate directory names
# Location of raw data
dataroot = "/home/kc/Research/air_traffic/data/fr24_china/"

# Location for output
copyroot = "/home/kc/Research/air_traffic/data/fr24_clean/"

# mode should be in of ["copy", "list", ""]
# "copy" will create a filtered copy of the data in copyroot
# "list" will just write a list listing the good trajectories without making copies
# "" will only write down the filter summary without copying or listing the good trajectories
#
# Choose one that best fit how you want to use the data
# Also, not copying the trajectories will obviously make thing much faster
mode = "copy"


# Filter criteria to be used
# checker_fun takes a list of checker function from opensky_checkers
# checker_str is just a list of string labeling the checker functions
checker_fun = [check_nondeparture, check_stayhk,
               check_uniquetime, check_landed, check_landedhk]

checker_str = ["Departures", "Not stayed HKTMA",
               "Duplicated time points", "Not landed", "Not landed at HK"]


# --------------------------------------------------------------------------- #
# *** Actual computation starts here

date_fmt = "%Y-%m-%d"

date = pd.to_datetime(start_date, format=date_fmt)
end = pd.to_datetime(end_date, format=date_fmt)
dt = pd.Timedelta(1, "D")

checker_n = len(checker_fun)

# Overall filter statistics
total_all, good_all = 0, 0
bad_all = {s: 0 for s in checker_str}

summary_writer = open(f"{copyroot}/filter_summary.txt", "w")
if mode == "list":
    list_writer = open(f"{copyroot}/list_{start_date}_{end_date}.txt", "w")


while date <= end:
    dstr = date.strftime(date_fmt)
    mstr = date.strftime("%Y-%m")
    datadir = dataroot + mstr + "/" + dstr
    copydir = copyroot + mstr + "/" + dstr

    # Create destination directory if not exist
    if not os.path.exists(copydir) and mode == "copy":
        os.makedirs(copydir)

    # Filter statistics for this day
    total, good = 0, 0
    badfiles = {s: [] for s in checker_str}

    print(f"Now working on {dstr} ...")

    # Loop through all trajectories in this day
    for subdir, dirs, files in os.walk(datadir):
        for file in files:
            fname = os.path.join(subdir, file)
            df = pd.read_csv(fname, header=0)

            # FR24 sometime has duplicated rows
            # I would forgive them if they have identical space-time coordinate
            df = df.drop_duplicates(subset=["time", "latitude", "longitude"])

            total += 1
            total_all += 1
            keep = True

            # Pass the trajectory to the checker functions
            for i in range(checker_n):
                if not checker_fun[i](df):
                    badfiles[checker_str[i]].append(file)
                    bad_all[checker_str[i]] += 1

                    keep = False

            # All passed: keep the trajectory
            if keep:
                good += 1
                good_all += 1

                if mode == "copy":
                    df.to_csv(f"{copydir}/{file}", index=False)
                elif mode == "list":
                    list_writer.write(f"{fname}\n")

        # Filter summary for this date
        summary_writer.write(f"*** {dstr} --- {good}/{total} passed\n")
        for item in badfiles:
            for file in badfiles[item]:
                summary_writer.write(f"\t {item}: {file}\n")
            summary_writer.write("\n")
        summary_writer.write("# ----------------------------------------- #\n")

    # Forward to the next day
    date += dt


# Finish writing the filer list
summary_writer.close()
if mode == "list":
    list_writer.close()


# Now write the overall summary
summary_writer = open(f"{copyroot}/filter_statistics.txt", "w")

summary_writer.write("*** Overall Summary ***\n")
summary_writer.write("\n")
summary_writer.write(f"Passed: {good_all}/{total_all}  ({round(good_all / total_all * 100, 2)}%)\n")
summary_writer.write("\n")

for item in bad_all:
    b = bad_all[item]
    summary_writer.write(f"{item}: {b}/{total_all} ({round(b/total_all * 100, 2)}%) \n")

summary_writer.close()

print("Done !!")
