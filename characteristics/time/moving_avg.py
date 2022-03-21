import numpy as np
from scipy.stats import binned_statistic


def moving_avg(x, t, dt, start_hour=-1, start_by="pad"):
    """
    Compute the moving average of x(t) within (t-dt, t).
    Return the computed average along with an array containing the
    corresponding time values.

    The start of the time array depends on the first time point.
    Specifying start_hour != -1 force the time axis start at the wanted hour.
    Specifying start_hour == -1 will simply start from the first recorded time

    start_by specify the method for offseting the time axis.
        pad: Pad zeros up to the start point, so we don't lose data
        cut: Cut data down to the start point, so we don't add extra zeros

    (!) When UTC timestamps are inputted for arr_times, the resulting
        counts will also be in UTC.
    """

    # 1 - Sort the input data in timed order
    ind = np.argsort(t)
    t = t[ind]
    x = x[ind]
    first = t[0]

    # 2 - Compute the first point of the time axis
    if start_hour == -1:
        t0 = first
    else:
        first_sec = first % 86400
        start_sec = 3600 * start_hour
        delta = first_sec - start_sec

        if start_by == "pad":
            if delta >= 0:
                t0 = first - delta
            else:
                t0 = first - 86400 - delta

        elif start_by == "cut":
            if delta <= 0:
                t0 = first - delta
            else:
                t0 = first + 86400 - delta

    # The first valid time point is t0 + dt because we have no data before t0
    t_axis = np.arange(t0 + dt, t[-1] + dt, dt)

    # Compute the arrivial count by histogram
    bins = np.insert(t_axis, 0, t0)
    avg, _, _ = binned_statistic(t, x, statistic="mean", bins=bins)

    return avg, t_axis
