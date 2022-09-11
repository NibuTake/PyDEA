#!/usr/bin/bash
echo "Start building source"
rm -rf ./build
rm -rf ./dist
python setup.py sdist
python setup.py bdist_wheel
echo "Done building source"
