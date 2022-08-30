import os
import json
import pickle

from air_traffic.FR24Writer import FR24Writer


# --------------------------------------------------------------------------- #
# User inputs

# Locations to read data from
# All files are expected to be fully decompressed,
# so that in the directory you should see the bare .json / .txt files
dataroot = "../raw"

# Locations to store data to
saveroot = "../data/extracted"

# Location for a pickled FR24Writer object to be restored.
# This is for continuing a partial flight extraction.
# Set this to an empty string if there are nothing to be restored.
# Each sucessful run will generate a FR24Writer.pickle for use
restore_loc = ""

# --------------------------------------------------------------------------- #
# *** Main program starts here
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

    for file in files:
        # Skip files that are not json, e.g. any leftover zip files
        if not file.endswith(".json") and not file.endswith(".txt"):
            continue
        fname = os.path.join(root, file)
        print(fname)

        with open(fname, "r") as f:
            try:
                json_data = json.load(f)
                timestamp_fetched = False
            except json.JSONDecodeError:
                log_writer.write(f"Error encountered on: {fname} \r\n")
                continue

            for key, item in json_data.items():
                # Each json file contains some useless meta-data,
                # actual flight data take shape of a list
                if not isinstance(item, list):
                    continue

                # Pick only flights that are coming to HK
                if item[12] != "HKG":
                    continue

                # Read the timestamp for the current file and read only once
                # Do one push every 24 hours = 86400 seconds
                if not timestamp_fetched and (item[10] - cutoff_time >= 86400):
                    cutoff_time = item[10]
                    flights.push(cutoff_time)

                flights.write(key, item)


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
