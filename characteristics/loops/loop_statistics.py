import numpy as np


from loop_reader import *


# --------------------------------------------------------------------------- #
dstr = "20170101_0000-20171231_2359"

datadir = f"/home/kc/Research/air_traffic/data/fr24_clean/spacetime/{dstr}"
savedir = f"/home/kc/Research/air_traffic/data/loops"
savename = f"{savedir}/{dstr}.csv"

reread = True


# --------------------------------------------------------------------------- #
def loop_length(data):

    length = []
    for x in data:
        x = np.array(x, dtype=float)
        diff = x[1:] - x[:-1]
        length.extend(diff)

    return length


def loop_length_seq(data):

    length = []
    for x in data:
        x = np.array(x, dtype=float)
        diff = x[1:] - x[:-1]
        length.append(np.average(diff))

    return length


def loop_total(data):

    length = []
    for x in data:
        x = np.array(x, dtype=float)
        length.append(x[-1] - x[0])

    return length


def loop_count(data):

    count = []
    for x in data:
        count.append(len(x) - 1)  # The last point is always the exit point

    return count


# --------------------------------------------------------------------------- #
# Read in loop data
if reread:
    loop_write(datadir, savename)

data = loop_read_sepreated(savename)

# --------------------------------------------------------------------------- #
for k in data:

    np.savetxt(f"{savedir}/loop_len_{k}_{dstr}.txt", loop_length(data[k]))
    np.savetxt(f"{savedir}/loop_len_seq_{k}_{dstr}.txt", loop_length_seq(data[k]))
    np.savetxt(f"{savedir}/loop_total_{k}_{dstr}.txt", loop_total(data[k]))
    np.savetxt(f"{savedir}/loop_count_{k}_{dstr}.txt", loop_count(data[k]))
