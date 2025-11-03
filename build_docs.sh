#!/usr/bin/bash
echo "Start building docs"
uv run python tutorials/bib-build.py
rm -rf ./_docs_src/tutorials
rm -rf ./docs
uv run sphinx-apidoc -f -o ./_docs_src ./src
uv run sphinx-build ./_docs_src ./docs
uv run python fix_gallery_links.py
echo "Done building docs"
