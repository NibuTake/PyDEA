from typing import Union

import numpy as np
import pulp

from Pyfrontier.domain import DMUSet, Result
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
        orient: str,
        frontier: str,
        DMUs: DMUSet,
        uncontrollable_index: list[int] = [],
    ):
        self.orient = orient
        self.DMUs = DMUs
        self.frontier = frontier
        self._uncontrollable_index = uncontrollable_index

    def apply(self) -> list:
        """AI is creating summary for fit"""
        dmu_result_list = [self._solve_problem(j) for j in range(self.DMUs.N)]
        return dmu_result_list

    def _redefine_theta_i(
        self, i: int, theta: pulp.LpVariable
    ) -> Union[int, pulp.LpVariable]:
        if i in self._uncontrollable_index:
            return 1
        else:
            return theta

    def _define_input_orient_problem(
        self,
        o: int,
        lambda_N: list,
        theta: pulp.LpVariable,
    ) -> pulp.LpProblem:
        problem = pulp.LpProblem(self.orient, pulp.LpMinimize)
        problem += theta

        # X
        for i in range(self.DMUs.m):
            theta_i = self._redefine_theta_i(i, theta)
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.inputs[:, i])
                <= theta_i * self.DMUs.inputs[o, i]
            )

        # Y
        for i in range(self.DMUs.s):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.outputs[:, i])
                >= 1 * self.DMUs.outputs[o, i]
            )
        return problem

    def _define_output_orient_problem(
        self,
        o: int,
        lambda_N: list,
        theta: pulp.LpVariable,
    ) -> pulp.LpProblem:
        problem = pulp.LpProblem(self.orient, pulp.LpMaximize)
        problem += theta

        # X
        for i in range(self.DMUs.m):

            problem += (
                pulp.lpDot(lambda_N, self.DMUs.inputs[:, i])
                <= 1 * self.DMUs.inputs[o, i]
            )

        # Y
        for i in range(self.DMUs.s):
            theta_i = self._redefine_theta_i(i, theta)
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.outputs[:, i])
                >= theta_i * self.DMUs.outputs[o, i]
            )

        return problem

    def _solve_problem(self, o: int):
        # Define variables.
        theta = pulp.LpVariable("theta", lowBound=0)
        lambda_N = self._dict_to_list(
            pulp.LpVariable.dicts(
                "Lambda", range(self.DMUs.N), lowBound=0, cat="Continuous"
            )
        )

        # Define problem.
        if self.orient == "in":
            problem = self._define_input_orient_problem(o, lambda_N, theta)
        else:
            problem = self._define_output_orient_problem(o, lambda_N, theta)

        # Add restriction.
        if self.frontier == "VRS":
            problem += np.sum(lambda_N) == 1

        # Solve problem.
        problem.solve()
        eff = self._rounder(problem.objective.value())
        lambda_list = [self._rounder(n.value()) for n in lambda_N]
        output = {"eff": eff, "lambdas": lambda_list, "id": o}

        res = self._verify_output(o, output)
        return res

    def _verify_output(self, o: int, dmu_result: dict) -> Result:
        slack_solver = SlackSolver(self.orient, self.DMUs, self._uncontrollable_index)
        res = slack_solver.apply(o, dmu_result)
        result = Result(**res)
        result._set_dmu(self.DMUs.inputs[o], self.DMUs.outputs[o], self.DMUs.get_id(o))
        return result


class SlackSolver(BaseSolver):
    def __init__(self, orient: str, DMUs: DMUSet, uncontrollable_index: list):
        self.orient = orient
        self.DMUs = DMUs
        self._uncontrollable_index = uncontrollable_index

    def apply(self, o: int, dmu_result: dict) -> dict:
        if dmu_result["eff"] == 1:
            dmu_result["is_eff"] = True
            slack_result = self._solve_problem(o, dmu_result["eff"])
            dmu_result = self._add_slack_result_to_dea_result(dmu_result, slack_result)
        else:
            dmu_result["is_eff"] = False
        return dmu_result

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

    def _solve_problem(self, o: int, theta: float):
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

        # Add restrictions.
        problem += np.sum(lambda_N) == 1

        # Solve.
        problem.solve(pulp.PULP_CBC_CMD(msg=1, gapRel=1e-10, options=["revised"]))

        return {"sx": [i.value() for i in sx], "sy": [r.value() for r in sy]}

    def _add_slack_result_to_dea_result(self, dea_result: dict, slack_result: dict):
        result = dea_result.copy()
        result.update(slack_result)

        if np.sum(result["sx"]) + np.sum(result["sy"]) > 0:
            result.update({"is_slack": True})
            result.update({"is_eff": False})
        else:
            result.update({"is_slack": False})

        return result
