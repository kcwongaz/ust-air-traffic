import numpy as np


def seasonal_difference(timeseries, dt, period):
    """
    Remove additive seasonal trend by seaonsal differencing,
    i.e. X(t) -> X(t) - X(t - period)

    The new time series will have one less period in length
    """

    n = period // dt
    diff = [timeseries[i] - timeseries[i - n]
            for i in range(n, len(timeseries))]

    return diff


def seasonal_quotient(timeseries, dt, period):
    """
    Remove multiplicative seasonal trend by seaonsal quotienting,
    i.e. X(t) -> X(t)/X(t - period)

    The new time series will have one less period in length
    """

    n = period // dt
    diff = [timeseries[i] / timeseries[i - n]
            for i in range(n, len(timeseries))]

    return diff


def seasonal_mean(timeseries, dt, period):
    """
    Compute the seasonal mean
    """

    n = period // dt
    n_period = len(timeseries) // n

    mean = np.zeros(n)
    for i in range(n):
        sample = [timeseries[m*n + i] for m in range(n_period-1)]
        mean[i] = np.mean(sample)

    return mean


def remove_seasonal_mean(timeseries, dt, period):
    """
    Remove seasonal trend by substracting the seasonal mean
    """

    n = period // dt

    mean = seasonal_mean(timeseries, dt, period)

    # Substract the seasonal mean elementwise to avoid edge effects
    detrended = np.zeros(len(timeseries))
    for i in range(len(detrended)):
        i_trend = i % n
        detrended[i] = timeseries[i] - mean[i_trend]

    return detrended
