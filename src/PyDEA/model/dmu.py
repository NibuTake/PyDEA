from dataclasses import dataclass, field

import numpy as np


@dataclass
class DMUSet:
    """Dataset for DEA"""

    inputs: np.ndarray
    outputs: np.ndarray
    index: np.ndarray = np.nan

    def __post_init__(self):
        self._set_dimension()
        # TODO: validation

    def _set_dimension(self):
        self._N = self.inputs.shape[0]
        self._m = self.inputs.shape[1]
        self._s = self.outputs.shape[1]

    def get_id(self, o: int):
        if self.index is np.nan:
            return o
        else:
            return self.index[o]

    @property
    def N(self):
        return self._N

    @property
    def m(self):
        return self._m

    @property
    def s(self):
        return self._s


@dataclass
class DMU:
    input: np.ndarray
    output: np.ndarray
    id: int


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
