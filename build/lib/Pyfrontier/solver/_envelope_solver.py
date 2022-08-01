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

    def _init_problem(self) -> pulp.LpProblem:
        if self.orient == "in":
            problem = pulp.LpProblem(self.orient, pulp.LpMinimize)
        else:
            problem = pulp.LpProblem(self.orient, pulp.LpMaximize)
        return problem

    def _input_orient_coef(self, i: int) -> tuple:
        theta = pulp.LpVariable("theta", lowBound=0)
        in_coef = theta
        out_coef = 1

        if i in self._uncontrollable_index:
            in_coef = 1
        return (in_coef, out_coef)

    def _output_orient_coef(self, i: int) -> tuple:
        theta = pulp.LpVariable("theta", lowBound=0)
        in_coef = 1
        out_coef = theta

        if i in self._uncontrollable_index:
            out_coef = 1
        return (in_coef, out_coef)

    def _solve_problem(self, o: int) -> dict:
        """[summary]

        Args:
            o (int): Index of a target DMU_o
        """
        # Define problem and variables.
        problem = self._init_problem()
        lambda_N = self._dict_to_list(
            pulp.LpVariable.dicts(
                "Lambda", range(self.DMUs.N), lowBound=0, cat="Continuous"
            )
        )
        theta = pulp.LpVariable("theta", lowBound=0)

        # Define objective.
        problem += theta

        if self.orient == "in":
            in_coef = theta
            out_coef = 1
        else:
            in_coef = 1
            out_coef = theta

        # X
        for i in range(self.DMUs.m):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.inputs[:, i])
                <= in_coef * self.DMUs.inputs[o, i]
            )

        # Y
        for i in range(self.DMUs.s):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.outputs[:, i])
                >= out_coef * self.DMUs.outputs[o, i]
            )

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
        slack_solver = SlackSolver(self.orient, self.DMUs)
        res = slack_solver.apply(o, dmu_result)
        result = Result(**res)
        result._set_dmu(self.DMUs.inputs[o], self.DMUs.outputs[o], self.DMUs.get_id(o))
        return result


class SlackSolver(BaseSolver):
    def __init__(self, orient: str, DMUs: DMUSet):
        self.orient = orient
        self.DMUs = DMUs
        self.u_c_index = 100

    def apply(self, o: int, dmu_result: dict) -> dict:
        if dmu_result["eff"] == 1:
            dmu_result["is_eff"] = True
            slack_result = self._solve_problem(o, dmu_result["eff"])
            dmu_result = self._add_slack_result_to_dea_result(dmu_result, slack_result)
        else:
            dmu_result["is_eff"] = False
        return dmu_result

    def _init_problem(self):
        problem = pulp.LpProblem(self.orient, pulp.LpMaximize)
        return problem

    def _solve_problem(self, o: int, theta: float):
        problem = self._init_problem()

        # Define problem and variables.
        sx = self._dict_to_list(
            pulp.LpVariable.dicts("sx", range(self.DMUs.m), lowBound=0)
        )
        sy = self._dict_to_list(
            pulp.LpVariable.dicts("sy", range(self.DMUs.s), lowBound=0)
        )
        lambda_N = self._dict_to_list(
            pulp.LpVariable.dicts("Lambda", range(self.DMUs.N), lowBound=0)
        )
        problem += np.sum(sx) + np.sum(sy)

        # Add restrictions.
        if self.orient == "in":
            in_coef = theta
            out_coef = 1
        else:
            in_coef = 1
            out_coef = theta

        for i in range(self.DMUs.m):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.inputs[:, i]) + sx[i]
                == in_coef * self.DMUs.inputs[o, i]
            )

        for r in range(self.DMUs.s):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.outputs[:, r]) - sy[r]
                == out_coef * self.DMUs.outputs[o, r]
            )
        problem += np.sum(lambda_N) == 1

        # Solve and add results.
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
