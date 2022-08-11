"""
Context-dependent DEA
=========================

This example.

"""

# %%
# Import libraries.
# ------------------------
# Hie

import matplotlib.pyplot as plt
import pandas as pd

from Pyfrontier.frontier_model import EnvelopDEA, HierarchalDEA

# %%
df = pd.DataFrame(
    {
        "input_1": [4, 2, 1, 1, 5, 2.5, 1.5, 5, 4, 2.5],
        "input_2": [1, 1.5, 3, 4, 2, 2.5, 5, 3, 3, 4.5],
        "output": [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
    }
)

h_dea = HierarchalDEA(EnvelopDEA("CRS", "in"))

h_dea.fit(df[["input_1", "input_2"]].to_numpy(), df[["output"]].to_numpy())

h_dea.result[0]
# %%
plt.figure()
for res in h_dea.result:
    plt.plot(
        [r.dmu.input[0] for r in res],
        [r.dmu.input[1] for r in res],
        "o-",
        color="C0",
    )
# %%
# References
# ------------------------
# .. seealso::
#
#    Author
#       Lawrence M. Seiford and Joe Zhu.
#    Title
#       *Context-dependent data envelopment analysis—Measuring attractiveness and progress*,
#     Omega-international Journal of Management Science,
#     2003.
#     :numref:`https://EconPapers.repec.org/RePEc:eee:jomega:v:31:y:2003:i:5:p:397-408`.
