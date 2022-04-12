import numpy as np


def find_first_turning(distances):
    """
    Find the first turning point from the array of distances.
    A turning point occur when the first difference changes sign,
    this can be check by checking the sign of product of first differences.
    """

    # To determine a turning point, we need at least 2 segments, 3 points.
    if len(distances) < 3:
        return None

    diff = distances[1:] - distances[:-1]
    prod = diff[1:] * diff[:-1]

    # Turning occurs <=> product of first differences <= 0
    ind = np.where(prod <= 0)[0]

    # Check if there is actually a turning point, return None if not
    if len(ind) == 0:
        return None

    # Again, to determine a turning point, we need at least 3 points.
    # So we the determination works only starting from the third point.
    # This is also reflected by len(prod) == len(distances) - 2.
    first = ind[0] + 2

    return first


def find_first_turning_dist(distances):

    first = find_first_turning(distances)
    if first is None:
        return -1

    return distances[first]
