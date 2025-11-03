# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pyfrontier (PyDEA) is a Python library for Data Envelopment Analysis (DEA), a mathematical programming approach for evaluating the relative efficiency of decision-making units (DMUs). The library supports multiple DEA models including envelope models, multiplier models, additive models, and hierarchical models with various returns to scale (CRS, VRS, IRS, DRS).

## Development Commands

### Testing
```bash
# Run all tests with coverage
pytest tests/ --cov=src/Pyfrontier --cov-report=xml

# Run tests with pipenv (as done in CI)
pipenv run pytest -v tests/ --cov=src/Pyfrontier --cov-report=xml

# Run a single test file
pytest tests/frontier_model/test_envelop_dea.py
```

### Documentation
```bash
# Build documentation (runs Sphinx with tutorials)
./build_docs.sh

# This script:
# - Runs tutorials/bib-build.py to process bibliographies
# - Cleans old docs
# - Runs sphinx-apidoc to auto-generate API docs
# - Builds HTML docs to ./docs directory
```

### Code Quality
```bash
# Black formatter runs automatically via pre-commit
# To run manually:
black src/ tests/

# Install pre-commit hooks
pre-commit install
```

### Environment Setup
```bash
# Using pipenv (recommended)
pipenv shell
pipenv install --dev

# Or using pip directly
pip install -e .
pip install -r requirements.txt
```

## Architecture

### Core Design Pattern: Model-Solver Separation

The codebase follows a clear separation between **models** (frontier_model) and **solvers** (solver):

- **Models** (`src/Pyfrontier/frontier_model/`): High-level DEA model interfaces that users interact with
  - `EnvelopDEA`: Standard envelope models with radial efficiency measures
  - `MultipleDEA`: Multiplier/dual formulation with support for assurance regions
  - `AdditiveDEA`: Non-radial models (SBM, RAM, etc.)
  - `HierarchalDEA`: Multi-level hierarchical DEA models
  - All inherit from `BaseDataEnvelopmentAnalysis`

- **Solvers** (`src/Pyfrontier/solver/`): Low-level optimization implementations using PuLP
  - `EnvelopeSolver`: Implements envelope model LP formulations
  - `MultipleSolver`: Implements multiplier model LP formulations
  - `AdditiveSolver`: Implements additive model LP formulations
  - All inherit from `BaseSolver`
  - Handle actual linear programming problem construction and solving

### Data Flow

1. **Input**: User provides numpy arrays of inputs/outputs to a model's `fit()` method
2. **DMUSet Creation**: Data is wrapped in `DMUSet` domain object (in `domain/dmu.py`)
3. **Solver Invocation**: Model instantiates appropriate solver with configuration
4. **LP Problem**: Solver constructs PuLP LP problems for each DMU
5. **Result Objects**: Solver returns list of result objects (`EnvelopResult`, `MultipleResult`, or `AdditiveResult`)
6. **User Access**: Results available via model's `.result` or `.results` property

### Domain Objects (`src/Pyfrontier/domain/`)

- `DMU`: Individual decision-making unit with inputs, outputs, and ID
- `DMUSet`: Collection of DMUs with dimension properties (N, m, s)
- `EnvelopResult`, `MultipleResult`, `AdditiveResult`: Store efficiency scores, slacks, lambdas, and projections
- `AssuranceRegion`: Constraints on multiplier weights
- `SlackWeight`: Weights for slack variables in additive models
- `NumberOfJobs`, `MultiProcessor`: Parallel processing support

### Linear Programming Models (`src/Pyfrontier/solver/_models.py`)

Contains utility classes for LP problem construction:
- `Bias`: Manages convexity constraints for different returns to scale (VRS/IRS/DRS)
- Used by solvers to build appropriate LP formulations

## Key Implementation Details

### Returns to Scale (frontier parameter)
- **CRS** (Constant): No convexity constraint (sum of lambdas free)
- **VRS** (Variable): Sum of lambdas = 1
- **IRS** (Increasing): Sum of lambdas >= 1 (input-oriented) or <= 1 (output-oriented)
- **DRS** (Decreasing): Sum of lambdas <= 1 (input-oriented) or >= 1 (output-oriented)

### Orientation (orient parameter)
- **"in"** (Input-oriented): Minimize inputs while keeping outputs fixed
- **"out"** (Output-oriented): Maximize outputs while keeping inputs fixed

### Super-efficiency
When `super_efficiency=True` in EnvelopDEA, the DMU being evaluated is excluded from the reference set, allowing efficiency scores > 1 for efficient units.

### Uncontrollable Factors
The `uncontrollable_index` parameter in `fit()` specifies input/output indices that should not be improved in projections (e.g., environmental factors).

### Parallel Processing
Models accept `n_jobs` parameter to solve multiple DMU problems in parallel using multiprocessing.

## Testing Conventions

- Test fixtures in `tests/conftest.py` provide sample data
- Test files mirror source structure: `tests/frontier_model/test_envelop_dea.py` tests `src/Pyfrontier/frontier_model/_dea.py`
- Tests use pandas DataFrames but models accept numpy arrays
- Coverage tracked via pytest-cov

## Package Distribution

- Package name: **Pyfrontier** (PyPI)
- Module import: `from Pyfrontier.frontier_model import EnvelopDEA`
- Version: Defined in `src/Pyfrontier/__init__.py` and `setup.py`
- Source in `src/` directory, tests in `tests/` directory
- Built using setuptools with `setup.py`

## Documentation

- Main docs: https://nibutake.github.io/PyDEA/
- Uses Sphinx with sphinx-gallery for tutorial notebooks
- Tutorials in `_docs_src/tutorials/` are executable Python files that generate docs
- References managed via BibTeX in `tutorials/ref.bib`
