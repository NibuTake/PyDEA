"""
Cross efficiency
=========================

This example.

"""

# %%
import matplotlib.pyplot as plt
import pandas as pd

from Pyfrontier.frontier_model import MultipleDEA

df = pd.DataFrame(
    {"price": [3, 2, 4, 6, 4], "rent": [5, 2, 2, 1, 6], "output": [2, 1.5, 3, 2, 2]}
)

# %%

dea = MultipleDEA("CRS", "in")
dea.fit(df[["price", "rent"]].to_numpy(), df[["output"]].to_numpy())
# %%
dea.result[0]
# %%
[r.score for r in dea.result]
# %%
dea.cross_efficiency
# %%
efficiency_matrix = dea._cross_efficiency_matrix()

plt.figure()
plt.imshow(efficiency_matrix, interpolation="nearest", vmin=0, vmax=1, cmap="Blues")
plt.colorbar()
plt.show()
# %%
# References
# ------------------------
# .. seealso::
#
# <bib>Doyle1994Cross</bib>

# %%
# .. seealso::
#
# <bib>Sexton1986DEA</bib>
