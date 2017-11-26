#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys
import pytest


from fontv.libfv import FontVersion
from fontTools.ttLib import TTFont

# TEST FONT FILE CREATION
# fv = FontVersion("testfiles/Hack-Regular.ttf")
#
# fv.version_string_parts = ['Version 1.010']
# fv.write_version_string(fontpath="testfiles/Test-VersionOnly.ttf")
#
# fv.version_string_parts = ["Version 1.010", "DEV"]
# fv.write_version_string(fontpath="testfiles/Test-VersionDEV.ttf")
#
# fv.version_string_parts = ["Version 1.010", "RELEASE"]
# fv.write_version_string(fontpath="testfiles/Test-VersionREL.ttf")
#
# fv.version_string_parts = ["Version 1.010", "abcd123-dev"]
# fv.write_version_string(fontpath="testfiles/Test-VersionShaDEV.ttf")
#
# fv.version_string_parts = ["Version 1.010", "abcd123-release"]
# fv.write_version_string(fontpath="testfiles/Test-VersionShaREL.ttf")
#
# fv.version_string_parts = ["Version 1.010", "metadata string"]
# fv.write_version_string(fontpath="testfiles/Test-VersionMeta.ttf")
#
# fv.version_string_parts = ["Version 1.010", "metadata string", "another metadata string"]
# fv.write_version_string(fontpath="testfiles/Test-VersionMoreMeta.ttf")
#
# fv.version_string_parts = ["Version 1.010", "DEV", "metadata string"]
# fv.write_version_string(fontpath="testfiles/Test-VersionDEVMeta.ttf")
#
# fv.version_string_parts = ["Version 1.010", "RELEASE", "metadata string"]
# fv.write_version_string(fontpath="testfiles/Test-VersionRELMeta.ttf")
#
# fv.version_string_parts = ["Version 1.010", "abcd123-dev", "metadata string"]
# fv.write_version_string(fontpath="testfiles/Test-VersionShaDEVMeta.ttf")
#
# fv.version_string_parts = ["Version 1.010", "abcd123-release", "metadata string"]
# fv.write_version_string(fontpath="testfiles/Test-VersionShaRELMeta.ttf")


# Test file version strings

# Test-VersionDEV.ttf:
# Version 1.010;DEV

# Test-VersionDEVMeta.ttf:
# Version 1.010;DEV;metadata string

# Test-VersionMeta.ttf:
# Version 1.010;metadata string

# Test-VersionMoreMeta.ttf:
# Version 1.010;metadata string;another metadata string

# Test-VersionOnly.ttf:
# Version 1.010

# Test-VersionREL.ttf:
# Version 1.010;RELEASE

# Test-VersionRELMeta.ttf:
# Version 1.010;RELEASE;metadata string

# Test-VersionShaDEV.ttf:
# Version 1.010;abcd123-dev

# Test-VersionShaDEVMeta.ttf:
# Version 1.010;abcd123-dev;metadata string

# Test-VersionShaREL.ttf:
# Version 1.010;abcd123-release

# Test-VersionShaRELMeta.ttf:
# Version 1.010;abcd123-release;metadata string

all_testfiles_list = [
    "tests/testfiles/Test-VersionDEV.ttf",
    "tests/testfiles/Test-VersionDEVMeta.ttf",
    "tests/testfiles/Test-VersionMeta.ttf",
    "tests/testfiles/Test-VersionMoreMeta.ttf",
    "tests/testfiles/Test-VersionOnly.ttf",
    "tests/testfiles/Test-VersionREL.ttf",
    "tests/testfiles/Test-VersionRELMeta.ttf",
    "tests/testfiles/Test-VersionShaDEV.ttf",
    "tests/testfiles/Test-VersionShaDEVMeta.ttf",
    "tests/testfiles/Test-VersionShaREL.ttf",
    "tests/testfiles/Test-VersionShaRELMeta.ttf"
]

dev_testfiles_list = [
    "tests/testfiles/Test-VersionDEV.ttf",
    "tests/testfiles/Test-VersionDEVMeta.ttf",
    "tests/testfiles/Test-VersionShaDEV.ttf",
    "tests/testfiles/Test-VersionShaDEVMeta.ttf"
]

rel_testfiles_list = [
    "tests/testfiles/Test-VersionREL.ttf",
    "tests/testfiles/Test-VersionRELMeta.ttf",
    "tests/testfiles/Test-VersionShaREL.ttf",
    "tests/testfiles/Test-VersionShaRELMeta.ttf"
]

# pytest fixtures for parametrized testing of various groupings of test files


@pytest.fixture(params=all_testfiles_list)
def allfonts(request):
    return request.param


@pytest.fixture(params=dev_testfiles_list)
def devfonts(request):
    return request.param


@pytest.fixture(params=rel_testfiles_list)
def relfonts(request):
    return request.param


# TESTS

def test_libfv_fontversion_obj_instantiation(allfonts):
    fv = FontVersion(allfonts)


def test_libfv_version_string_property_set_on_instantiation(allfonts):
    fv = FontVersion(allfonts)
    assert fv.version == "Version 1.010"

