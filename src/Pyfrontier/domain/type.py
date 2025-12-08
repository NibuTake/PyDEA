from dataclasses import dataclass
from typing import Literal


# Type alias for frontier parameter
FrontierType = Literal["CRS", "VRS", "NDRS", "NIRS"]


@dataclass
class Frontier:
    """Frontier type with validation for DEA models.
    """

    _frontier: FrontierType

    def __post_init__(self):
        self._validate_frontier()

    def _validate_frontier(self):
        valid_frontiers = ["CRS", "VRS", "NDRS", "NIRS"]
        if self._frontier not in valid_frontiers:
            raise ValueError(
                f"Invalid frontier value: '{self._frontier}'. "
                f"Must be one of {valid_frontiers}. "
            )

    @property
    def value(self) -> FrontierType:
        """Returns the validated frontier value."""
        return self._frontier
