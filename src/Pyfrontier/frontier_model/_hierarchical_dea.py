from typing import List

import numpy as np

from Pyfrontier.domain.result import BaseResult
from Pyfrontier.frontier_model import EnvelopDEA


class HierarchalDEA:
    def __init__(self, dea_model: EnvelopDEA):
        self.dea = dea_model
        self.result: List[List[BaseResult]] = []

    def fit(self, inputs: np.ndarray, outputs: np.ndarray, index=np.nan):
        while True:
            self.dea.fit(inputs, outputs, index)
            self.result.append([r for r in self.dea.result if r.score == 1])

            if len(self.dea._get_dmu(False)) == 0:
                break

            inputs = self.dea._get_inputs(False)
            outputs = self.dea._get_outputs(False)
            index = self.dea._get_index(False)
