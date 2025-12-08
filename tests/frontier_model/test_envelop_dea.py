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


class TestEnvelopeFrontierLambda:
    def test_NIRS(self, house_data):
        multiple_dea = EnvelopDEA("NIRS", "in")
        multiple_dea.fit(
            house_data[["Fee", "House"]].values, house_data[["Income"]].values
        )
        for r in multiple_dea.result:
            assert sum(r.weights) <= 1

    def test_NDRS(self, house_data):
        multiple_dea = EnvelopDEA("NDRS", "in")
        multiple_dea.fit(
            house_data[["Fee", "House"]].values, house_data[["Income"]].values
        )
        for r in multiple_dea.result:
            assert sum(r.weights) >= 1


class TestEnvelopeFrontierVirtualDmu:
    """
    Test that virtual DMUs (projections onto efficient frontier) are all efficient.

    This validates that the virtual_dmu property correctly projects inefficient DMUs
    onto the efficient frontier. When re-evaluated, all virtual DMUs should have
    efficiency scores of 1.0 (within numerical tolerance).
    """

    def test_virtual_dmu_input_oriented_VRS(self, sample_data):
        """Virtual DMUs should all have efficiency score = 1 (input-oriented VRS)."""
        # First DEA analysis
        dea = EnvelopDEA("VRS", "in")
        dea.fit(sample_data[["Day", "Cost"]].values, sample_data[["Ben"]].values)

        # Extract virtual DMUs from results
        virtual_inputs = np.array([r.virtual_dmu.input for r in dea.result])
        virtual_outputs = np.array([r.virtual_dmu.output for r in dea.result])

        # Second DEA analysis on virtual DMUs
        dea_virtual = EnvelopDEA("VRS", "in")
        dea_virtual.fit(virtual_inputs, virtual_outputs)

        # All virtual DMUs should be efficient (score = 1.0)
        for r in dea_virtual.result:
            assert r.score == 1.0, f"Virtual DMU {r.id} has score {r.score}, expected 1.0"

    def test_virtual_dmu_output_oriented_VRS(self, sample_data):
        """Virtual DMUs should all have efficiency score = 1 (output-oriented VRS)."""
        # First DEA analysis
        dea = EnvelopDEA("VRS", "out")
        dea.fit(sample_data[["Day", "Cost"]].values, sample_data[["Ben"]].values)

        # Extract virtual DMUs from results
        virtual_inputs = np.array([r.virtual_dmu.input for r in dea.result])
        virtual_outputs = np.array([r.virtual_dmu.output for r in dea.result])

        # Second DEA analysis on virtual DMUs
        dea_virtual = EnvelopDEA("VRS", "out")
        dea_virtual.fit(virtual_inputs, virtual_outputs)

        # All virtual DMUs should be efficient (score = 1.0)
        for r in dea_virtual.result:
            assert r.score == 1.0, f"Virtual DMU {r.id} has score {r.score}, expected 1.0"

    def test_virtual_dmu_input_oriented_CRS(self, house_data):
        """Virtual DMUs should all have efficiency score ≈ 1 (input-oriented CRS)."""
        # First DEA analysis
        dea = EnvelopDEA("CRS", "in")
        dea.fit(house_data[["Fee", "House"]].values, house_data[["Income"]].values)

        # Extract virtual DMUs from results
        virtual_inputs = np.array([r.virtual_dmu.input for r in dea.result])
        virtual_outputs = np.array([r.virtual_dmu.output for r in dea.result])

        # Second DEA analysis on virtual DMUs
        dea_virtual = EnvelopDEA("CRS", "in")
        dea_virtual.fit(virtual_inputs, virtual_outputs)

        # All virtual DMUs should be approximately efficient (score ≈ 1.0)
        # Using tolerance to account for floating-point rounding errors
        for r in dea_virtual.result:
            np.testing.assert_almost_equal(
                r.score, 1.0, decimal=5,
                err_msg=f"Virtual DMU {r.id} has score {r.score}, expected ≈1.0"
            )

    def test_virtual_dmu_output_oriented_CRS(self, house_data):
        """Virtual DMUs should all have efficiency score ≈ 1 (output-oriented CRS)."""
        # First DEA analysis
        dea = EnvelopDEA("CRS", "out")
        dea.fit(house_data[["Fee", "House"]].values, house_data[["Income"]].values)

        # Extract virtual DMUs from results
        virtual_inputs = np.array([r.virtual_dmu.input for r in dea.result])
        virtual_outputs = np.array([r.virtual_dmu.output for r in dea.result])

        # Second DEA analysis on virtual DMUs
        dea_virtual = EnvelopDEA("CRS", "out")
        dea_virtual.fit(virtual_inputs, virtual_outputs)

        # All virtual DMUs should be approximately efficient (score ≈ 1.0)
        # Using tolerance to account for floating-point rounding errors
        for r in dea_virtual.result:
            np.testing.assert_almost_equal(
                r.score, 1.0, decimal=5,
                err_msg=f"Virtual DMU {r.id} has score {r.score}, expected ≈1.0"
            )
