import pytest

import pandas as pd

from Pyfrontier.frontier_model import EnvelopDEA, HierarchalDEA


def test_can_work_hierarchal_model():
    df = pd.DataFrame(
        {
            "input_1": [4, 2, 1, 1, 5, 2.5, 1.5, 5, 4, 2.5],
            "input_2": [1, 1.5, 3, 4, 2, 2.5, 5, 3, 3, 4.5],
            "output": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        }
    )

    h_dea = HierarchalDEA(EnvelopDEA("CRS", "in", n_jobs=2))

    h_dea.fit(df[["input_1", "input_2"]].to_numpy(), df[["output"]].to_numpy())
