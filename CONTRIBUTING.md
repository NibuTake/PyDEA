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
- fork repository
- activate virtual environment
    - [pipenv](./python_version/dev/Pipfile)

```bash
cd python_version/dev
pipenv shell
install pre-commit
```

### Code style
We use black and flake 8. These are executed when committing by pre-commit.

### Unit tests
This will be done in github actions in the future, but here is how to do it when developing locally.

```bash
pytest tests
```

### Documentation
We use [shpinx](https://www.sphinx-doc.org/en/master/index.html) to generate document.
Basically, it is generated from a docstring, and the tutorials are generated from a python file found [here](./tutorials/).

This command makes a docs folder. Run this command if you have updated the docstring or if you have updated or added a tutorial. In the future, we would like it to be executed automatically on commit.

```bash
. build_docs.sh
```

### Pull request
No policy has been set at this time.
