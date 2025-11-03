# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pyfrontier (PyDEA) is a Python library for Data Envelopment Analysis (DEA), a mathematical programming approach for evaluating the relative efficiency of decision-making units (DMUs). The library supports multiple DEA models including envelope models, multiplier models, additive models, and hierarchical models with various returns to scale (CRS, VRS, IRS, DRS).

## Development Commands

### Testing

**Local Testing (current Python version):**
```bash
# Run all tests with coverage
uv run pytest tests/ --cov=src/Pyfrontier --cov-report=xml

# Run a single test file
uv run pytest tests/frontier_model/test_envelop_dea.py
```

**Testing with Multiple Python Versions (using uv):**

uv supports running tests against multiple Python versions. Here are the methods:

```bash
# Method 1: Specify Python version with uv run
uv run --python 3.11 pytest tests/
uv run --python 3.12 pytest tests/
uv run --python 3.13 pytest tests/

# Method 2: Use uv with pyenv or similar to manage multiple Python installations
# First, ensure you have the Python versions installed (e.g., via pyenv)
# Then test against each version:
uv run --python python3.11 pytest tests/
uv run --python python3.12 pytest tests/
uv run --python python3.13 pytest tests/

# Method 3: Use the provided test script (recommended)
bash test_all_versions.sh

# Test a specific version only
bash test_all_versions.sh 3.13
```

**Using the test script (`test_all_versions.sh`):**
- Tests all supported Python versions (3.8-3.13) automatically
- Color-coded output for easy reading
- Summary report at the end
- Exit code indicates success/failure for CI integration

**Note**:
- uv automatically downloads and manages Python versions as needed
- No need to manually install Python versions
- For manual installation: Use `pyenv` (macOS/Linux) or `py` launcher (Windows)

**CI/CD Testing:**
The GitHub Actions workflow (`.github/workflows/unit_test.yml`) automatically tests against all supported Python versions (3.8-3.13) using a matrix strategy.

### Documentation
```bash
# Build documentation locally (runs Sphinx with tutorials)
bash build_docs.sh

# This script:
# - Runs tutorials/bib-build.py to process bibliographies
# - Cleans old docs
# - Runs sphinx-apidoc to auto-generate API docs
# - Runs sphinx-build to generate HTML docs to ./docs directory
# - Runs fix_gallery_links.py to fix gallery thumbnail links
```

**Automatic Deployment:**
- Documentation is automatically deployed to GitHub Pages via GitHub Actions
- Triggers:
  - Manual workflow dispatch
  - On release published
  - On push to main branch (when docs-related files change)
- Workflow file: `.github/workflows/deploy-docs.yml`

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
# Using uv (recommended)
uv sync --all-groups

# For development only dependencies
uv sync --group dev

# For production dependencies only
uv sync
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
- Uses Sphinx 8+ with sphinx-gallery 0.19+ for tutorial notebooks
- Source files in `tutorials/src/*/` (Python scripts with special formatting)
- Generated files in `_docs_src/tutorials/` (RST, images, notebooks)
- Built HTML in `docs/` directory (excluded from git via .gitignore)
- References managed via BibTeX in `tutorials/ref.bib`

### Documentation Build Process

1. **Tutorial Source Processing**: `tutorials/bib-build.py` copies `tutorials/src/` to `tutorials/build/` and processes BibTeX references
2. **Sphinx-Gallery Execution**: Executes Python scripts in `tutorials/build/`, generates RST files, notebooks, and plots
3. **API Documentation**: `sphinx-apidoc` generates API reference from docstrings
4. **HTML Generation**: `sphinx-build` generates final HTML documentation
5. **Post-Processing**: `fix_gallery_links.py` converts gallery thumbnail references to working HTML links

### Known Issues and Workarounds

**Gallery Thumbnail Links**: Sphinx-Gallery generates `:ref:` directives for thumbnails that don't resolve to clickable links in HTML. The `fix_gallery_links.py` script post-processes the HTML to convert these to proper `<a>` tags.

**Jupyter Notebook Conflicts**: The `.ipynb` files generated by Sphinx-Gallery are excluded via `exclude_patterns` in `conf.py` to prevent conflicts with the `.rst` files during Sphinx build.
