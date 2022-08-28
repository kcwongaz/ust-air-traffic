import os
import json
import pickle
import shutil
import zipfile

from FR24Writer import FR24Writer


# --------------------------------------------------------------------------- #
# User inputs

# Locations to read data from
# All the .bz2 files and top level .zip files are expected to be decompressed.
# (e.g. 01.tar.bz2, 02.zip, etc.)
# So that the directories have all the yyyymmdd.zip files.
# Make sure all yyyymmdd.zip are there, or you will miss some time points.
dataroot = "/mnt/Passport/Lishuai_data/USA"

# Locations to store data to
saveroot = "/home/kc/Research/air_traffic/data/fr24_usa"

# Location for a pickled FR24Writer object to be restored.
# This is for continuing a partial flight extraction.
# Set this to an empty string if there are nothing to be restored.
# Each sucessful run will generate a FR24Writer.pickle for use
restore_loc = ""


# (!!!) Some suggestions
# Do the extraction for one geographic area per run.
# i.e. set dataroot ".../Lishuai_data/china/" instead of ".../Lishuai_data/"
# When start for a new area, always set restore_loc = ""
# These should prevent some potential problems that I haven't fully tested.
#
# You can also do it year-by-year or month-by-month like
#   dataroot = "/mnt/Passport/Lishuai_data/china/2017/"
# But when you continue to the next year, remember to set restore_loc
# so that you pick up the flights that have not landed in the previous year.

# --------------------------------------------------------------------------- #
# *** Main program starts here

# Initialize flight writer
if restore_loc == "":
    flights = FR24Writer(saveroot)
else:
    with open(restore_loc, "rb") as f:
        flights = pickle.load(f)
        flights.set_saveroot(saveroot)
cutoff_time = 0

# Create the working directories if not already there
if not os.path.exists(saveroot):
    os.makedirs(saveroot, exist_ok=True)

tempdir = f"{saveroot}/temp"
if not os.path.exists(tempdir):
    os.makedirs(tempdir, exist_ok=True)

# Start the log
log_writer = open(f"{saveroot}/fr24_extract.log", "a")
log_writer.write("# --------------------------------------------------- #\r\n")
log_writer.write(f"Extract from: {dataroot} \r\n \r\n")


# *** Main loop
for root, dirs, files in os.walk(dataroot):
    # os.walk() returns a generator that compute the next element in place.
    # This next element is read off from the returned dirs object.
    # So sorting dirs in place make os.walk() traverse in sorted order
    dirs.sort()
    files.sort()

    # 1. Copy the yyyymmdd.zip files to local working directory
    for file in files:
        if file.endswith(".zip") and len(file) >= 12:
            fname = os.path.join(root, file)
            shutil.copy(fname, tempdir)

            log_writer.write(f"Found: {fname} \r\n")
            print(f"Found: {fname}")

    # 2. Unzip all the copied .zip files
    for file in os.listdir(tempdir):
        if not file.endswith(".zip"):
            continue

        # Have to unzip file one-by-one, because some files may contain error
        zf = zipfile.ZipFile(os.path.join(tempdir, file), "r")
        for zf_child in zf.namelist():
            try:
                zf.extract(zf_child, tempdir)
            except zipfile.BadZipFile:
                log_writer.write(f"Error unzipping {zf}/{zf_child} \r\n")
        zf.close()

    # 3. Now loop through the unzipped .json file to extract flights
    for troot, tdirs, tfiles in os.walk(tempdir):
        tdirs.sort()
        tfiles.sort()

        for tfile in tfiles:
            if not tfile.endswith(".json") and not tfile.endswith(".txt"):
                continue
            fname = os.path.join(troot, tfile)

            if os.stat(fname).st_size == 0:
                log_writer.write(f"Empty JSON file: {fname} \r\n")
                continue

            with open(fname, "r") as f:
                try:
                    json_data = json.load(f)
                    timestamp_fetched = False
                    print(fname)
                except json.JSONDecodeError:
                    log_writer.write(f"Error encountered on: {fname} \r\n")
                    continue

                for key, item in json_data.items():
                    # Each json file contains some useless meta-data,
                    # actual flight data take shape of a list
                    if not isinstance(item, list):
                        continue

                    # The data row also need to have the correct length
                    # Expecting length 18, but some can have 19 for some reason
                    if len(item) < 18:
                        log_writer.write(f"Error encountered on: {fname} \r\n")
                        continue

                    # Pick only flights that are coming to HK
                    if item[12] != "HKG":
                        continue

                    # Read the timestamp for the current file only once
                    # Do one push every 24 hours = 86400 seconds
                    if not timestamp_fetched and (item[10] - cutoff_time >= 86400):
                        cutoff_time = item[10]
                        flights.push(cutoff_time)

                    flights.write(key, item)

    # Done with this round, empty the temp directory
    shutil.rmtree(tempdir)
    os.makedirs(tempdir, exist_ok=True)


# One last push before finishing.
# This is to store all the data we got regardless of the push criteria.
# But this time we push without cleaning them in FR24Writer.
#
# So in case there are more data points in the next run,
# we can still add them in the restored FR24Writer, and we will overwrite
# the .csv file with the complete data from both this run and the next run.
# This ensure we don't throw away any flights at the time window boundary.
flights.push_safely()

# Store the FR24Writer object with whatever leftover flights,
# so that we can continue with them later.
with open(f"{saveroot}/FR24Writer.pickle", "wb") as f:
    pickle.dump(flights, f)

log_writer.write("\r\n Successfully finished. \r\n")
log_writer.write("# --------------------------------------------------- #\r\n")
log_writer.close()

print("Finished !!")
