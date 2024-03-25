from dataclasses import dataclass

import numpy as np


@dataclass
class DMU:
    input: np.ndarray
    output: np.ndarray
    id: int


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
        # 'self.index is np.nan' sometimes cause bug: 'TypeError: 'float' object is not subscriptable'
        if np.all(np.isnan(self.index)):
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
class BooleanInput:
    _value: bool

    @property
    def value(self):
        return bool(self._value)
