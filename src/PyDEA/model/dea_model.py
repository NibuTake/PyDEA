import numpy as np

from .dmu import DMU, DMUSet
from .metric import Attractiveness, Degree, Level, Progress
from .solver import AttractivenessSolver, EnvelopeSolver


class EnvelopeDEA:
    def __init__(self, frontier: str, orient: str):
        self.frontier = frontier
        self.orient = orient
        self.DMUs = None
        self.result = None

    def fit(self, inputs, outputs, index=np.nan):
        # Define data.
        self.DMUs = DMUSet(inputs, outputs, index)

        # call solver.
        solver = EnvelopeSolver(self.orient, self.frontier, self.DMUs)
        self.result = solver.apply()

    def dmu(self, is_eff: bool = True):
        return [r for r in self.result if r.is_eff is is_eff]

    def _inputs(self, is_eff: bool):
        ids = [r.id for r in self.dmu(is_eff)]
        return self.DMUs.inputs[ids]

    def _outputs(self, is_eff: bool):
        ids = [r.id for r in self.dmu(is_eff)]
        return self.DMUs.outputs[ids]

    def _index(self, is_eff: bool):
        return np.vstack([r.dmu.id for r in self.dmu(is_eff)])


class HierarchicalDEA:
    def __init__(self, frontier: str, orient: str):
        self.frontier = frontier
        self.orient = orient
        self.DMUs = None
        self.result = []

    def fit(self, inputs, outputs, index=np.nan):
        while True:
            dea = EnvelopeDEA(self.frontier, self.orient)
            dea.fit(inputs, outputs, index)
            self.result.append(dea.dmu(True))

            if len(dea.dmu(False)) == 0:
                break
            else:
                inputs = dea._inputs(False)
                outputs = dea._outputs(False)
                index = dea._index(False)

    def layer_dmus(self, level: int):
        layer_dmus = self.result[Level(level).var]
        inputs = np.vstack([r.dmu.input for r in layer_dmus])
        outputs = np.vstack([r.dmu.output for r in layer_dmus])
        index = np.vstack([r.dmu.id for r in layer_dmus])
        return DMUSet(inputs, outputs, index)

    def attractiveness(self, dmu: DMU, level: int, d: int):
        var = Attractiveness(self._calc_metric(dmu, level, d)).var
        if self.orient == "in":
            return var
        else:
            return 1 / var

    def progress(self, dmu: DMU, level: int, d: int):
        var = Progress(self._calc_metric(dmu, level, d)).var
        if self.orient == "in":
            return 1 / var
        else:
            return var

    def _calc_metric(self, dmu: DMU, level: int, d: int):
        order = Level(level).var + Degree(d).var
        DMUs = self.layer_dmus(order)

        attr_solver = AttractivenessSolver(self.orient, self.frontier, DMUs)
        res = attr_solver.apply(dmu)
        return res.eff
