import abc

import numpy as np


class BaseDataEnvelopmentAnalysis(abc.ABC):
    def __init__(self) -> None:
        pass

    def _get_dmu(self, score: int = 1):
        if score == 1:
            return [r for r in self.result if r.score == 1]
        else:
            return [r for r in self.result if r.score != 1]

    def _get_inputs(self, score: int):
        ids = [r.id for r in self._get_dmu(score)]
        return self.DMUs.inputs[ids]

    def _get_outputs(self, score: int):
        ids = [r.id for r in self._get_dmu(score)]
        return self.DMUs.outputs[ids]

    def _get_index(self, score: int):
        return np.vstack([r.dmu.id for r in self._get_dmu(score)])
