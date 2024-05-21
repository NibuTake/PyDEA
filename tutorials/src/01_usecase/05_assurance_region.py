"""
Assurance region
=========================

Preparing...

"""

# %%
# .. math::
#    \alpha_i \leq \frac{\nu_i}{\nu_{i_o}} \beta_i, i= 1, \dots, m

# %%
# Import modules and prepare data.
# ------------------------
#
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from Pyfrontier.frontier_model import MultipleDEA

df = pd.DataFrame({"price": [1, 2, 4, 6], "rent": [5, 2, 1, 1], "output": [3, 3, 3, 3]})

df
# %%
# これによって乗数同士の重要性などを加味することができる。
#
# .. math::
#    1 \leq \frac{x_{price}}{x_{rent}} \leq 2

# %%
dea = MultipleDEA("CRS", "in")
dea.fit(df[["price", "rent"]].to_numpy(), df[["output"]].to_numpy())

print("ordinary dea: ", [r.score for r in dea.result])

# %%
dea_ar = MultipleDEA("CRS", "in")
dea_ar.add_assurance_region("in", index_a=0, index_b=1, coefficient=2, operator="<=")
dea_ar.add_assurance_region("in", index_a=0, index_b=1, coefficient=1, operator=">=")
dea_ar.fit(df[["price", "rent"]].to_numpy(), df[["output"]].to_numpy())

print("assurance region: ", [r.score for r in dea_ar.result])


# %%
def restrict_f_1(x: np.ndarray):
    return -x + 4


def restrict_f_2(x: np.ndarray):
    return -2 * x + 6


x = np.array([0, 6])
x1 = np.array([2, 6])
x2 = np.array([0, 2])

plt.figure()
plt.plot(
    [r.dmu.input[0] for r in dea.result], [r.dmu.input[1] for r in dea.result], "o-"
)
plt.plot(x, restrict_f_1(x), linestyle="--", label="rent = price")
plt.plot(x, restrict_f_2(x), linestyle="--", label="price = 2*rent")
plt.fill_between(x1, restrict_f_1(x1), [6, 6], alpha=0.2, color="C0")
plt.fill_between(x2, restrict_f_2(x2), [6, 6], alpha=0.2, color="C0")
plt.plot(x1, restrict_f_1(x1), color="red")
plt.plot(x2, restrict_f_2(x2), color="red", label="frontier")
plt.xlabel("price")
plt.ylabel("rent")
plt.ylim(0, 6)
plt.legend()
plt.show()

# %%
# 通常のDEAで効率的だったDMUは、フロンティアの傾きに制約が課されることで一つのみとなった。


# %%
# References
# ------------------------
# .. seealso::
#
# <bib>THOMPSON199093</bib>
