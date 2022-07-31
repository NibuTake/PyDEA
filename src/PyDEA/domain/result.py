from dataclasses import dataclass, field

import numpy as np

from PyDEA.domain import DMU


@dataclass
class Result:
    eff: float
    lambdas: list
    id: int
    sx: list = field(default_factory=list)
    sy: list = field(default_factory=list)
    is_slack: bool = False
    is_eff: bool = False
    dmu: DMU = DMU(np.nan, np.nan, 0)

    def _set_dmu(self, input: np.ndarray, output: np.ndarray, id: int):
        self.dmu = DMU(input, output, id)
