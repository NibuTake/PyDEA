import abc
from dataclasses import dataclass
from typing import List

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
    """

    score: float
    id: int
    dmu: DMU
    weight: List[float]
    x_slack: List[float]
    y_slack: List[float]

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
    """

    score: float
    id: int
    dmu: DMU
    x_slack: List[float]
    y_slack: List[float]

    @property
    def is_efficient(self) -> bool:
        if np.sum(self.x_slack) + np.sum(self.y_slack) > 0:
            return False
        else:
            return True
