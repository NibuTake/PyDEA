from dataclasses import dataclass

import numpy as np


@dataclass
class SlackWeight:
    _weights: np.ndarray = np.array([])
    _n_dim: int = 0

    def __post_init__(self):
        self._reset_weight()
        self._has_same_dim()
        self._is_positive()

    @property
    def value(self) -> np.ndarray:
        if np.sum(self._weights) > 0:
            return self._weights / np.sum(self._weights)
        else:
            return self._weights

    def _reset_weight(self):
        if self._weights.shape[0] == 0:
            self._weights = np.array([1 for _ in range(self._n_dim)])

    def _has_same_dim(self):
        if self._weights.shape[0] != self._n_dim:
            print("dim ", self._weights.shape[0], self._n_dim)
            raise ValueError("Dim of value doesn't match that of weights.")

    def _is_positive(self):
        if np.sum(self._weights < 0) > 0:
            raise ValueError("Weight should be positive.")
