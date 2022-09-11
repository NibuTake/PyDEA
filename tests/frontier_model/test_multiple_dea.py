import math

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
