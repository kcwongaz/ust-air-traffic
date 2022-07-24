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


def find_minima(dist, min_loc):

    # To determine a turning point, we need at least 2 segments, 3 points.
    if len(dist) < 3:
        return []

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

    # Filter out those that are not in the range specified by min_loc
    min_dist = dist[minima]
    ind = np.where((min_dist >= min_loc[0]) & (min_dist <= min_loc[1]))
    minima = minima[ind]

    return minima


def find_minima_spacetime(dist, time, min_loc):

    minima = find_minima(dist, min_loc)

    if len(minima) == 0:
        return [], []

    min_dist = dist[minima]
    min_time = time[minima]

    return min_dist, min_time


def find_exitpoint(dist, time, min_loc):
    """
    Find exit point of the loops by searching for the first point where
    the aircraft return to the same distance as the last minimum.
    """

    minima = find_minima(dist, min_loc)

    # Exit point is undefined when there is no loop
    if len(minima) == 0:
        return None, None

    # Skip one more point to avoid having constant segments
    dist_after = dist[minima[-1] + 2:]
    time_after = time[minima[-1] + 2:]
    exitpoint = np.argmin(np.abs(dist_after - dist[minima[-1]]))

    exit_dist = dist_after[exitpoint]
    exit_time = time_after[exitpoint]

    return exit_dist, exit_time


def label_flight_loops(flight_dict):
    """
    Generate a dict labeling where the loops locate in each flight.
    This is done by finding which candidate regions out of 'locations' has
    the most numbr of loops.

    If there are no loop, it will just label the flight to have the first
    loop region. This should not cause a problem, because upon find_minima()
    in the area, the loop search will return [].

    It is acutally not necessary to complete distinguish the three loops area,
    just locating whether the loops are in the upper of lower region in the
    spacetime graph is sufficent for my purpose. The tricker part is flight
    from North always produces a 'fake' loop.
    """

    min_loc = {}

    for key in flight_dict:
        min_loc[key] = locate_loops(flight_dict[key])

    return min_loc


def locate_loops(flight):
    """
    Locate the loop location for a single flight.
    """

    # locations = [(70, 80), (90, 102), (103, 125)]

    # It is not necessary to completely distinguish the three loops area
    locations = [(70, 80), (90, 130)]

    dist = flight[:, 1]
    loop_num = [len(find_minima(dist, loc)) for loc in locations]
    min_loc = locations[np.argmax(loop_num)]

    return min_loc


def label_flight_dir(flight_dict):
    """
    Generate a dict labeling where the loops locate in each flight.
    This is done looking at which direction does the flight come in.
    """

    min_loc = {}
    for key in flight_dict:
        dist = flight_dict[key][:, 1]
        ind = np.where(dist <= 200)  # look only at the later part of the flight

        lat = flight_dict[key][ind, 2]
        lon = flight_dict[key][ind, 3]

    return min_loc


def sort_flight_keys(flight_dict, min_loc):

    # Build the list of flight with loops in the designated area
    flight_exit = []
    keys = []

    for key in flight_dict:
        time = flight_dict[key][:, 0]
        dist = flight_dict[key][:, 1]

        if type(min_loc) is dict:
            min_loc_this = min_loc[key]
        else:
            min_loc_this = min_loc

        _, exit_time = find_exitpoint(dist, time, min_loc_this)

        # Only flights with loops in target region are kept
        if exit_time is not None:
            flight_exit.append(exit_time)
            keys.append(key)

    # Sort the list of flight by exist time
    ind_sort = np.argsort(flight_exit)

    flight_exit = np.array(flight_exit)
    flight_exit = flight_exit[ind_sort]
    keys = np.array(keys)
    keys = keys[ind_sort]

    return keys, flight_exit


def sort_flight_minima(flight_dict, min_loc):

    flight_min = []
    flight_dist = []

    keys, flight_exit = sort_flight_keys(flight_dict, min_loc)

    for k in keys:
        time = flight_dict[k][:, 0]
        dist = flight_dict[k][:, 1]

        if type(min_loc) is dict:
            min_loc_this = min_loc[k]
        else:
            min_loc_this = min_loc

        min_dist, min_time = find_minima_spacetime(dist, time, min_loc_this)

        flight_min.append(min_time)
        flight_dist.append(min_dist)

    return flight_min, flight_exit, flight_dist


def redirect_flight(flight_min, flight_exit, target, tol=60):
    """
    Intake a sorted list of flight loop minima and the corresponding exit points,
    then compute the time saved after the target flight (indexed by exit order)
    got redirected.
    """

    s = []
    while target is not None:
        exit_this = flight_exit[target]
        t_saved = np.zeros(len(flight_min))

        for i in range(target + 1, len(flight_min)):
            matched = flight_min[i][np.abs(flight_min[i] - exit_this) < tol]

            if len(matched) > 0:
                t_saved[i] = flight_exit[i] - matched[0]
            if len(matched) > 1:
                print("Warning: More than one match found!")

        # If there are no promotable flight, end the search.
        # If there are more than one promotable flight, choose the one gives
        # the largest save (greedy search)
        if np.sum(t_saved) == 0:
            target = None
            s.append(0)
        else:
            # Greedy search
            target = np.argmax(t_saved)

            # Priority preserving search
            # target = np.nonzero(t_saved)[0][0]
            s.append(t_saved[target])

    s = np.array(s)
    return s


def detect_selection_problem(flight_min, flight_exit, tol=60):
    count = 0

    for target in range(len(flight_min)):
        exit_this = flight_exit[target]
        t_saved = np.zeros(len(flight_min))

        for i in range(target + 1, len(flight_min)):
            matched = flight_min[i][np.abs(flight_min[i] - exit_this) < tol]

            if len(matched) > 0:
                t_saved[i] = flight_exit[i] - matched[0]
            if len(matched) > 1:
                print("Warning: More than one match found!")

        # Compute how many candidate promotion is there
        num_selection = len(np.nonzero(t_saved)[0])
        if num_selection > 1:
            count += 1

    return count
