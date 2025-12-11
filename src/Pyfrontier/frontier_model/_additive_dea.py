from typing import List, Optional

import numpy as np

from Pyfrontier.domain import AdditiveResult, DMUSet, Frontier, FrontierType
from Pyfrontier.domain.parallel import NumberOfJobs
from Pyfrontier.frontier_model._base import BaseDataEnvelopmentAnalysis
from Pyfrontier.solver import AdditiveSolver


class AdditiveDEA(BaseDataEnvelopmentAnalysis):
    """This is a envelop dea model.

    Args:
        frontier (FrontierType):
            - CRS: Constant Returns to Scale
            - VRS: Variable Returns to Scale
            - NDRS: Non-Decreasing Returns to Scale
            - NIRS: Non-Increasing Returns to Scale
        n_jobs (int, optional): The number of parallel jobs to solve DMU programming.
    """

    def __init__(self, frontier: FrontierType, n_jobs: int = 1):
        self.frontier = Frontier(frontier).value
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
        labels: Optional[np.ndarray] = None,
    ):
        """Fit additive model.

        Args:
            inputs (np.ndarray): Inputs of DMUs.
            outputs (np.ndarray): Outputs of DMUs.
            x_weight (np.ndarray, optional): [description]. Defaults to np.array([]).
            y_weight (np.ndarray, optional): [description]. Defaults to np.array([]).
            index (np.ndarray, optional): This is ID to identify the DMU. The default is generated as a sequential number.
            labels (np.ndarray, optional): String labels for DMUs. Defaults to None.
        """
        self.DMUs = DMUSet(inputs, outputs, index, labels=labels)
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
