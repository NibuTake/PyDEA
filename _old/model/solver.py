import numpy as np
import pulp

from .dmu import DMU, DMUSet, Result


class EnvelopeSolver:
    def __init__(self, orient: str, frontier: str, DMUs: DMUSet):
        self.orient = orient
        self.DMUs = DMUs
        self.frontier = frontier
        self.u_c_index = 100

    def apply(self):
        # Define problems for all DMUs.
        dmu_result_list = [self._solve_problem(j) for j in range(self.DMUs.N)]

        return dmu_result_list

    # Envelope (in => min, out => max)
    def _init_problem(self):
        if self.orient == "in":
            problem = pulp.LpProblem(self.orient, pulp.LpMinimize)
        else:
            problem = pulp.LpProblem(self.orient, pulp.LpMaximize)
        return problem

    def _solve_problem(self, o: int):
        """[summary]

        Args:
            o (int): Index of a target DMU_o
        """
        # Define problem and variables.
        problem = self._init_problem()
        lambda_N = _dict_to_list(
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

        # Add restrictions.
        for i in range(self.DMUs.m):
            # Process uncontrollable variables.
            # if i == self.u_c_index:
            #     in_coef = 1
            # else:
            #     in_coef = theta
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.inputs[:, i])
                <= in_coef * self.DMUs.inputs[o, i]
            )

        for i in range(self.DMUs.s):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.outputs[:, i])
                >= out_coef * self.DMUs.outputs[o, i]
            )

        if self.frontier == "VRS":
            problem += np.sum(lambda_N) == 1

        # Solve problem.
        problem.solve()
        eff = _rounder(problem.objective.value())
        lambda_list = [_rounder(n.value()) for n in lambda_N]
        output = {"eff": eff, "lambdas": lambda_list, "id": o}

        res = self._verify_output(o, output)
        return res

    def _verify_output(self, o: int, dmu_result: dict) -> Result:
        slack_solver = SlackSolver(self.orient, self.DMUs)
        res = slack_solver.apply(o, dmu_result)
        result = Result(**res)
        result._set_dmu(self.DMUs.inputs[o], self.DMUs.outputs[o], self.DMUs.get_id(o))
        return result


class SlackSolver:
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
        sx = _dict_to_list(pulp.LpVariable.dicts("sx", range(self.DMUs.m), lowBound=0))
        sy = _dict_to_list(pulp.LpVariable.dicts("sy", range(self.DMUs.s), lowBound=0))
        lambda_N = _dict_to_list(
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


class AttractivenessSolver:
    def __init__(self, orient: str, frontier: str, DMUs: DMUSet):
        self.orient = orient
        self.DMUs = DMUs
        self.frontier = frontier
        self.u_c_index = 100

    def apply(self, target_dmu: DMU):
        return self._solve_problem(target_dmu)

    # Envelope (in => min, out => max)
    def _init_problem(self):
        if self.orient == "in":
            problem = pulp.LpProblem(self.orient, pulp.LpMinimize)
        else:
            problem = pulp.LpProblem(self.orient, pulp.LpMaximize)
        # NOTE: Minimum
        # problem = pulp.LpProblem(self.orient, pulp.LpMinimize)
        return problem

    def _solve_problem(self, target_dmu: DMU):
        """[summary]

        Args:
            o (int): Index of a target DMU_o
        """
        # Define problem and variables.
        problem = self._init_problem()
        lambda_N = _dict_to_list(
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

        # Add restrictions.
        for i in range(self.DMUs.m):
            # Process uncontrollable variables.
            # if i == self.u_c_index:
            #     in_coef = 1
            # else:
            #     in_coef = theta
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.inputs[:, i])
                <= in_coef * target_dmu.input[i]
            )

        for i in range(self.DMUs.s):
            problem += (
                pulp.lpDot(lambda_N, self.DMUs.outputs[:, i])
                >= out_coef * target_dmu.output[i]
            )

        if self.frontier == "VRS":
            problem += np.sum(lambda_N) == 1

        # Solve problem.
        problem.solve()
        eff = _rounder(problem.objective.value())
        lambda_list = [_rounder(n.value()) for n in lambda_N]
        output = {"eff": eff, "lambdas": lambda_list, "id": 0}

        return self._verify_output(0, output)

    def _verify_output(self, o: int, dmu_result: dict) -> Result:
        result = Result(**dmu_result)
        result._set_dmu(self.DMUs.inputs[o], self.DMUs.outputs[o], self.DMUs.index[o])
        return result


# TODO:
# 1. _verify_output
# 2. 分岐関数まとめ
# 3. ファイル構成見直し
# 共通関数作成
# 4. 動作検証
# 5. multiple


def _dict_to_list(_dict):
    return [_dict[k] for k in _dict]


def _rounder(v):
    sign_figs = 8
    return round(v, sign_figs)
