import numpy as np


def find_first_turning(dist):
    """
    Find the first turning point from the array of distances.
    A turning point occur when the first difference changes sign,
    this can be check by checking the sign of product of first differences.
    """

    # To determine a turning point, we need at least 2 segments, 3 points.
    if len(dist) < 3:
        return None

    diff = dist[1:] - dist[:-1]
    prod = diff[1:] * diff[:-1]

    # Turning occurs <=> product of first differences <= 0
    ind = np.where(prod <= 0)[0]

    # Check if there is actually a turning point, return None if not
    if len(ind) == 0:
        return None

    # Again, to determine a turning point, we need at least 3 points,
    # and we can only determine if the interior point(s) have a turning.
    # We cannot determine if the two ends points are turning points.
    # This is also reflected by len(prod) == len(distances) - 2.
    first = ind[0] + 1

    return first


def find_first_turning_dist(dist):

    first = find_first_turning(dist)
    if first is None:
        return -1

    return dist[first]


def find_minima(dist, loop_loc):

    # Keep only points in the loop region
    ind = np.where((dist >= loop_loc[0]) & (dist <= loop_loc[1]))
    dist = dist[ind]
    time = time[ind]

    # To determine a turning point, we need at least 2 segments, 3 points.
    if len(dist) < 3:
        return None

    diff = dist[1:] - dist[:-1]
    prod = diff[1:] * diff[:-1]
    diff2 = diff[1:] - diff[:-1]

    # Minimium occurs iff:
    # (i) product of first differences <= 0
    # (ii) second differences > 0
    ind = np.where((prod <= 0) & (diff2 > 0))[0]

    # Return empty list if there is not a minima
    if len(ind) == 0:
        return []

    # We can identify minima only in the interior of the array
    # for the same reason explained in find_first_turning(dist)
    minima = ind + 1

    return minima


def find_minima_spacetime(dist, time, loop_loc):

    minima = find_minima(dist, loop_loc)

    if len(minima) == 0:
        return []

    min_dist = dist[minima]
    min_time = time[minima]

    return min_dist, min_time


def find_exitpoint(dist, time, loop_loc):
    """
    Find exit point of the loops by searching for the first point where
    the aircraft return to the same distance as the last minimum.
    """

    minima = find_minima(dist, loop_loc)

    # Exit point is undefined when there is no loop
    if len(minima) == 0:
        return None

    dist_after = dist[minima[-1]:]
    time_after = time[minima[-1]:]
    exitpoint = np.argmin(np.abs(dist_after - dist[minima[-1]]))

    exit_dist = dist_after[exitpoint]
    exit_time = time_after[exitpoint]

    return exit_dist, exit_time


def sort_flight_exitpoint():
    pass


def redirect_flight():
    pass
