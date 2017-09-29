#!/bin/sh

python3 setup.py sdist bdist_wheel
twine upload dist/font-v-0.3.0*
