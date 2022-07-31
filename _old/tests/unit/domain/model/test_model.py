from model.model import EnvelopeDEA


def test_can_calculate_envelope(sample_data):
    frontier = "VRS"
    orient = "in"
    envelope_dea = EnvelopeDEA(frontier, orient)
    res = envelope_dea.fit(
        sample_data[["Day", "Cost"]].values, sample_data[["Ben"]].values
    )

    [print(r) for r in res]
    assert True


def test_can_calculate_envelope_houses(house_data):
    frontier = "CRS"
    orient = "in"
    envelope_dea = EnvelopeDEA(frontier, orient)
    res = envelope_dea.fit(
        house_data[["Fee", "House"]].values, house_data[["Income"]].values
    )

    [print(r) for r in res]

    assert True
