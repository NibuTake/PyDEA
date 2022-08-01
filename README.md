# Pyfrontier: A data envelopment analysis module
<div align="center"><img src="./_docs_src/img/logo.png" height="200"/></div>

[Install](#installation) | [Tutorial](#tutorial) | [Docs](#documentation) | [Communication](#communication)| [References](#references)

Pyfrontier is a data envelopment analysis for Python user. Our main motivation is to encourage more people to apply DEA effectively and contribute to the development of this field.

This covers the following functions.

- Data envelopment analysis (DEA)
    - VRS, CRS
    - multiple, envelope model
- Free disposal hull (FDH)
- Hierarchical model

Unfortunately we are still preparing this module until everyone can use it comfortably without any obstacles.

## Installation
This is an interim response until we open it up to pypI. We apologize for any inconvenience.

```
git clone https://github.com/NibuTake/PyDEA.git
pip install .
```

## Tutorial
- [What is DEA?]()
- Example

```python
import numpy as np
from Pyfrontier.frontier_model import EnvelopeDEA

dea = EnvelopeDEA(frontier="CRS", orient="in")

dea.fit(inputs, outputs)
dea.result
```

## Documentation

- [API references](https://nibutake.github.io/PyDEA/index.html?)
- [Algorithms]()

## Communication
- [Issues](https://github.com/NibuTake/PyDEA/issues) for bug reports and feature requests.
- [Discussion](https://github.com/NibuTake/PyDEA/discussions) for any questions.

## References
- [yamada](./references/yamada.md)

## MEMO
```
sphinx-apidoc -f -o ./_docs_src ./src
sphinx-build ./_docs_src ./docs
touch .nojekyll .docs
```
