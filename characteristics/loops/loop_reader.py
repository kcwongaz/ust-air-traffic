import numpy as np
import csv
import os

from loop_helpers import *


def loop_write(datadir, savename):

    with open(savename, mode="w") as f:
        writer = csv.writer(f, delimiter=',', quotechar='"',
                            quoting=csv.QUOTE_MINIMAL)

        for subdir, dirs, files in os.walk(datadir):
            for file in files:
                fname = os.path.join(subdir, file)
                print(fname)

                if file == "fnames.txt":
                    continue

                data = np.loadtxt(fname)
                data = data[data[:, 1] <= 200]
                min_loc = locate_loops(data)

                _, min_time = find_minima_spacetime(data[:, 1], data[:, 0], min_loc)

                # No loop
                if len(min_time) == 0:
                    continue

                _, exit_time = find_exitpoint(data[:, 1], data[:, 0], min_loc)

                # Determine entry direction #
                lat = data[0, 2]
                lon = data[0, 3]

                if lon < 114:
                    group = "W"
                elif lat > 21:
                    group = "NE"
                else:
                    group = "SE"

                row = [group]
                row.extend(min_time)
                row.append(exit_time)
                print(row)
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


def loop_read_sepreated(fname):

    data = loop_read(fname)
    data_sep = {}

    for entry in data:
        area = entry[0]

        if area not in data_sep:
            data_sep[area] = []
        else:
            data_sep[area].append(entry[1:])

    return data_sep
