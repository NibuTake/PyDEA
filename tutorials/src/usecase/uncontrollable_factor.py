"""
Uncontrollable factor
=========================

This example.
"""

# %%
# Import libraries.
# ------------------------
# 制御できない項目を指定してDEAを適用する。

import matplotlib.pyplot as plt
import pandas as pd

from Pyfrontier.frontier_model import EnvelopDEA

supply_chain_df = pd.DataFrame(
    {"cost": [1, 2, 4, 6, 4], "day": [4, 2, 1, 1, 4], "profit": [2, 2, 2, 2, 2]}
)
supply_chain_df

EnvelopDEA
plt
