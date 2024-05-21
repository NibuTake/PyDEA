import pytest
from Pyfrontier.solver._models import Bias


class TestMultipleBias:
    def test_input_oriented_IRS_bias(self):
        bias = Bias("IRS", "in").value
        assert bias.lowBound == 0
        assert bias.upBound is None

    def test_output_oriented_IRS_bias(self):
        bias = Bias("IRS", "out").value
        assert bias.lowBound is None
        assert bias.upBound == 0

    def test_input_oriented_DRS_bias(self):
        bias = Bias("DRS", "in").value
        assert bias.lowBound is None
        assert bias.upBound == 0

    def test_output_oriented_DRS_bias(self):
        bias = Bias("DRS", "out").value
        assert bias.lowBound == 0
        assert bias.upBound is None

    @pytest.mark.parametrize(
        "orient",
        ["in", "out"],
    )
    def test_CRS_bias(self, orient):
        bias = Bias("CRS", orient).value
        assert bias == 0

    @pytest.mark.parametrize(
        "orient",
        ["in", "out"],
    )
    def test_VRS_bias(self, orient):
        bias = Bias("VRS", orient).value
        assert bias.lowBound is None
        assert bias.upBound is None
