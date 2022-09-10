from typing import List, Literal

import numpy as np

from Pyfrontier.domain import AssuranceRegion, DMUSet, EnvelopResult, MultipleResult
from Pyfrontier.frontier_model._base import BaseDataEnvelopmentAnalysis
from Pyfrontier.solver import EnvelopeSolver, MultipleSolver


class EnvelopDEA(BaseDataEnvelopmentAnalysis):
    """This is a envelop dea model.

    Args:
        frontier (Literal["CRS", "VRS"]): CRS means constant returns to scale. VRS means variable returns to scale.
        orient (Literal["in", "out"]): Input or output oriented model.
        super_efficiency (bool, optional): Whether to use super-efficiency. Defaults to False.
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
        index: np.ndarray = np.nan,
        uncontrollable_index: List[int] = [],
    ):
        """Fit envelop model.

        Args:
            inputs (np.ndarray): Inputs of DMUs.
            outputs (np.ndarray): Outputs of DMUs.
            index (np.ndarray, optional): This is ID to identify the DMU. The default is generated as a sequential number.
            uncontrollable_index (List[int], optional): Specifies the index of the variable that will not be improved in DEA. In the case of input-oriented, this means how many columns of input or output are used in the case of output-oriented.
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
        """The return value is a list of objects.

        Returns:
            List[EnvelopResult]: [description]
        """
        return self.result


class MultipleDEA(BaseDataEnvelopmentAnalysis):
    """This is a multiplier dea model.

    Args:
        frontier (Literal["CRS", "VRS"]): CRS means constant returns to scale. VRS means variable returns to scale.
        orient (Literal["in", "out"]): Input or output oriented model.
    """

    def __init__(self, frontier: Literal["CRS", "VRS"], orient: Literal["in", "out"]):
        self.frontier = frontier
        self.orient = orient
        self.DMUs = None
        self.result: List[MultipleResult] = []
        self._assurance_region: List[AssuranceRegion] = []

    def fit(self, inputs: np.ndarray, outputs: np.ndarray, index: np.ndarray = np.nan):
        """Fit multiplier model.

        Args:
            inputs (np.ndarray): Input of DMUs.
            outputs (np.ndarray): Output of DMUs.
            index (np.ndarray, optional): This is ID to identify the DMU. The default is generated as a sequential number.
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
        """The return value is a list of objects.

        Returns:
            List[MultipleResult]: []
        """
        return self.result

    @property
    def cross_efficiency(self) -> List[float]:
        """This kind of efficiency can rank DMUs with peer evaluation instead of a self-evaluation.

        Returns:
            List[float]: Each values are always less than 1
        """
        matrix = self._cross_efficiency_matrix()
        return [self._get_cross_efficiency(i, matrix) for i in range(self.DMUs.N)]

    def _cross_efficiency_matrix(self) -> np.ndarray:
        cross_matrix_list = []
        for r in self.result:
            x_weights = np.vstack([r.x_weight for r in self.result])
            y_weights = np.vstack([r.y_weight for r in self.result])
            input = (r.dmu.input * x_weights).sum(axis=1)
            output = (r.dmu.output * y_weights).sum(axis=1)
            cross_matrix_list.append(output / input)

        return np.vstack(cross_matrix_list)

    def _get_cross_efficiency(self, i: int, cross_matrix: np.ndarray) -> float:
        return np.delete(cross_matrix[i], i).mean()

    def add_assurance_region(
        self,
        type: Literal["in", "out"],
        index_a: int,
        index_b: int,
        coefficient: float,
        operator: Literal["<=", ">="],
    ):
        """Add additional constrains in the form of ratio multiplier bound.
        - x_a/x_b =< coefficient
        - coefficient <= x_a/x_b

        Args:
            type (Literal["in", "out"]): This indicates whether constraints are imposed on inputs or outputs; it is not related to orient.
            index_a (int): [description]
            index_b (int): [description]
            coefficient (float): [description]
            operator (Literal["<=", ">="], optional): [description]
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
