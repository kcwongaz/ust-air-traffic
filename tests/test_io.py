from air_traffic.io import *


def test_read_trajectories():

    dfs = read_trajectories("../data/cleaned", "2017-01-01")
    count = 0
    for df in dfs:
        count += 1
    print(count)


def test_read_trajectories_range():

    datasets = read_trajectories_range("../data/cleaned", "2017-01-01", "2017-01-02")
    
    for dfs in datasets:
        count = 0
        for df in dfs:
            count += 1
        print(count)


# test_read_trajectories()
test_read_trajectories_range()
