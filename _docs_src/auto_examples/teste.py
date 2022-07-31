"""
.. _first:
1. Lightweight, versatile, and platform agnostic architecture
=============================================================
Optuna is entirely written in Python and has few dependencies.
This means that we can quickly move to the real example once you get interested in Optuna.
Quadratic Function Example
--------------------------
Usually, Optuna is used to optimize hyperparameters, but as an example,
let's optimize a simple quadratic function: :math:`(x - 2)^2`.
"""


###################################################################################################
# First of all, import :mod:`optuna`.


###################################################################################################
# In optuna, conventionally functions to be optimized are named `objective`.


def objective(trial):
    x = trial.suggest_float("x", -10, 10)
    return (x - 2) ** 2


###################################################################################################
