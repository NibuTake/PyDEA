from typing import Any, Dict, List, Literal

import numpy as np

from PyDEA.domain import DMUSet
from PyDEA.frontier_model._base import BaseDataEnvelopmentAnalysis
from PyDEA.solver import EnvelopeSolver


class EnvelopeDEA(BaseDataEnvelopmentAnalysis):
    """AI is creating summary for __init__

    Args:
        frontier (Literal["CRS", "VRS"]): ...
        orient (Literal["in", "out"]): ...
    """

    def __init__(self, frontier: Literal["CRS", "VRS"], orient: Literal["in", "out"]):
        self.frontier = frontier
        self.orient = orient
        self.DMUs = None
        self.result: List[Dict[str, Any]] = []

    def fit(self, inputs: np.ndarray, outputs: np.ndarray, index=np.nan):
        """AI is creating summary for fit

        Args:
            inputs (np.ndarray): [description]
            outputs (np.ndarray): [description]
            index ([type], optional): [description]. Defaults to np.nan.
        """
        # Define data.
        self.DMUs = DMUSet(inputs, outputs, index)

        # call solver.
        solver = EnvelopeSolver(self.orient, self.frontier, self.DMUs)
        self.result = solver.apply()

    @property
    def results(self) -> List[Dict[str, Any]]:
        """AI is creating summary for results

        Returns:
            List[Dict[str, Any]]: [description]
        """
        return self.result

    def _dmu(self, is_eff: bool = True):
        return [r for r in self.result if r.is_eff is is_eff]

    def _inputs(self, is_eff: bool):
        ids = [r.id for r in self._dmu(is_eff)]
        return self.DMUs.inputs[ids]

    def _outputs(self, is_eff: bool):
        ids = [r.id for r in self._dmu(is_eff)]
        return self.DMUs.outputs[ids]

    def _index(self, is_eff: bool):
        return np.vstack([r.dmu.id for r in self._dmu(is_eff)])
