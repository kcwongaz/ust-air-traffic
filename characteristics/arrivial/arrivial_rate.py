import numpy as np


def arrivial_rate(arr_times, dt, start_hour=-1, start_by="pad"):
    """
    Compute the arrivial rate by counting the number of arrivial in (t-dt, t).
    Return the computed rate along with an array containing the
    corresponding time values.

    The start of the time array depends on the first arrivial time,
    specifying start_hour != -1 force the time axis start at the wanted hour.

    start_by specify the method for offseting the time axis.
        pad: Pad zeros up to the start point, so we don't lose data
        cut: Cut data down to the start point, so we don't add extra zeros

    (!) When UTC timestamps are inputted for arr_times, the resulting
        counts will also be in UTC.
    """

    arr_times = np.sort(arr_times)
    first = arr_times[0]

    # Compute the first point of the time axis
    if start_hour == -1:
        t0 = first
    else:
        first_sec = first % 86400
        start_sec = 3600*start_hour
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
    t_axis = np.arange(t0 + dt, arr_times[-1] + dt, dt)

    # Compute the arrivial count by histogram
    bins = np.insert(t_axis, 0, t0)
    count, _ = np.histogram(arr_times, bins)

    return count, t_axis


def fold_timeseries(timeseries, dt, foldsize):
    """
    Fold a timeseries onto a given time-window size
    """

    n = round(foldsize / dt)
    total_len = int(len(timeseries) / n)

    folded = [timeseries[k*n:(k+1)*n] for k in range(total_len)]
    return folded


def nullify_day(timeseries, dt):
    """
    Replace value by nan if the whole day contains no data
    """

    # Number of point per day
    n = 86400 // dt

    # Change data type to float to allow nan
    timeseries = timeseries.astype(np.float64)

    # Fold data into daily winodw
    folded = fold_timeseries(timeseries, dt, foldsize=86400)
    for i, window in enumerate(folded):

        # If there is not a single flight in a day,
        # replace all zeros to nan
        if np.sum(window) == 0:
            print("Found empty day!")
            for j in range(-n, 2*n):
                timeseries[i*n + j] = np.nan

    return timeseries


def autocorr(timeseries, dt, lag_max):
    """
    Compute the autocorrelation coefficient for a stationary time series.
    Up to lag_max of time lag.
    """

    if lag_max > (dt * len(timeseries)):
        lag_max = (dt * len(timeseries))

    n_max = lag_max // dt
    a = np.zeros(n_max + 1)
    mean = np.nanmean(timeseries)
    var = np.nanvar(timeseries)

    for n in range(n_max + 1):
        sample = [timeseries[i]*timeseries[i+n]
                  for i in range(len(timeseries) - n)]

        a[n] = np.nanmean(sample) - mean*mean
        a[n] /= var

    return a


def autocorr_period(timeseries, dt, period):
    """
    Compute the autocorrelation coefficient for a periodic time series
    """

    n = round(period / dt)
    n_period = int(len(timeseries) / n)
    a_matrix = np.zeros((n, n))

    mean = np.zeros(n)
    var = np.zeros(n)
    for i in range(n):
        sample = [timeseries[m*n + i] for m in range(n_period-1)]
        mean[i] = np.nanmean(sample)
        var[i] = np.nanvar(sample)

    for i in range(n):
        for j in range(n):
            sample = [timeseries[m*n + i] * timeseries[m*n + i + j]
                      for m in range(n_period-1)]

            j_mod = (i+j) % n
            a_matrix[i, j] = np.nanmean(sample) - mean[i]*mean[j_mod]
            a_matrix[i, j] /= np.sqrt(var[i] * var[j_mod])

    return a_matrix


def autocovar_period(timeseries, dt, period, cumulant=True):
    """
    Compute the autocorrelation function for a periodic time series.
    This is also called the autocovariance.

    When cumulant is True, compute <X(t)X(t+T)> - <X(t)><X(t+T)>,
         cumulant is False, compute <X(t)X(t+T)>
    """

    n = round(period / dt)
    n_period = int(len(timeseries) / n)
    a_matrix = np.zeros((n, n))

    if cumulant:
        mean = np.zeros(n)
        for i in range(n):
            sample = [timeseries[m*n + i] for m in range(n_period-1)]
            mean[i] = np.nanmean(sample)

    for i in range(n):
        for j in range(n):
            sample = [timeseries[m*n + i] * timeseries[m*n + i + j]
                      for m in range(n_period-1)]

            a_matrix[i, j] = np.nanmean(sample)

            if cumulant:
                a_matrix[i, j] -= mean[i]*mean[(i+j) % n]

    return a_matrix


def autocorr_period_ext(timeseries, dt, period, n_period):
    """
    Compute the autocorrelation coefficient for a periodic time series;
    extended for n_period of periods
    """

    # If doing for just one period
    if n_period == 1:
        return autocorr_period(timeseries, dt, period)

    # Number of time steps in a period and in n periods
    ts_1 = period // dt
    ts_n = (period * n_period) // dt

    # Number of periods that can fit in the time series data
    num_period = len(timeseries) // ts_1

    a_matrix = np.zeros((ts_1, ts_n))

    mean = np.zeros(ts_1)
    var = np.zeros(ts_1)
    for i in range(ts_1):
        sample = [timeseries[m*ts_1 + i] for m in range(num_period-1)]
        mean[i] = np.nanmean(sample)
        var[i] = np.nanvar(sample)

    for i in range(ts_1):
        for j in range(ts_n):
            sample = [timeseries[m*ts_1 + i] * timeseries[m*ts_1 + i + j]
                      for m in range(num_period-n_period)]

            j_mod = (i+j) % ts_1
            a_matrix[i, j] = np.nanmean(sample) - mean[i]*mean[j_mod]
            a_matrix[i, j] /= np.sqrt(var[i] * var[j_mod])

    return a_matrix
