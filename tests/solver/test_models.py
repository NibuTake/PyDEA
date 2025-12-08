import pytest
from Pyfrontier.solver._models import Bias


class TestMultipleBias:
    def test_input_oriented_NDRS_bias(self):
        bias = Bias("NDRS", "in").value
        assert bias.lowBound == 0
        assert bias.upBound is None

    def test_output_oriented_NDRS_bias(self):
        bias = Bias("NDRS", "out").value
        assert bias.lowBound is None
        assert bias.upBound == 0

    def test_input_oriented_NIRS_bias(self):
        bias = Bias("NIRS", "in").value
        assert bias.lowBound is None
        assert bias.upBound == 0

    def test_output_oriented_NIRS_bias(self):
        bias = Bias("NIRS", "out").value
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
