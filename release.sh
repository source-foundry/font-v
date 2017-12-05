#!/bin/sh

python3 setup.py sdist bdist_wheel
twine upload dist/font-v-0.4.1*
twine upload dist/font_v-0.4.1*
