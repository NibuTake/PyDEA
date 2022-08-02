from dataclasses import dataclass

import numpy as np

from Pyfrontier.domain import DMU


# @dataclass(frozen=True)
@dataclass
class EnvelopResult:
    score: float
    weight: list
    id: int
    dmu: DMU

    def __post_init__(self):
        if self.score == 1:
            self._is_efficient = True
        else:
            self._is_efficient = False

    @property
    def is_efficient(self) -> bool:
        return self._is_efficient

    @property
    def dict(self):
        pass

    def add_slack(self, x_slack: list, y_slack: list):
        self.x_slack = x_slack
        self.y_slack = y_slack

        if np.sum(x_slack) + np.sum(y_slack) > 0:
            self.has_slack = True
        else:
            self.has_slack = False

    def _set_dmu(self, input: np.ndarray, output: np.ndarray, id: int):
        self.dmu = DMU(input, output, id)
