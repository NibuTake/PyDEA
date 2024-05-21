"""
Ex. sample
=========================

This example doesn't do much, it just makes a simple plot
"""

# %%
# Import libraries.
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
# In the built documentation.
plt
