#!/bin/sh

coverage run --source fontv -m py.test
coverage report -m
# coverage html

#coverage xml
#codecov --token=$CODECOV_{{font-v}}
