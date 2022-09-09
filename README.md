# Pyfrontier: A data envelopment analysis module
<div align="center"><img src="./images/logo.png" height="200"/></div>

[Install](#installation) | [Tutorial](https://nibutake.github.io/PyDEA/tutorials/index.html#) | [Docs](https://nibutake.github.io/PyDEA/index.html) | [Contribution](./CONTRIBUTING.md)

Pyfrontier is a data envelopment analysis for Python user. Our main motivation is to encourage more people to apply DEA effectively and contribute to the development of this field.

Unfortunately we are still preparing this module until everyone can use it comfortably without any obstacles...

## Installation
This is an interim response until we open it up to pypI. We apologize for any inconvenience.

```
git clone https://github.com/NibuTake/PyDEA.git
pip install .
```

## Tutorial
A brief example is provided below. For more information, please click [here](https://nibutake.github.io/PyDEA/tutorials/index.html#).

```python
import numpy as np
from Pyfrontier.frontier_model import EnvelopeDEA

dea = EnvelopeDEA(frontier="CRS", orient="in")

dea.fit(inputs, outputs)
dea.result
```

## Communication
- [Issues](https://github.com/NibuTake/PyDEA/issues) for bug reports and feature requests.
- [Discussion](https://github.com/NibuTake/PyDEA/discussions) for any questions.

## References
We use [ref.bib](./tutorials/ref.bib) for tutorial.
These are read by [bibtexparser](https://bibtexparser.readthedocs.io/en/master/) and automatically quoted and displayed at the specified location.
