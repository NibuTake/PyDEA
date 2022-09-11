from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

# import Pyfrontier


URL = "https://nibutake.github.io/PyDEA/index.html?"
DOWNLOAD_URL = "https://github.com/NibuTake/PyDEA"

DESCRIPTION = "Pyfrontier is a data envelopment analysis for Python user."

PYTHON_REQUIRES = ">=3.8"
INSTALL_REQUIRES = ["numpy>=1.21", "pulp>=2.6.0"]

with open("README.md", "r") as fp:
    readme = fp.read()
long_description = readme


CLASSIFIERS = [
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries",
]


setup(
    name="Pyfrontier",
    # version=Pyfrontier.__version__,
    version="0.1.1",
    license="MIT",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Takeshi Morinibu",
    author_email="takeshi715tech@gmail.com",
    url=URL,
    download_url=DOWNLOAD_URL,
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*/*/*/*.py")],
    include_package_data=True,
    zip_safe=False,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    classifiers=CLASSIFIERS,
)
