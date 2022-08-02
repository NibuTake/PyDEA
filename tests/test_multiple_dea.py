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
        assert math.isclose(r_envelope.score, r_multiple["eff"], rel_tol=1e-7)
