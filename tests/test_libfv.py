#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import os.path
import re

import pytest

from fontTools.ttLib import TTLibError

from fontv.libfv import FontVersion

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

meta_testfiles_list = [
    "tests/testfiles/Test-VersionMeta.ttf",
    "tests/testfiles/Test-VersionMoreMeta.ttf"
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


@pytest.fixture(params=meta_testfiles_list)
def metafonts(request):
    return request.param


@pytest.fixture(params=dev_testfiles_list)
def devfonts(request):
    return request.param


@pytest.fixture(params=rel_testfiles_list)
def relfonts(request):
    return request.param


# testi
def _test_hexadecimal_sha1_string_matches(needle):
    p = re.compile("""[(a-f|0-9)]{7,10}""")
    m = p.match(needle)
    if m is None:
        return False
    else:
        return True


# TESTS

def test_libfv_missing_file_read_attempt():
    with pytest.raises(IOError):
        fv = FontVersion("tests/testfiles/bogus.ttf")


def test_libfv_nonfont_file_read_attempt():
    with pytest.raises(TTLibError):
        fv = FontVersion("tests/testfiles/test.txt")


def test_libfv_fontversion_obj_instantiation(allfonts):
    fv = FontVersion(allfonts)


def test_libfv_version_string_property_set_on_instantiation(allfonts):
    fv = FontVersion(allfonts)
    assert fv.version == "Version 1.010"


def test_libfv_fontversion_object_parameter_properties_defaults(allfonts):
    fv = FontVersion(allfonts)
    assert fv.develop_string == "DEV"
    assert fv.release_string == "RELEASE"
    assert fv.sha1_develop == "-dev"
    assert fv.sha1_release == "-release"


def test_libfv_fontversion_object_properties_truth_defaults():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    assert fv.contains_metadata is False
    assert fv.contains_status is False
    assert fv.is_development is False
    assert fv.is_release is False


def test_libfv_fontversion_object_properties_truth_defaults_with_metaonly(metafonts):
    fv = FontVersion(metafonts)
    assert fv.contains_metadata is True
    assert fv.contains_status is False
    assert fv.is_development is False
    assert fv.is_release is False


def test_libfv_fontversion_object_properties_truth_development(devfonts):
    fv = FontVersion(devfonts)
    assert fv.contains_metadata is True
    assert fv.contains_status is True
    assert fv.is_development is True
    assert fv.is_release is False


def test_libfv_fontversion_object_properties_truth_release(relfonts):
    fv = FontVersion(relfonts)
    assert fv.contains_metadata is True
    assert fv.contains_status is True
    assert fv.is_development is False
    assert fv.is_release is True


def test_libfv_fontversion_object_versionparts_meta_lists_versionstring_only():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    assert len(fv.version_string_parts) == 1
    assert len(fv.metadata) == 0


def test_libfv_fontversion_object_versionparts_meta_lists_version_with_onemeta():
    fv = FontVersion("tests/testfiles/Test-VersionMeta.ttf")
    assert len(fv.version_string_parts) == 2
    assert fv.version_string_parts[0] == "Version 1.010"
    assert fv.version_string_parts[1] == "metadata string"
    assert len(fv.metadata) == 1
    assert fv.metadata[0] == "metadata string"


def test_libfv_fontversion_object_versionparts_meta_lists_version_with_twometa():
    fv = FontVersion("tests/testfiles/Test-VersionMoreMeta.ttf")
    assert len(fv.version_string_parts) == 3
    assert fv.version_string_parts[0] == "Version 1.010"
    assert fv.version_string_parts[1] == "metadata string"
    assert fv.version_string_parts[2] == "another metadata string"
    assert len(fv.metadata) == 2
    assert fv.metadata[0] == "metadata string"
    assert fv.metadata[1] == "another metadata string"


def test_libfv_clear_metadata_method(allfonts):
    fv = FontVersion(allfonts)
    fv.clear_metadata()
    assert len(fv.version_string_parts) == 1
    assert fv.version_string_parts[0] == "Version 1.010"


def test_libfv_get_version_string_method():
    fv1 = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    fv2 = FontVersion("tests/testfiles/Test-VersionMeta.ttf")
    fv3 = FontVersion("tests/testfiles/Test-VersionMoreMeta.ttf")
    assert fv1.get_version_string() == "Version 1.010"
    assert fv2.get_version_string() == "Version 1.010;metadata string"
    assert fv3.get_version_string() == "Version 1.010;metadata string;another metadata string"


def test_libfv_set_development_method_on_versiononly():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    assert len(fv.version_string_parts) == 1
    fv.set_development_status()
    assert len(fv.version_string_parts) == 2
    assert fv.version_string_parts[0] == "Version 1.010"
    assert fv.version_string_parts[1] == "DEV"
    assert fv.is_development is True
    assert fv.is_release is False
    assert fv.contains_status is True
    assert fv.contains_metadata is True


def test_libfv_set_development_method_on_release(relfonts):
    fv = FontVersion(relfonts)
    prelength = len(fv.version_string_parts)
    fv.set_development_status()
    postlength = len(fv.version_string_parts)
    assert prelength == postlength
    assert fv.version_string_parts[0] == "Version 1.010"
    assert fv.version_string_parts[1] == "DEV"
    assert fv.is_development is True
    assert fv.is_release is False
    assert fv.contains_status is True
    assert fv.contains_metadata is True


def test_libfv_set_development_method_on_development(devfonts):
    fv = FontVersion(devfonts)
    prelength = len(fv.version_string_parts)
    fv.set_development_status()
    postlength = len(fv.version_string_parts)
    assert prelength == postlength
    assert fv.version_string_parts[0] == "Version 1.010"
    assert fv.version_string_parts[1] == "DEV"
    assert fv.is_development is True
    assert fv.is_release is False
    assert fv.contains_status is True
    assert fv.contains_metadata is True


def test_libfv_set_development_method_on_nostatus(metafonts):
    fv = FontVersion(metafonts)
    prelength = len(fv.version_string_parts)
    fv.set_development_status()
    postlength = len(fv.version_string_parts)
    assert prelength == (postlength - 1)   # should add an additional substring to the version string here
    assert fv.version_string_parts[0] == "Version 1.010"
    assert fv.version_string_parts[1] == "DEV"
    assert fv.is_development is True
    assert fv.is_release is False
    assert fv.contains_status is True
    assert fv.contains_metadata is True


def test_libfv_set_release_method_on_versiononly():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    assert len(fv.version_string_parts) == 1
    fv.set_release_status()
    assert len(fv.version_string_parts) == 2
    assert fv.version_string_parts[0] == "Version 1.010"
    assert fv.version_string_parts[1] == "RELEASE"
    assert fv.is_development is False
    assert fv.is_release is True
    assert fv.contains_status is True
    assert fv.contains_metadata is True


def test_libfv_set_release_method_on_release(relfonts):
    fv = FontVersion(relfonts)
    prelength = len(fv.version_string_parts)
    fv.set_release_status()
    postlength = len(fv.version_string_parts)
    assert prelength == postlength
    assert fv.version_string_parts[0] == "Version 1.010"
    assert fv.version_string_parts[1] == "RELEASE"
    assert fv.is_development is False
    assert fv.is_release is True
    assert fv.contains_status is True
    assert fv.contains_metadata is True


def test_libfv_set_release_method_on_development(devfonts):
    fv = FontVersion(devfonts)
    prelength = len(fv.version_string_parts)
    fv.set_release_status()
    postlength = len(fv.version_string_parts)
    assert prelength == postlength
    assert fv.version_string_parts[0] == "Version 1.010"
    assert fv.version_string_parts[1] == "RELEASE"
    assert fv.is_development is False
    assert fv.is_release is True
    assert fv.contains_status is True
    assert fv.contains_metadata is True


def test_libfv_set_release_method_on_nostatus(metafonts):
    fv = FontVersion(metafonts)
    prelength = len(fv.version_string_parts)
    fv.set_release_status()
    postlength = len(fv.version_string_parts)
    assert prelength == (postlength - 1)   # should add an additional substring to the version string here
    assert fv.version_string_parts[0] == "Version 1.010"
    assert fv.version_string_parts[1] == "RELEASE"
    assert fv.is_development is False
    assert fv.is_release is True
    assert fv.contains_status is True
    assert fv.contains_metadata is True


def test_libfv_set_gitsha1_bad_parameters_raises_valueerror(allfonts):
    with pytest.raises(ValueError):
        fv = FontVersion(allfonts)
        fv.set_git_commit_sha1(development=True, release=True)


def test_libfv_set_default_gitsha1_method(allfonts):
    fv = FontVersion(allfonts)
    fv.set_git_commit_sha1()
    sha_needle = fv.version_string_parts[1]
    assert _test_hexadecimal_sha1_string_matches(sha_needle) is True
    assert ("-dev" in sha_needle) is False
    assert ("-release" in sha_needle) is False


def test_libfv_set_development_gitsha1_method(allfonts):
    fv = FontVersion(allfonts)
    fv.set_git_commit_sha1(development=True)
    sha_needle = fv.version_string_parts[1]
    assert _test_hexadecimal_sha1_string_matches(sha_needle) is True
    assert ("-dev" in sha_needle) is True
    assert ("-release" in sha_needle) is False


def test_libfv_set_release_gitsha1_method(allfonts):
    fv = FontVersion(allfonts)
    fv.set_git_commit_sha1(release=True)
    sha_needle = fv.version_string_parts[1]
    assert _test_hexadecimal_sha1_string_matches(sha_needle) is True
    assert ("-dev" in sha_needle) is False
    assert ("-release" in sha_needle) is True


def test_libfv_set_version_number(allfonts):
    fv = FontVersion(allfonts)
    prelength = len(fv.version_string_parts)
    fv.set_version_number("2.000")
    postlength = len(fv.version_string_parts)
    assert prelength == postlength
    assert fv.version_string_parts[0] == "Version 2.000"
    assert fv.version == "Version 2.000"


def test_libfv_set_version_string_one_substring():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    fv.set_version_string("Version 2.000")
    assert len(fv.version_string_parts) == 1
    assert fv.version_string_parts[0] == "Version 2.000"


def test_libfv_set_version_string_two_substrings():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    fv.set_version_string("Version 2.000;DEV")
    assert len(fv.version_string_parts) == 2
    assert fv.version_string_parts[0] == "Version 2.000"
    assert fv.version_string_parts[1] == "DEV"


def test_libfv_set_version_string_three_substrings():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    fv.set_version_string("Version 2.000;DEV;other stuff")
    assert len(fv.version_string_parts) == 3
    assert fv.version_string_parts[0] == "Version 2.000"
    assert fv.version_string_parts[1] == "DEV"
    assert fv.version_string_parts[2] == "other stuff"


def test_libfv_write_version_string_method(allfonts):
    temp_out_file_path = os.path.join("tests", "testfiles", "Test-Temp.ttf")  # temp file write path
    fv = FontVersion(allfonts)
    fv.set_version_number("2.000")
    fv.write_version_string(fontpath=temp_out_file_path)
    fv2 = FontVersion(temp_out_file_path)
    assert fv2.version_string_parts[0] == "Version 2.000"
    # modify again to test write to same temp file path without use of the fontpath parameter in
    # order to test the block of code where that is handled
    fv2.set_version_number("3.000")
    fv2.write_version_string()
    fv3 = FontVersion(temp_out_file_path)
    assert fv3.version_string_parts[0] == "Version 3.000"

    os.remove(temp_out_file_path)

