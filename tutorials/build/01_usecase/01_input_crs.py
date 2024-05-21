"""
Input oriented model
=========================

The following DEA model is an input-oriented model where the inputs are minimized and the outputs are kept at their current levels.

.. math::
    & \\theta^* = \min \\theta, subject \\ to \\\\
    & \sum_{j=1}^{n} \lambda_j x_{i, j} \leq \\theta x_{i, o}, i=1,2, \dots, m; \\\\
    & \sum_{j=1}^{n} \lambda_j y_{r, j} \geq y_{r, o}, r=1,2, \dots, s; \\\\
    & \sum_{j=1}^{n} \lambda_j = 1 \\\\
    & \lambda_j \geq 0, j=1,2, \dots, n.

where :math:`DMU_o` represents one of the :math:`n` DMUs under evaluation,
and :math:`x_{i, o}` and :math:`y_{i, o}` are the :math:`i` th input and :math:`r` th output
for :math:`DMU_o`, respectively.
"""

# %%
# Import modules and prepare data.
# ------------------------
# Sample supply chain data is generated.

import matplotlib.pyplot as plt
import pandas as pd

from Pyfrontier.frontier_model import EnvelopDEA

supply_chain_df = pd.DataFrame(
    {"day": [1, 2, 4, 6, 4], "cost": [5, 2, 1, 1, 4], "profit": [15, 15, 15, 15, 15]}
)
supply_chain_df
# %%
# Fit dea model.
# ------------------------------
#
# The necessity inputs are inputs and outputs. The result has below belongings.
dea = EnvelopDEA("CRS", "in")
dea.fit(
    supply_chain_df[["day", "cost"]].to_numpy(),
    supply_chain_df[["profit"]].to_numpy(),
)

dea.result[0]
# %%
# Visualize the result.
# ------------------------------
#
# .
eff_dmu = [r.dmu for r in dea.result if r.is_efficient]
ineff_dmu = [r.dmu for r in dea.result if r.is_efficient != 1]
weak_eff_dmu = [r.dmu for r in dea.result if r.has_slack]

plt.figure()
plt.plot(
    [d.input[0] for d in eff_dmu],
    [d.input[1] for d in eff_dmu],
    "-o",
    label="efficient dmu",
)
plt.plot(
    [d.input[0] for d in ineff_dmu],
    [d.input[1] for d in ineff_dmu],
    "o",
    label="not-efficient dmu",
)
plt.plot(
    [d.input[0] for d in weak_eff_dmu],
    [d.input[1] for d in weak_eff_dmu],
    "o",
    label="weak-efficient dmu",
)
plt.plot([4, 6], [1, 1], linestyle="--", color="black")
plt.legend()
plt.show()


# %%
# About slack
# ------------------------------
#
# .

print([r.score for r in dea.result])
print([r.is_efficient for r in dea.result])
print([r.has_slack for r in dea.result])

print(dea.result[-2].x_slack, dea.result[-2].y_slack)

# %%
