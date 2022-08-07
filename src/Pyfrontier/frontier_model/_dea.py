from typing import List, Literal

import numpy as np

from Pyfrontier.domain import AssuranceRegion, DMUSet, EnvelopResult, MultipleResult
from Pyfrontier.frontier_model._base import BaseDataEnvelopmentAnalysis
from Pyfrontier.solver import EnvelopeSolver, MultipleSolver


class EnvelopDEA(BaseDataEnvelopmentAnalysis):
    """AI is creating summary for __init__

    Args:
        frontier (Literal["CRS", "VRS"]): ...
        orient (Literal["in", "out"]): ...
    """

    def __init__(
        self,
        frontier: Literal["CRS", "VRS"],
        orient: Literal["in", "out"],
        super_efficiency: bool = False,
    ):
        self.frontier = frontier
        self.orient = orient
        self.super_efficiency = super_efficiency
        self.DMUs = None
        self.result: List[EnvelopResult] = []

    def fit(
        self,
        inputs: np.ndarray,
        outputs: np.ndarray,
        index=np.nan,
        uncontrollable_index: list[int] = [],
    ):
        """AI is creating summary for fit

        Args:
            inputs (np.ndarray): [description]
            outputs (np.ndarray): [description]
            index ([type], optional): [description]. Defaults to np.nan.
        """
        # Define data.
        self.DMUs = DMUSet(inputs, outputs, index)
        self._uncontrollable_index = uncontrollable_index

        # call solver.
        solver = EnvelopeSolver(
            self.orient,
            self.frontier,
            self.DMUs,
            uncontrollable_index,
            is_super_efficiency=self.super_efficiency,
        )
        self.result = solver.apply()

    @property
    def results(self) -> List[EnvelopResult]:
        """AI is creating summary for results

        Returns:
            List[Dict[str, Any]]: [description]
        """
        return self.result


class MultipleDEA(BaseDataEnvelopmentAnalysis):
    """AI is creating summary for __init__

    Args:
        frontier (Literal["CRS", "VRS"]): ...
        orient (Literal["in", "out"]): ...
    """

    def __init__(self, frontier: Literal["CRS", "VRS"], orient: Literal["in", "out"]):
        self.frontier = frontier
        self.orient = orient
        self.DMUs = None
        self.result: List[MultipleResult] = []
        self._assurance_region: List[AssuranceRegion] = []

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
        solver = MultipleSolver(
            self.orient, self.frontier, self.DMUs, self._assurance_region
        )
        self.result = solver.apply()

    @property
    def results(self) -> List[MultipleResult]:
        """AI is creating summary for results

        Returns:
            List[Dict[str, Any]]: [description]
        """
        return self.result

    def add_assurance_region(
        self,
        type: Literal["in", "out"],
        index_a: int,
        index_b: int,
        coefficient: float,
        operator: Literal["<=", ">="],
    ):
        """AI is creating summary for add_assurance_region
        - x_a/x_b =< coefficient
        - coefficient <= x_a/x_b

        Args:
            type (Literal[): [description]
            index_a (int): [description]
            index_b (int): [description]
            coefficient (float): [description]
            operator (Literal[, optional): [description]. Defaults to ", ">="].
        """
        self._assurance_region.append(
            AssuranceRegion(type, index_a, index_b, coefficient, operator)
        )

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
