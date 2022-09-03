from typing import List, Literal, Optional

import numpy as np
import pulp

from Pyfrontier.domain import DMU, AdditiveResult, DMUSet, SlackWeight
from Pyfrontier.solver._base import BaseSolver


class AdditiveSolver(BaseSolver):
    def __init__(
        self,
        frontier: Optional[Literal["CRS", "VRS"]],
        DMUs: DMUSet,
        x_weight: np.ndarray,
        y_weight: np.ndarray,
    ) -> None:
        self.x_weight = x_weight
        self.y_weight = y_weight
        self.frontier = frontier
        self.DMUs = DMUs

    def apply(self) -> List[AdditiveResult]:
        return [self._solve_problem(j) for j in range(self.DMUs.N)]

    def _define_problem(
        self, o: int, lambda_N: list, sx: list, sy: list
    ) -> pulp.LpProblem:
        x_weight = SlackWeight(self.x_weight, self.DMUs.m)
        y_weight = SlackWeight(self.y_weight, self.DMUs.s)

        problem = pulp.LpProblem("additive", pulp.LpMaximize)
        problem += np.sum(np.array(sx) * x_weight.value) + np.sum(
            np.array(sy) * y_weight.value
        )

        # X
        for i in range(self.DMUs.m):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.inputs[:, i]) + sx[i]
                <= self.DMUs.inputs[o, i]
            )

        # Y
        for r in range(self.DMUs.s):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.outputs[:, r]) - sy[r]
                >= self.DMUs.outputs[o, r]
            )

        if self.frontier == "VRS":
            problem += np.sum(lambda_N) == 1

        return problem

    def _solve_problem(self, o: int) -> AdditiveResult:
        # Define variables.
        sx = self._dict_to_list(
            pulp.LpVariable.dicts(
                "sx", range(self.DMUs.m), lowBound=0, cat="Continuous"
            )
        )
        sy = self._dict_to_list(
            pulp.LpVariable.dicts(
                "sy", range(self.DMUs.s), lowBound=0, cat="Continuous"
            )
        )
        lambda_N = self._dict_to_list(
            pulp.LpVariable.dicts(
                "Lambda", range(self.DMUs.N), lowBound=0, cat="Continuous"
            )
        )
        problem = self._define_problem(o, lambda_N, sx, sy)
        problem.solve(pulp.PULP_CBC_CMD(msg=1, gapRel=1e-10, options=["revised"]))

        return AdditiveResult(
            score=np.nan,
            id=o,
            dmu=DMU(self.DMUs.inputs[o], self.DMUs.outputs[o], self.DMUs.get_id(o)),
            x_slack=[self._rounder(i.value()) for i in sx],
            y_slack=[self._rounder(r.value()) for r in sy],
        )
