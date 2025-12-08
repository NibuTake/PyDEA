import pytest

from Pyfrontier.domain.type import Frontier


class TestFrontier:
    @pytest.mark.parametrize(
        "valid_frontier",
        ["CRS", "VRS", "NDRS", "NIRS"],
    )
    def test_valid_frontier_values(self, valid_frontier):
        """Test that valid frontier values are accepted."""
        frontier = Frontier(valid_frontier)
        assert frontier.value == valid_frontier

    @pytest.mark.parametrize(
        "invalid_frontier",
        ["IRS", "DRS", "invalid", "crs", "vrs", "", None, 123],
    )
    def test_invalid_frontier_values(self, invalid_frontier):
        """Test that invalid frontier values raise ValueError."""
        with pytest.raises(ValueError) as exc_info:
            Frontier(invalid_frontier)

        assert "Invalid frontier value" in str(exc_info.value)
