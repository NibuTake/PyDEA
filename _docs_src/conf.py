# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

from recommonmark.parser import CommonMarkParser

import Pyfrontier

sys.path.insert(0, os.path.abspath("../"))


project = "Pyfrontier"
copyright = "2022, contributors"
author = "Contributors"
release = Pyfrontier.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.imgconverter",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx_gallery.gen_gallery",
    "sphinx_autodoc_typehints",
    "nbsphinx",
]
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "tutorials/**/*.ipynb"]
# exclude_patterns.append('**.ipynb_checkpoints')
source_suffix = [".rst"]

sphinx_gallery_conf = {
    "examples_dirs": [
        "../tutorials/build/01_usecase",
        "../tutorials/build/02_advanced",
    ],
    "gallery_dirs": [
        "tutorials/01_usecase",
        "tutorials/02_advanced",
    ],
    "within_subsection_order": "sphinx_gallery.sorting.FileNameSortKey",
    "filename_pattern": r"/*\.py",
    "first_notebook_cell": None,
    "remove_config_comments": True,
    "reference_url": {
        "Pyfrontier": None,
    },
}

nbsphinx_execute = "never"
nbsphinx_allow_errors = True

source_parsers = {
    ".md": CommonMarkParser,
}


# setting of mathjax
mathjax3_config = {
    "TeX": {
        "Macros": {
            "bm": ["{\\boldsymbol{#1}}", 1],
        },
    },
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

# Remove "Edit on GitHub."
html_show_sourcelink = False

# matplotlib plot directive
plot_include_source = True
plot_formats = [("png", 90)]
plot_html_show_formats = False
plot_html_show_source_link = False
