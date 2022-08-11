from typing import List, Literal, Optional

import numpy as np

from Pyfrontier.domain import AdditiveResult, DMUSet
from Pyfrontier.frontier_model._base import BaseDataEnvelopmentAnalysis
from Pyfrontier.solver import AdditiveSolver


class AdditiveDEA(BaseDataEnvelopmentAnalysis):
    def __init__(self, frontier: Literal["CRS", "VRS"]):
        self.frontier = frontier
        self.DMUs: Optional[DMUSet] = None
        self._result: List[AdditiveResult] = []

    def fit(
        self,
        inputs: np.ndarray,
        outputs: np.ndarray,
        x_weight: np.ndarray = np.array([]),
        y_weight: np.ndarray = np.array([]),
        index=np.nan,
    ):
        self.DMUs = DMUSet(inputs, outputs, index)
        solver = AdditiveSolver(self.frontier, self.DMUs, x_weight, y_weight)
        self._result = solver.apply()

    @property
    def result(self) -> List[AdditiveResult]:
        """AI is creating summary for result

        Returns:
            List[AdditiveResult]: [description]
        """
        return self._result
