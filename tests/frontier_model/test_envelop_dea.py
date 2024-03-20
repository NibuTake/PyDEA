import time

import pandas as pd
import numpy as np

from Pyfrontier.frontier_model import EnvelopDEA


def test_can_calculate_envelope(sample_data):

    dea = EnvelopDEA("VRS", "in")
    dea.fit(sample_data[["Day", "Cost"]].values, sample_data[["Ben"]].values)

    [print(r) for r in dea.result]
    assert True


def test_parallel_can_work(sample_data):
    default_dea = EnvelopDEA("VRS", "in")
    start_time = time.time()
    default_dea.fit(sample_data[["Day", "Cost"]].values, sample_data[["Ben"]].values)
    default_time = round(time.time() - start_time)
    default_result = np.asarray([r.score for r in default_dea.result])

    parallel_dea = EnvelopDEA("VRS", "in", n_jobs=2)
    start_time = time.time()
    parallel_dea.fit(sample_data[["Day", "Cost"]].values, sample_data[["Ben"]].values)
    parallel_time = round(time.time() - start_time)
    parallel_result = np.asarray([r.score for r in parallel_dea.result])

    print("default mode time consumed: {}s".format(default_time))
    print("parallel mode time consumed: {}s".format(parallel_time))

    assert bool(np.all(np.equal(default_result, parallel_result)))


def test_can_calculate_envelope_houses(house_data):
    frontier = "CRS"
    orient = "in"
    dea = EnvelopDEA(frontier, orient)
    dea.fit(house_data[["Fee", "House"]].values, house_data[["Income"]].values)

    [print(r) for r in dea.result]

    assert True


def test_super_efficiency(house_data):
    frontier = "CRS"
    orient = "in"
    dea = EnvelopDEA(frontier, orient, super_efficiency=True)

    df = pd.DataFrame(
        {"cost": [1, 2, 4, 6, 4], "time": [5, 2, 1, 1, 4], "profit": [2, 2, 2, 2, 2]}
    )
    dea.fit(df[["cost", "time"]].to_numpy(), df[["profit"]].to_numpy())

    for r in dea.result:
        print(r.score)

    assert True
