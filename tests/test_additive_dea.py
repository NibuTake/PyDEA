import numpy as np
import pandas as pd

from Pyfrontier.frontier_model import AdditiveDEA


def test_additive_solve():
    df = pd.DataFrame(
        {
            "input_1": [1, 1.5, 3, 3],
            "input_2": [3, 1.5, 1, 3],
            "output": [16, 16, 16, 16],
        }
    )

    x_weight = np.array([0.1, 0.9])
    y_weight = np.array([0])

    dea = AdditiveDEA(frontier="CRS")
    dea.fit(
        df[["input_1", "input_2"]].to_numpy(),
        df[["output"]].to_numpy(),
        x_weight=x_weight,
        y_weight=y_weight,
    )

    slack_result = [
        (r.x_slack, r.y_slack) for r in dea.result if r.is_efficient is False
    ]
    assert slack_result == [([0.0, 2.0], [0.0])]
