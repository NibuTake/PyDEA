import math

import numpy as np

from Pyfrontier.frontier_model import EnvelopDEA, MultipleDEA


def test_can_calculate_envelope_houses(house_data):
    frontier = "CRS"
    orient = "in"
    envelope_dea = EnvelopDEA(frontier, orient)
    envelope_dea.fit(house_data[["Fee", "House"]].values, house_data[["Income"]].values)

    multiple_dea = MultipleDEA(frontier, orient)
    multiple_dea.fit(house_data[["Fee", "House"]].values, house_data[["Income"]].values)

    for r_envelope, r_multiple in zip(envelope_dea.result, multiple_dea.result):
        assert math.isclose(r_envelope.score, r_multiple.score, rel_tol=1e-5)


def test_parallel_can_work_on_multiple_model(sample_data):
    default_dea = MultipleDEA("VRS", "in")
    default_dea.fit(sample_data[["Day", "Cost"]].values, sample_data[["Ben"]].values)
    default_result = np.asarray([r.score for r in default_dea.result])

    parallel_dea = MultipleDEA("VRS", "in", n_jobs=2)
    parallel_dea.fit(sample_data[["Day", "Cost"]].values, sample_data[["Ben"]].values)
    parallel_result = np.asarray([r.score for r in parallel_dea.result])

    assert bool(np.all(np.equal(default_result, parallel_result)))


def test_can_assurance_region(house_data):
    frontier = "CRS"
    orient = "in"

    multiple_dea = MultipleDEA(frontier, orient)
    multiple_dea.add_assurance_region(
        "in", index_a=0, index_b=1, coefficient=1, operator=">="
    )

    multiple_dea.fit(house_data[["Fee", "House"]].values, house_data[["Income"]].values)

    [r for r in multiple_dea.result]
    assert True


class TestFrontierBias:
    def test_input_oriented_DRS(self, house_data):
        multiple_dea = MultipleDEA("DRS", "in")
        multiple_dea.fit(
            house_data[["Fee", "House"]].values, house_data[["Income"]].values
        )
        assert all([r.bias <= 0 for r in multiple_dea.result])

    def test_output_oriented_DRS(self, house_data):
        multiple_dea = MultipleDEA("DRS", "out")
        multiple_dea.fit(
            house_data[["Fee", "House"]].values, house_data[["Income"]].values
        )
        assert all([r.bias >= 0 for r in multiple_dea.result])

    def test_input_oriented_IRS(self, house_data):
        multiple_dea = MultipleDEA("IRS", "in")
        multiple_dea.fit(
            house_data[["Fee", "House"]].values, house_data[["Income"]].values
        )
        assert all([r.bias >= 0 for r in multiple_dea.result])

    def test_output_oriented_IRS(self, house_data):
        multiple_dea = MultipleDEA("IRS", "out")
        multiple_dea.fit(
            house_data[["Fee", "House"]].values, house_data[["Income"]].values
        )
        assert all([r.bias <= 0 for r in multiple_dea.result])
