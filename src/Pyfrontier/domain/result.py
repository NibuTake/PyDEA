import abc
from dataclasses import dataclass
from typing import List, Literal

import numpy as np

from Pyfrontier.domain import DMU


@dataclass(frozen=True)
class BaseResult(abc.ABC):
    score: float
    id: int
    dmu: DMU


@dataclass(frozen=True)
class EnvelopResult(BaseResult):
    """
    - score: efficiency
    - id:
    - dmu:
    - weight:
    - x_slack:
    - y_slack:
    - orientation: "in" for input-oriented, "out" for output-oriented
    """

    score: float
    id: int
    dmu: DMU
    weights: List[float]
    x_slack: List[float]
    y_slack: List[float]
    orientation: Literal["in", "out"]

    def __post_init__(self):
        pass

    @property
    def is_efficient(self) -> bool:
        if self.score == 1:
            return not self.has_slack
        else:
            return False

    @property
    def has_slack(self) -> bool:
        if np.sum(self.x_slack) + np.sum(self.y_slack) > 0:
            return True
        else:
            return False

    @property
    def virtual_dmu(self) -> DMU:
        """
        Returns the virtual DMU (projection onto the efficient frontier).

        The virtual DMU represents the target values that an inefficient DMU
        should achieve to become efficient, based on DEA theory.

        For input-oriented models:
            - projected_input = score * original_input - input_slack
            - projected_output = original_output + output_slack

        For output-oriented models:
            - projected_input = original_input - input_slack
            - projected_output = score * original_output + output_slack

        Returns:
            DMU: A new DMU object with projected input and output values
        """
        if self.orientation == "in":
            projected_input = self.score * self.dmu.input - np.array(self.x_slack)
            projected_output = self.dmu.output + np.array(self.y_slack)
        else:  # "out"
            projected_input = self.dmu.input - np.array(self.x_slack)
            projected_output = self.score * self.dmu.output + np.array(self.y_slack)

        return DMU(
            input=projected_input,
            output=projected_output,
            id=self.dmu.id,
        )


@dataclass(frozen=True)
class MultipleResult(BaseResult):
    """
    - score: efficiency
    - id:
    - dmu:
    - x_weight:
    - y_weight:
    - bias:
    """

    score: float
    id: int
    dmu: DMU
    x_weight: List[float]
    y_weight: List[float]
    bias: float

    def __post_init__(self):
        pass

    @property
    def is_efficient(self) -> bool:
        if self.score == 1:
            return True
        else:
            return False


@dataclass(frozen=True)
class AdditiveResult(BaseResult):
    """
    - score: efficiency
    - id:
    - dmu:
    - x_slack:
    - y_slack:
    - weights: lambda
    """

    score: float
    id: int
    dmu: DMU
    x_slack: List[float]
    y_slack: List[float]
    weights: List[float]

    @property
    def is_efficient(self) -> bool:
        if np.sum(self.x_slack) + np.sum(self.y_slack) > 0:
            return False
        else:
            return True
