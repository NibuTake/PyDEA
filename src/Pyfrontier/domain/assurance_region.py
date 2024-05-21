from dataclasses import dataclass
from typing import Literal


@dataclass
class AssuranceRegion:
    """
    - x_a/x_b =< coefficient
    - coefficient <= x_a/x_b
    """

    type: Literal["input", "output"]
    index_a: int
    index_b: int
    coefficient: float
    operator: Literal["=<", ">="]
