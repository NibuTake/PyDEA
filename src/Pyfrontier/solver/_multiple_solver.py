import pulp

from Pyfrontier.domain import DMUSet
from Pyfrontier.solver._base import BaseSolver


class MultipleSolver(BaseSolver):
    """AI is creating summary for __init__

    Args:
        orient (str): [description]
        frontier (str): [description]
        DMUs ([type]): [description]
    """

    def __init__(self, orient: str, frontier: str, DMUs: DMUSet):
        self.orient = orient
        self.DMUs = DMUs
        self.frontier = frontier

    def apply(self) -> list:
        """AI is creating summary for fit"""
        dmu_result_list = [self._solve_problem(j) for j in range(self.DMUs.N)]
        return dmu_result_list

    def _init_problem(self) -> pulp.LpProblem:
        if self.orient == "in":
            problem = pulp.LpProblem(self.orient, pulp.LpMaximize)
        else:
            problem = pulp.LpProblem(self.orient, pulp.LpMinimize)
        return problem

    def _define_objective(self):
        if self.frontier == "VRS":
            bias = pulp.LpVariable("bias", lowBound=0)
        else:
            bias = 0
        return bias

    def _solve_problem(self, o: int) -> dict:
        # Define problem and variables.
        problem = self._init_problem()
        mu = self._dict_to_list(
            pulp.LpVariable.dicts("Mu", range(self.DMUs.s), lowBound=0)
        )
        nu = self._dict_to_list(
            pulp.LpVariable.dicts("Nu", range(self.DMUs.m), lowBound=0)
        )

        # Define objective.
        bias = self._define_objective()

        # Add restrictions.
        if self.orient == "in":
            problem += pulp.lpDot(mu, self.DMUs.outputs[o, :]) + bias

            for j in range(self.DMUs.N):
                problem += (
                    pulp.lpDot(mu, self.DMUs.outputs[j, :])
                    - pulp.lpDot(nu, self.DMUs.inputs[j, :])
                    + bias
                    <= 0
                )

            problem += pulp.lpDot(nu, self.DMUs.inputs[o, :]) == 1
        else:
            problem += pulp.lpDot(nu, self.DMUs.inputs[o, :]) + bias

            for j in range(self.DMUs.N):
                problem += (
                    pulp.lpDot(nu, self.DMUs.inputs[j, :])
                    - pulp.lpDot(mu, self.DMUs.outputs[j, :])
                    + bias
                    >= 0
                )

            problem += pulp.lpDot(mu, self.DMUs.outputs[o, :]) == 1

        # Solve and add results.
        problem.solve(pulp.PULP_CBC_CMD(msg=1, gapRel=1e-10, options=["revised"]))

        eff = self._rounder(problem.objective.value())

        weight_x = [i.value() for i in nu]
        weight_y = [r.value() for r in mu]

        output = {"eff": eff, "weight": {"x": weight_x, "y": weight_y}}

        if self.frontier == "VRS":
            output.update({"bias": bias.value()})

        return self._verify_output(o, output)

    def _verify_output(self, o: int, dmu_result: dict) -> dict:
        return dmu_result
