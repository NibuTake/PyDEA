"""
Returns to scale
=========================

Preparing...
"""

# %%
# Import modules and prepare data.
# ------------------------
# Average of rental properties in a given district.

import matplotlib.pyplot as plt
import pandas as pd

from Pyfrontier.frontier_model import MultipleDEA

sample_df = pd.DataFrame(
    {
        "input": [
            1,
            2,
            4,
            6,
        ],
        "output": [
            0.5,
            2,
            4,
            5,
        ],
    }
)
sample_df
# %%
# Fit dea model.
# ------------------------------
#
# The necessity inputs are inputs and outputs. The result has below belongings.
dea = MultipleDEA("VRS", "in")
dea.fit(
    sample_df[["input"]].to_numpy(),
    sample_df[["output"]].to_numpy(),
)

dea.result
# %%
plt.figure()
plt.plot(sample_df["input"], sample_df["output"])
# %%
# %%
