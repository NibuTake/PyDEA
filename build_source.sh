#!/usr/bin/bash
echo "Start building source"
python setup.py sdist
python setup.py bdist_wheel
echo "Done building source"
