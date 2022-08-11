"""
Super efficiency
=========================

This example.
"""

# %%
# Import libraries.
# ------------------------
# 超効率性は自分自身を除くDMUによって測られる効率性であり１を超え得る。
# 効率値が１では比較し辛い場合に評価する手法。

import matplotlib.pyplot as plt
import pandas as pd

from Pyfrontier.frontier_model import EnvelopDEA

supply_chain_df = pd.DataFrame(
    {"cost": [1, 2, 4, 6, 4], "day": [4, 2, 1, 1, 4], "profit": [2, 2, 2, 2, 2]}
)
supply_chain_df
# %%
# Fit dea model.
# ------------------------------
#
# The necessity inputs are inputs and outputs. The result has below belongings.
dea = EnvelopDEA("CRS", "in", super_efficiency=True)
dea.fit(
    supply_chain_df[["day", "cost"]].to_numpy(),
    supply_chain_df[["profit"]].to_numpy(),
)

dea.result[1]


# %%
plt.figure()
plt.plot(
    [r.dmu.input[0] for r in dea.result[:-1]],
    [r.dmu.input[1] for r in dea.result[:-1]],
    "-o",
)
plt.plot([4, 6], [1, 1], color="C0")
plt.plot([1, 4], [4, 1], color="black", linestyle="--")
plt.legend()
plt.show()
# %%
