#!/usr/bin/env bash

PREFIX=../lib/fontv

pylint --disable=line-too-long,fixme "$PREFIX"/app.py "$PREFIX"/libfv.py "$PREFIX"/utilities.py

