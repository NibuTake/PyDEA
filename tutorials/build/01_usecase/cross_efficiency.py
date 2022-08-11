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
#    Author
#       John Doyle and Rodney Green.
#    Title
#       *Efficiency and Cross-efficiency in DEA: Derivations, Meanings and Uses*,
#     Journal of the Operational Research Society,
#     1994.
#     :numref:`https://doi.org/10.1057/jors.1994.84`.


# %%
# .. seealso::
#
#    Author
#       Sexton, Thomas R. and Silkman, Richard H. and Hogan, Andrew J..
#    Title
#       *Data envelopment analysis: Critique and extensions*,
#     New Directions for Program Evaluation,
#     1986.
#     :numref:`https://onlinelibrary.wiley.com/doi/abs/10.1002/ev.1441`.
