from Pyfrontier.frontier_model import EnvelopDEA


def test_can_calculate_envelope(sample_data):

    dea = EnvelopDEA("VRS", "in")
    dea.fit(sample_data[["Day", "Cost"]].values, sample_data[["Ben"]].values)

    [print(r) for r in dea.result]
    assert True


def test_can_calculate_envelope_houses(house_data):
    frontier = "CRS"
    orient = "in"
    dea = EnvelopDEA(frontier, orient)
    dea.fit(house_data[["Fee", "House"]].values, house_data[["Income"]].values)

    [print(r) for r in dea.result]

    assert True
