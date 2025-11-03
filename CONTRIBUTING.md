# Contribution Guidelines
We appreciate any efforts that help us to make this module better!
You can help with code, reporting error or adding document.

There are some ways to sophisticate this project:
- Implement a feature
    - If you have some functions or idea about DEA, please open an issue first to discuss.
- Complement document
    - Unfortunately, the tutorial is not yet sufficient. It would be helpful if you could add the missing information.
- Refactor code
    - If you find a better implementation than the existing code, please let us know.
- Report a bug
    - If you find a bug, please report it. It is an opportunity to strengthen the reliability of the module.
- Add an advanced application
    - The idea of applying DEA is to increase creativity for the user. If you come up with one, please open an issue.


## Issue Guidelines
Preparing...

## Pull Request Guidelines
If you make a pull request, please follow the guidelines below:

- [Setup](#setup)
- [Code formatter](#code-style)
- [Tests](#unit-tests)
- [Documentation](#documentation)
- [Creating a Pull Request](#pull-request)

### Setup

#### Prerequisites

- Python 3.8 or higher
- [uv](https://github.com/astral-sh/uv) (recommended package manager)

#### Setup Development Environment

1. Fork the repository
2. Clone your fork and navigate to the directory
3. Install dependencies:

```bash
# Install dependencies
uv sync --all-groups
```

### Code style
We use black and flake8. These are executed when committing by pre-commit.

```bash
# Install pre-commit hooks
uv run pre-commit install
```

### Unit tests

#### Run tests with current Python version

```bash
uv run pytest tests/ --cov=src/Pyfrontier
```

#### Test across all Python versions (3.8-3.13)

```bash
bash test_all_versions.sh
```

#### Test specific Python version only

```bash
bash test_all_versions.sh 3.13
```

**Note**: The `test_all_versions.sh` script automatically downloads and tests against all supported Python versions (3.8-3.13) using uv. No manual Python installation required!

### Documentation

We use [Sphinx](https://www.sphinx-doc.org/en/master/index.html) to generate documentation.
Basically, it is generated from docstrings, and the tutorials are generated from Python files found in [tutorials/](./tutorials/).

#### Build documentation locally

```bash
bash build_docs.sh
```

This command generates the docs folder. Run this command if you have updated docstrings or if you have updated or added tutorials.

#### Documentation Deployment

Documentation is automatically deployed to GitHub Pages via GitHub Actions when:
- A new release is published
- Changes are pushed to `main` branch (docs-related files)
- Manually triggered via workflow dispatch

**First-time GitHub Pages Setup:**
1. Go to repository Settings → Pages
2. Under "Build and deployment":
   - Source: Select "GitHub Actions"
3. The workflow will automatically deploy on the next trigger

### Pull request
No policy has been set at this time.

### Deploy

```bash
rm -rf dist build src/Pyfrontier.egg-info
uv build
uv run twine upload --repository testpypi dist/*
```