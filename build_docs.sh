#!/usr/bin/bash
echo "Start building docs"
python tutorials/bib-build.py
rm -rf ./_docs_src/tutorials
rm -rf ./docs
sphinx-apidoc -f -o ./_docs_src ./src
sphinx-build ./_docs_src ./docs
touch .nojekyll ./docs
echo "Done building docs"
