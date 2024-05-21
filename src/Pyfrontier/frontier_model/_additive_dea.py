from typing import List, Literal, Optional

import numpy as np

from Pyfrontier.domain import AdditiveResult, DMUSet
from Pyfrontier.domain.parallel import NumberOfJobs
from Pyfrontier.frontier_model._base import BaseDataEnvelopmentAnalysis
from Pyfrontier.solver import AdditiveSolver


class AdditiveDEA(BaseDataEnvelopmentAnalysis):
    """This is a envelop dea model.

    Args:
        frontier (Literal["CRS", "VRS", "IRS", "DRS"]): CRS means constant returns to scale. VRS means variable returns to scale. IRS means increasing returns to scale. DRS means decreasing returns to scale.
        n_jobs (int, optional): The number of parallel jobs to solve DMU programming.
    """

    def __init__(self, frontier: Literal["CRS", "VRS", "IRS", "DRS"], n_jobs: int = 1):
        self.frontier = frontier
        self.DMUs: Optional[DMUSet] = None
        self._result: List[AdditiveResult] = []
        self.n_jobs = NumberOfJobs(n_jobs).value

    def fit(
        self,
        inputs: np.ndarray,
        outputs: np.ndarray,
        x_weight: np.ndarray = np.array([]),
        y_weight: np.ndarray = np.array([]),
        index: np.ndarray = np.nan,
    ):
        """Fit additive model.

        Args:
            inputs (np.ndarray): Inputs of DMUs.
            outputs (np.ndarray): Outputs of DMUs.
            x_weight (np.ndarray, optional): [description]. Defaults to np.array([]).
            y_weight (np.ndarray, optional): [description]. Defaults to np.array([]).
            index (np.ndarray, optional): This is ID to identify the DMU. The default is generated as a sequential number.
        """
        self.DMUs = DMUSet(inputs, outputs, index)
        solver = AdditiveSolver(
            self.frontier, self.DMUs, x_weight, y_weight, n_jobs=self.n_jobs
        )
        self._result = solver.apply()

    @property
    def result(self) -> List[AdditiveResult]:
        """The return value is a list of objects.

        Returns:
            List[AdditiveResult]: [description]
        """
        return self._result
