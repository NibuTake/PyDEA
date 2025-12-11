from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class DMU:
    input: np.ndarray
    output: np.ndarray
    id: int
    label: Optional[str] = None


@dataclass
class DMUSet:
    """Dataset for DEA"""

    inputs: np.ndarray
    outputs: np.ndarray
    index: np.ndarray = np.nan
    labels: Optional[np.ndarray] = None

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

    def get_label(self, o: int) -> Optional[str]:
        """Get label for DMU at position o."""
        if self.labels is None:
            return None
        return self.labels[o]

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
