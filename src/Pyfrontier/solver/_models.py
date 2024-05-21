from dataclasses import dataclass
from typing import Literal, Union

import pulp


@dataclass
class Bias:
    frontier: Literal["CRS", "VRS", "IRS", "DRS"]
    orient: Literal["in", "out"]

    @property
    def value(self) -> Union[pulp.LpVariable, int]:
        if self.frontier == "VRS":
            return pulp.LpVariable("bias")
        elif self.frontier == "IRS":
            return (
                pulp.LpVariable("bias", lowBound=0)
                if self.orient == "in"
                else pulp.LpVariable("bias", upBound=0)
            )
        elif self.frontier == "DRS":
            return (
                pulp.LpVariable("bias", upBound=0)
                if self.orient == "in"
                else pulp.LpVariable("bias", lowBound=0)
            )
        else:
            return 0
