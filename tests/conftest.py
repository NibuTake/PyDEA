import sys

sys.path.append("./PyDEA")

import pandas as pd
import pytest


@pytest.fixture
def sample_data():
    df = pd.DataFrame()
    df["Day"] = [1, 2, 4, 6, 4, 2, 5, 3]
    df["Cost"] = [5, 2, 1, 1, 4, 4, 2, 3]
    df["Ben"] = [15, 15, 15, 15, 15, 15, 15, 15]

    return df


@pytest.fixture
def house_data():
    import os

    print(os.getcwd())
    df = pd.read_csv("./tests/data/houses.csv")
    return df
