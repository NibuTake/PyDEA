from typing import List, Literal, Tuple, Union

import numpy as np
import pulp


from Pyfrontier.domain import DMU, DMUSet, EnvelopResult, FrontierType
from Pyfrontier.domain import MultiProcessor
from Pyfrontier.solver._base import BaseSolver


class EnvelopeSolver(BaseSolver):
    """AI is creating summary for __init__

    Args:
        orient (str): [description]
        frontier (str): [description]
        DMUs ([type]): [description]
    """

    def __init__(
        self,
        orient: Literal["in", "out"],
        frontier: FrontierType,
        DMUs: DMUSet,
        uncontrollable_index: List[int] = [],
        is_super_efficiency: bool = False,
        n_jobs: int = 1,
    ):
        self.orient = orient
        self.DMUs = DMUs
        self.frontier = frontier
        self._uncontrollable_index = uncontrollable_index
        self._is_super_efficiency = is_super_efficiency
        self.n_jobs = n_jobs

    def apply(self) -> List[EnvelopResult]:
        processor = MultiProcessor(self._solve_problem, self.DMUs.N)
        return processor.solve(self.n_jobs)

    def _redefine_theta_i(
        self, i: int, theta: pulp.LpVariable
    ) -> Union[int, pulp.LpVariable]:
        if i in self._uncontrollable_index:
            return 1
        else:
            return theta

    def _index_of_dmu(self, o: int) -> List[int]:
        if self._is_super_efficiency:
            return [i for i in range(self.DMUs.N) if i != o]
        else:
            return [i for i in range(self.DMUs.N)]

    def _define_input_orient_problem(
        self, o: int, lambda_N: list, theta: pulp.LpVariable
    ) -> pulp.LpProblem:
        problem = pulp.LpProblem(
            self.orient + str(o), pulp.LpMinimize
        )  # avoid repeated name
        problem += theta

        # X
        for i in range(self.DMUs.m):
            theta_i = self._redefine_theta_i(i, theta)
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.inputs[self._index_of_dmu(o), i])
                <= theta_i * self.DMUs.inputs[o, i]
            )

        # Y
        for i in range(self.DMUs.s):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.outputs[self._index_of_dmu(o), i])
                >= 1 * self.DMUs.outputs[o, i]
            )
        return problem

    def _define_output_orient_problem(
        self, o: int, lambda_N: list, theta: pulp.LpVariable
    ) -> pulp.LpProblem:
        problem = pulp.LpProblem(
            self.orient + str(o), pulp.LpMaximize
        )  # avoid repeated name
        problem += theta

        # X
        for i in range(self.DMUs.m):

            problem += (
                pulp.lpDot(lambda_N, self.DMUs.inputs[self._index_of_dmu(o), i])
                <= 1 * self.DMUs.inputs[o, i]
            )
        # Y
        for i in range(self.DMUs.s):
            theta_i = self._redefine_theta_i(i, theta)
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.outputs[self._index_of_dmu(o), i])
                >= theta_i * self.DMUs.outputs[o, i]
            )

        return problem

    def _solve_problem(self, o: int) -> EnvelopResult:
        # Define variables.
        theta = pulp.LpVariable("theta", lowBound=0)
        lambda_N = self._dict_to_list(
            pulp.LpVariable.dicts(
                "Lambda", self._index_of_dmu(o), lowBound=0, cat="Continuous"
            )
        )

        # Define problem.
        if self.orient == "in":
            problem = self._define_input_orient_problem(o, lambda_N, theta)
        else:
            problem = self._define_output_orient_problem(o, lambda_N, theta)

        if self.frontier == "VRS":
            problem += np.sum(lambda_N) == 1
        elif self.frontier == "NDRS":
            problem += np.sum(lambda_N) >= 1
        elif self.frontier == "NIRS":
            problem += np.sum(lambda_N) <= 1

        # Use high-precision solver parameters for better numerical accuracy
        # gapRel: relative gap tolerance for optimality
        # ratioGap: primal-dual gap ratio (1e-12 for very high precision)
        problem.solve(
            pulp.PULP_CBC_CMD(msg=0, gapRel=1e-12, options=["ratio 1e-12"])
        )

        score = self._rounder(problem.objective.value())
        sx, sy = self._optimize_slack(score, o)

        return EnvelopResult(
            score=self._rounder(problem.objective.value()),
            weights=[self._rounder(n.value()) for n in lambda_N],
            id=o,
            x_slack=sx,
            y_slack=sy,
            dmu=DMU(self.DMUs.inputs[o], self.DMUs.outputs[o], self.DMUs.get_id(o)),
            orientation=self.orient,
        )

    def _optimize_slack(self, theta: float, o: int) -> Tuple[list, list]:
        if self._is_super_efficiency:
            return ([], [])
        else:
            slack_solver = SlackSolver(
                self.orient, self.frontier, self.DMUs, self._uncontrollable_index
            )
        return slack_solver.apply(o, theta)


class SlackSolver(BaseSolver):
    def __init__(
        self,
        orient: str,
        frontier: FrontierType,
        DMUs: DMUSet,
        uncontrollable_index: list,
    ):
        self.orient = orient
        self.frontier = frontier
        self.DMUs = DMUs
        self._uncontrollable_index = uncontrollable_index

    def apply(self, o: int, theta: float) -> Tuple[list, list]:
        slack_result = self._solve_problem(o, theta)
        return slack_result["sx"], slack_result["sy"]

    def _redefine_theta(self, i: int, theta) -> tuple:
        if i in self._uncontrollable_index:
            return 1
        else:
            return theta

    def _define_input_orient_problem(
        self, o: int, sx: list, sy: list, lambda_N: list, theta: float
    ) -> pulp.LpProblem:
        problem = pulp.LpProblem(self.orient, pulp.LpMaximize)
        problem += np.sum(sx) + np.sum(sy)

        for i in range(self.DMUs.m):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.inputs[:, i]) + sx[i]
                == self._redefine_theta(1, theta) * self.DMUs.inputs[o, i]
            )

        for r in range(self.DMUs.s):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.outputs[:, r]) - sy[r]
                == 1 * self.DMUs.outputs[o, r]
            )

        return problem

    def _define_output_orient_problem(
        self, o: int, sx: list, sy: list, lambda_N: list, theta: float
    ) -> pulp.LpProblem:
        problem = pulp.LpProblem(self.orient, pulp.LpMaximize)
        problem += np.sum(sx) + np.sum(sy)

        for i in range(self.DMUs.m):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.inputs[:, i]) + sx[i]
                == 1 * self.DMUs.inputs[o, i]
            )

        for r in range(self.DMUs.s):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.outputs[:, r]) - sy[r]
                == self._redefine_theta(1, theta) * self.DMUs.outputs[o, r]
            )

        return problem

    def _solve_problem(self, o: int, theta: float) -> dict:
        # Define variables.
        sx = self._dict_to_list(
            pulp.LpVariable.dicts("sx", range(self.DMUs.m), lowBound=0)
        )
        sy = self._dict_to_list(
            pulp.LpVariable.dicts("sy", range(self.DMUs.s), lowBound=0)
        )
        lambda_N = self._dict_to_list(
            pulp.LpVariable.dicts("Lambda", range(self.DMUs.N), lowBound=0)
        )

        # Define problem.
        if self.orient == "in":
            problem = self._define_input_orient_problem(o, sx, sy, lambda_N, theta)
        else:
            problem = self._define_output_orient_problem(o, sx, sy, lambda_N, theta)

        # Apply frontier constraint (same as EnvelopeSolver)
        if self.frontier == "VRS":
            problem += np.sum(lambda_N) == 1
        elif self.frontier == "NDRS":
            problem += np.sum(lambda_N) >= 1
        elif self.frontier == "NIRS":
            problem += np.sum(lambda_N) <= 1
        # CRS: No constraint on sum(lambda)

        # Use high-precision solver parameters for better numerical accuracy
        # gapRel: relative gap tolerance for optimality
        # ratio: primal-dual gap ratio (1e-12 for very high precision)
        # revised: use revised simplex method for better numerical stability
        problem.solve(
            pulp.PULP_CBC_CMD(msg=0, gapRel=1e-12, options=["revised", "ratio 1e-12"])
        )

        return {"sx": [i.value() for i in sx], "sy": [r.value() for r in sy]}
