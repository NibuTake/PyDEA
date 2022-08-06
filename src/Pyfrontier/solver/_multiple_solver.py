from typing import List, Union

import pulp

from Pyfrontier.domain import DMUSet, MultipleResult
from Pyfrontier.domain.dmu import DMU
from Pyfrontier.solver._base import BaseSolver


class MultipleSolver(BaseSolver):
    """AI is creating summary for __init__

    Args:
        orient (str): [description]
        frontier (str): [description]
        DMUs ([type]): [description]
    """

    def __init__(self, orient: str, frontier: str, DMUs: DMUSet, bound: float = 0.0):
        self.orient = orient
        self.DMUs = DMUs
        self.frontier = frontier
        self.bound = bound

    def apply(self) -> List[MultipleResult]:
        return [self._solve_problem(j) for j in range(self.DMUs.N)]

    def _define_bias(self) -> Union[pulp.LpVariable, int]:
        if self.frontier == "VRS":
            return pulp.LpVariable("bias")
        else:
            return 0

    def _define_input_oriented_problem(
        self, bias: Union[pulp.LpVariable, int], mu: list, nu: list, o: int
    ) -> pulp.LpProblem:
        problem = pulp.LpProblem(self.orient, pulp.LpMaximize)
        problem += pulp.lpDot(mu, self.DMUs.outputs[o, :]) + bias

        for j in range(self.DMUs.N):
            problem += (
                pulp.lpDot(mu, self.DMUs.outputs[j, :])
                - pulp.lpDot(nu, self.DMUs.inputs[j, :])
                + bias
                <= 0
            )
        problem += pulp.lpDot(nu, self.DMUs.inputs[o, :]) == 1
        return problem

    def _define_output_oriented_problem(
        self, bias: Union[pulp.LpVariable, int], mu: list, nu: list, o: int
    ) -> pulp.LpProblem:
        problem = pulp.LpProblem(self.orient, pulp.LpMinimize)
        problem += pulp.lpDot(nu, self.DMUs.inputs[o, :]) + bias

        for j in range(self.DMUs.N):
            problem += (
                pulp.lpDot(nu, self.DMUs.inputs[j, :])
                - pulp.lpDot(mu, self.DMUs.outputs[j, :])
                + bias
                >= 0
            )
        problem += pulp.lpDot(mu, self.DMUs.outputs[o, :]) == 1
        return problem

    def _solve_problem(self, o: int) -> MultipleResult:
        # Define variables.
        mu = self._dict_to_list(
            pulp.LpVariable.dicts("Mu", range(self.DMUs.s), lowBound=self.bound)
        )
        nu = self._dict_to_list(
            pulp.LpVariable.dicts("Nu", range(self.DMUs.m), lowBound=self.bound)
        )
        bias = self._define_bias()

        # Problem.
        if self.orient == "in":
            problem = self._define_input_oriented_problem(bias, mu, nu, o)
        else:
            problem = self._define_output_oriented_problem(bias, mu, nu, o)
        problem.solve(pulp.PULP_CBC_CMD(msg=1, gapRel=1e-10, options=["revised"]))

        return MultipleResult(
            score=self._rounder(problem.objective.value()),
            id=o,
            dmu=DMU(self.DMUs.inputs[o], self.DMUs.outputs[o], self.DMUs.get_id(o)),
            x_weight=[self._rounder(i.value()) for i in nu],
            y_weight=[self._rounder(r.value()) for r in mu],
            bias=self._derive_value_from_bias(bias),
        )

    def _derive_value_from_bias(self, bias: Union[pulp.LpVariable, int]) -> float:
        if isinstance(bias, int):
            return 0.0
        else:
            return self._rounder(bias.value())
