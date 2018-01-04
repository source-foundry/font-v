#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import os.path
import re

import pytest

from fontTools.ttLib import TTFont, TTLibError

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
# fv.version_string_parts = ["Version 1.010", "[abcd123]"]
# fv.write_version_string(fontpath="testfiles/Test-VersionSha.ttf")
#
# fv.version_string_parts = ["Version 1.010", "[abcd123]", "metadata string"]
# fv.write_version_string(fontpath="testfiles/Test-VersionShaMeta.ttf")
#
# fv.version_string_parts = ["Version 1.010", "[abcd123]-dev"]
# fv.write_version_string(fontpath="testfiles/Test-VersionShaDEV.ttf")
#
# fv.version_string_parts = ["Version 1.010", "[abcd123]-release"]
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
# fv.version_string_parts = ["Version 1.010", "[abcd123]-dev", "metadata string"]
# fv.write_version_string(fontpath="testfiles/Test-VersionShaDEVMeta.ttf")
#
# fv.version_string_parts = ["Version 1.010", "[abcd123]-release", "metadata string"]
# fv.write_version_string(fontpath="testfiles/Test-VersionShaRELMeta.ttf")


# Test file version strings (ttf shown, otf with same paths include the same version strings)

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

# Test-VersionSha.ttf:
# Version 1.010;[abcd123]

# Test-VersionShaMeta.ttf:
# Version 1.010;[abcd123];metadata string

# Test-VersionShaDEV.ttf:
# Version 1.010;[abcd123]-dev

# Test-VersionShaDEVMeta.ttf:
# Version 1.010;[abcd123]-dev;metadata string

# Test-VersionShaREL.ttf:
# Version 1.010;[abcd123]-release

# Test-VersionShaRELMeta.ttf:
# Version 1.010;[abcd123]-release;metadata string

all_testfiles_list = [
    "tests/testfiles/Test-VersionDEV.ttf",
    "tests/testfiles/Test-VersionDEVMeta.ttf",
    "tests/testfiles/Test-VersionMeta.ttf",
    "tests/testfiles/Test-VersionMoreMeta.ttf",
    "tests/testfiles/Test-VersionOnly.ttf",
    "tests/testfiles/Test-VersionREL.ttf",
    "tests/testfiles/Test-VersionRELMeta.ttf",
    "tests/testfiles/Test-VersionSha.ttf",
    "tests/testfiles/Test-VersionShaMeta.ttf",
    "tests/testfiles/Test-VersionShaDEV.ttf",
    "tests/testfiles/Test-VersionShaDEVMeta.ttf",
    "tests/testfiles/Test-VersionShaREL.ttf",
    "tests/testfiles/Test-VersionShaRELMeta.ttf",
    "tests/testfiles/Test-VersionDEV.otf",
    "tests/testfiles/Test-VersionDEVMeta.otf",
    "tests/testfiles/Test-VersionMeta.otf",
    "tests/testfiles/Test-VersionMoreMeta.otf",
    "tests/testfiles/Test-VersionOnly.otf",
    "tests/testfiles/Test-VersionREL.otf",
    "tests/testfiles/Test-VersionRELMeta.otf",
    "tests/testfiles/Test-VersionSha.otf",
    "tests/testfiles/Test-VersionShaMeta.otf",
    "tests/testfiles/Test-VersionShaDEV.otf",
    "tests/testfiles/Test-VersionShaDEVMeta.otf",
    "tests/testfiles/Test-VersionShaREL.otf",
    "tests/testfiles/Test-VersionShaRELMeta.otf"
]

meta_testfiles_list = [
    "tests/testfiles/Test-VersionMeta.ttf",
    "tests/testfiles/Test-VersionMoreMeta.ttf",
    "tests/testfiles/Test-VersionMeta.otf",
    "tests/testfiles/Test-VersionMoreMeta.otf"
]

dev_testfiles_list = [
    "tests/testfiles/Test-VersionDEV.ttf",
    "tests/testfiles/Test-VersionDEVMeta.ttf",
    "tests/testfiles/Test-VersionShaDEV.ttf",
    "tests/testfiles/Test-VersionShaDEVMeta.ttf",
    "tests/testfiles/Test-VersionDEV.otf",
    "tests/testfiles/Test-VersionDEVMeta.otf",
    "tests/testfiles/Test-VersionShaDEV.otf",
    "tests/testfiles/Test-VersionShaDEVMeta.otf"
]

rel_testfiles_list = [
    "tests/testfiles/Test-VersionREL.ttf",
    "tests/testfiles/Test-VersionRELMeta.ttf",
    "tests/testfiles/Test-VersionShaREL.ttf",
    "tests/testfiles/Test-VersionShaRELMeta.ttf",
    "tests/testfiles/Test-VersionREL.otf",
    "tests/testfiles/Test-VersionRELMeta.otf",
    "tests/testfiles/Test-VersionShaREL.otf",
    "tests/testfiles/Test-VersionShaRELMeta.otf"
]

state_testfiles_list = [
    "tests/testfiles/Test-VersionSha.ttf",
    "tests/testfiles/Test-VersionShaMeta.ttf",
    "tests/testfiles/Test-VersionShaDEV.ttf",
    "tests/testfiles/Test-VersionShaREL.ttf",
    "tests/testfiles/Test-VersionShaDEVMeta.ttf",
    "tests/testfiles/Test-VersionShaRELMeta.ttf",
    "tests/testfiles/Test-VersionSha.otf",
    "tests/testfiles/Test-VersionShaMeta.otf",
    "tests/testfiles/Test-VersionShaDEV.otf",
    "tests/testfiles/Test-VersionShaREL.otf",
    "tests/testfiles/Test-VersionShaDEVMeta.otf",
    "tests/testfiles/Test-VersionShaRELMeta.otf"
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


@pytest.fixture(params=state_testfiles_list)
def statefonts(request):
    return request.param


# utilities for testing
def _test_hexadecimal_sha1_formatted_string_matches(needle):
    p = re.compile("""\[[(a-f|0-9)]{7,15}\]""")
    m = p.match(needle)
    if m is None:
        return False
    else:
        return True


def _test_hexadecimal_sha1_string_matches(needle):
    p = re.compile("""[(a-f|0-9)]{7,15}""")
    m = p.match(needle)
    if m is None:
        return False
    else:
        return True


def _get_mock_missing_nameid5_ttfont(filepath):
    ttf = TTFont(filepath)
    record_list = []
    for record in ttf['name'].names:
        if record.nameID == 5:
            pass
        else:
            record_list.append(record)
    ttf['name'].names = record_list

    return ttf


# TESTS

#
#
#   BEGIN FontVersion INSTANTIATION TESTS
#
#

def test_libfv_missing_file_read_attempt():
    with pytest.raises(IOError):
        fv = FontVersion("tests/testfiles/bogus.ttf")


def test_libfv_nonfont_file_read_attempt():
    with pytest.raises(TTLibError):
        fv = FontVersion("tests/testfiles/test.txt")


def test_libfv_mocked_missing_name_tables_attempt():
    with pytest.raises(IndexError):
        ttf = _get_mock_missing_nameid5_ttfont("tests/testfiles/Test-VersionOnly.ttf")
        fv = FontVersion(ttf)


def test_libfv_fontversion_obj_instantiation_with_filepath_string(allfonts):
    fv = FontVersion(allfonts)


def test_libfv_fontversion_obj_instantiation_with_ttfont_object(allfonts):
    ttf = TTFont(allfonts)
    fv1 = FontVersion(ttf)
    fv2 = FontVersion(allfonts)
    assert fv1.fontpath == fv2.fontpath
    assert fv1.version_string_parts == fv2.version_string_parts
    assert fv1.develop_string == fv2.develop_string
    assert fv1.release_string == fv2.release_string
    assert fv1.sha1_develop == fv2.sha1_develop
    assert fv1.sha1_release == fv2.sha1_release
    assert fv1.version == fv2.version
    assert fv1.metadata == fv2.metadata
    assert fv1.contains_status == fv2.contains_status
    assert fv1.contains_metadata == fv2.contains_metadata
    assert fv1.is_release == fv2.is_release
    assert fv1.is_development == fv2.is_development


def test_libfv_version_string_property_set_on_instantiation(allfonts):
    fv = FontVersion(allfonts)
    assert fv.version == "Version 1.010"


def test_libfv_version_string_property_set_on_instantiation_ttfont_object(allfonts):
    ttf = TTFont(allfonts)
    fv = FontVersion(ttf)
    assert fv.version == "Version 1.010"


def test_libfv_head_fontrevision_property_set_on_instantiation(allfonts):
    fv = FontVersion(allfonts)
    assert fv.head_fontRevision == 1.010


def test_libfv_head_fontrevision_property_set_on_instantiation_ttfont_object(allfonts):
    ttf = TTFont(allfonts)
    fv = FontVersion(ttf)
    assert fv.head_fontRevision == 1.010


def test_libfv_fontversion_object_parameter_properties_defaults(allfonts):
    fv = FontVersion(allfonts)
    assert fv.develop_string == "DEV"
    assert fv.release_string == "RELEASE"
    assert fv.sha1_develop == "-dev"
    assert fv.sha1_release == "-release"


def test_libfv_fontversion_object_parameter_properties_defaults_ttfont_object(allfonts):
    ttf = TTFont(allfonts)
    fv = FontVersion(ttf)
    assert fv.develop_string == "DEV"
    assert fv.release_string == "RELEASE"
    assert fv.sha1_develop == "-dev"
    assert fv.sha1_release == "-release"


def test_libfv_fontversion_object_properties_truth_defaults():
    fv1 = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    fv2 = FontVersion("tests/testfiles/Test-VersionOnly.otf")
    assert fv1.contains_metadata is False
    assert fv1.contains_status is False
    assert fv1.is_development is False
    assert fv1.is_release is False

    assert fv2.contains_metadata is False
    assert fv2.contains_status is False
    assert fv2.is_development is False
    assert fv2.is_release is False


def test_libfv_fontversion_object_properties_truth_defaults_ttfont_object():
    ttf1 = TTFont("tests/testfiles/Test-VersionOnly.ttf")
    fv1 = FontVersion(ttf1)
    ttf2 = TTFont("tests/testfiles/Test-VersionOnly.otf")
    fv2 = FontVersion(ttf2)

    assert fv1.contains_metadata is False
    assert fv1.contains_status is False
    assert fv1.is_development is False
    assert fv1.is_release is False

    assert fv2.contains_metadata is False
    assert fv2.contains_status is False
    assert fv2.is_development is False
    assert fv2.is_release is False


def test_libfv_fontversion_object_properties_truth_defaults_with_metaonly(metafonts):
    fv = FontVersion(metafonts)
    assert fv.contains_metadata is True
    assert fv.contains_status is False
    assert fv.is_development is False
    assert fv.is_release is False


def test_libfv_fontversion_object_properties_truth_defaults_with_metaonly_ttfont_object(metafonts):
    ttf = TTFont(metafonts)
    fv = FontVersion(ttf)
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


def test_libfv_fontversion_object_properties_truth_development_ttfont_object(devfonts):
    ttf = TTFont(devfonts)
    fv = FontVersion(ttf)
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


def test_libfv_fontversion_object_properties_truth_release_ttfont_object(relfonts):
    ttf = TTFont(relfonts)
    fv = FontVersion(ttf)
    assert fv.contains_metadata is True
    assert fv.contains_status is True
    assert fv.is_development is False
    assert fv.is_release is True


def test_libfv_fontversion_object_properties_truth_sha(statefonts):
    fv = FontVersion(statefonts)
    assert fv.contains_state is True
    assert len(fv.state) > 0


def test_libfv_fontversion_object_properties_truth_sha_ttfont_object(statefonts):
    ttf = TTFont(statefonts)
    fv = FontVersion(ttf)
    assert fv.contains_state is True
    assert len(fv.state) > 0


def test_libfv_fontversion_object_properties_truth_state_versionstring_only():
    fv1 = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    fv2 = FontVersion("tests/testfiles/Test-VersionOnly.otf")

    assert fv1.contains_state is False
    assert fv2.contains_state is False

    assert len(fv1.state) == 0
    assert len(fv2.state) == 0


def test_libfv_fontversion_object_properties_truth_state_meta_without_state():
    fv1 = FontVersion("tests/testfiles/Test-VersionMeta.ttf")
    fv2 = FontVersion("tests/testfiles/Test-VersionMeta.otf")
    fv3 = FontVersion("tests/testfiles/Test-VersionMoreMeta.ttf")
    fv4 = FontVersion("tests/testfiles/Test-VersionMoreMeta.otf")

    assert fv1.contains_state is False
    assert fv2.contains_state is False
    assert fv3.contains_state is False
    assert fv4.contains_state is False

    assert len(fv1.state) == 0
    assert len(fv2.state) == 0
    assert len(fv3.state) == 0
    assert len(fv4.state) == 0


def test_libfv_fontversion_object_versionparts_meta_lists_versionstring_only():
    fv1 = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    fv2 = FontVersion("tests/testfiles/Test-VersionOnly.otf")

    assert len(fv1.version_string_parts) == 1
    assert len(fv1.metadata) == 0

    assert len(fv2.version_string_parts) == 1
    assert len(fv2.metadata) == 0


def test_libfv_fontversion_object_versionparts_meta_lists_versionstring_only_ttfont_object():
    ttf1 = TTFont("tests/testfiles/Test-VersionOnly.ttf")
    fv1 = FontVersion(ttf1)
    ttf2 = TTFont("tests/testfiles/Test-VersionOnly.otf")
    fv2 = FontVersion(ttf2)

    assert len(fv1.version_string_parts) == 1
    assert len(fv1.metadata) == 0

    assert len(fv2.version_string_parts) == 1
    assert len(fv2.metadata) == 0


def test_libfv_fontversion_object_versionparts_meta_lists_version_with_onemeta():
    fv1 = FontVersion("tests/testfiles/Test-VersionMeta.ttf")
    assert len(fv1.version_string_parts) == 2
    assert fv1.version_string_parts[0] == "Version 1.010"
    assert fv1.version_string_parts[1] == "metadata string"
    assert len(fv1.metadata) == 1
    assert fv1.metadata[0] == "metadata string"

    fv2 = FontVersion("tests/testfiles/Test-VersionMeta.otf")
    assert len(fv2.version_string_parts) == 2
    assert fv2.version_string_parts[0] == "Version 1.010"
    assert fv2.version_string_parts[1] == "metadata string"
    assert len(fv2.metadata) == 1
    assert fv2.metadata[0] == "metadata string"


def test_libfv_fontversion_object_versionparts_meta_lists_version_with_onemeta_ttfont_object():
    ttf1 = TTFont("tests/testfiles/Test-VersionMeta.ttf")

    fv1 = FontVersion(ttf1)
    assert len(fv1.version_string_parts) == 2
    assert fv1.version_string_parts[0] == "Version 1.010"
    assert fv1.version_string_parts[1] == "metadata string"
    assert len(fv1.metadata) == 1
    assert fv1.metadata[0] == "metadata string"

    ttf2 = TTFont("tests/testfiles/Test-VersionMeta.otf")

    fv2 = FontVersion(ttf2)
    assert len(fv2.version_string_parts) == 2
    assert fv2.version_string_parts[0] == "Version 1.010"
    assert fv2.version_string_parts[1] == "metadata string"
    assert len(fv2.metadata) == 1
    assert fv2.metadata[0] == "metadata string"


def test_libfv_fontversion_object_versionparts_meta_lists_version_with_twometa():
    fv = FontVersion("tests/testfiles/Test-VersionMoreMeta.ttf")
    assert len(fv.version_string_parts) == 3
    assert fv.version_string_parts[0] == "Version 1.010"
    assert fv.version_string_parts[1] == "metadata string"
    assert fv.version_string_parts[2] == "another metadata string"
    assert len(fv.metadata) == 2
    assert fv.metadata[0] == "metadata string"
    assert fv.metadata[1] == "another metadata string"

    fv2 = FontVersion("tests/testfiles/Test-VersionMoreMeta.otf")
    assert len(fv2.version_string_parts) == 3
    assert fv2.version_string_parts[0] == "Version 1.010"
    assert fv2.version_string_parts[1] == "metadata string"
    assert fv2.version_string_parts[2] == "another metadata string"
    assert len(fv2.metadata) == 2
    assert fv2.metadata[0] == "metadata string"
    assert fv2.metadata[1] == "another metadata string"


def test_libfv_fontversion_object_versionparts_meta_lists_version_with_twometa_ttfont_object():
    ttf1 = TTFont("tests/testfiles/Test-VersionMoreMeta.ttf")

    fv1 = FontVersion(ttf1)
    assert len(fv1.version_string_parts) == 3
    assert fv1.version_string_parts[0] == "Version 1.010"
    assert fv1.version_string_parts[1] == "metadata string"
    assert fv1.version_string_parts[2] == "another metadata string"
    assert len(fv1.metadata) == 2
    assert fv1.metadata[0] == "metadata string"
    assert fv1.metadata[1] == "another metadata string"

    ttf2 = TTFont("tests/testfiles/Test-VersionMoreMeta.otf")

    fv2 = FontVersion(ttf2)
    assert len(fv2.version_string_parts) == 3
    assert fv2.version_string_parts[0] == "Version 1.010"
    assert fv2.version_string_parts[1] == "metadata string"
    assert fv2.version_string_parts[2] == "another metadata string"
    assert len(fv2.metadata) == 2
    assert fv2.metadata[0] == "metadata string"
    assert fv2.metadata[1] == "another metadata string"


#
#
#   END FontVersion INSTANTIATION TESTS
#
#

#
#
#  BEGIN FontVersion METHOD TESTS
#
#

def test_libfv_fontversion_object_str_method(allfonts):
    fv = FontVersion(allfonts)
    test_string = fv.__str__()
    assert test_string.startswith("<fontv.libfv.FontVersion> ") is True
    assert fv.get_version_string() in test_string
    assert fv.fontpath in test_string


def test_libfv_fontversion_object_equality(allfonts):
    fv1 = FontVersion(allfonts)
    fv2 = FontVersion(allfonts)
    fv3 = FontVersion(allfonts)
    fv3.version_string_parts[0] = "Version 12.000"
    assert fv1 == fv2
    assert (fv1 == fv3) is False
    assert (fv1 == "test string") is False
    assert (fv1 == fv1.version_string_parts) is False


def test_libfv_fontversion_object_inequality(allfonts):
    fv1 = FontVersion(allfonts)
    fv2 = FontVersion(allfonts)
    fv3 = FontVersion(allfonts)
    fv3.version_string_parts[0] = "Version 12.000"
    assert (fv1 != fv2) is False
    assert fv1 != fv3
    assert fv1 != "test string"
    assert fv1 != fv1.version_string_parts


def test_libfv_clear_metadata_method(allfonts):
    fv = FontVersion(allfonts)
    fv.clear_metadata()
    assert len(fv.version_string_parts) == 1
    assert fv.version_string_parts[0] == "Version 1.010"


def test_libfv_get_head_fontrevision_method(allfonts):
    fv = FontVersion(allfonts)
    assert fv.get_head_fontrevision_version_number() == 1.010


def test_libfv_get_metadata_method():
    fv1 = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    fv2 = FontVersion("tests/testfiles/Test-VersionMeta.ttf")
    fv3 = FontVersion("tests/testfiles/Test-VersionMoreMeta.ttf")
    assert fv1.get_metadata_list() == []
    assert fv2.get_metadata_list() == ["metadata string"]
    assert fv3.get_metadata_list() == ["metadata string", "another metadata string"]

    fv4 = FontVersion("tests/testfiles/Test-VersionOnly.otf")
    fv5 = FontVersion("tests/testfiles/Test-VersionMeta.otf")
    fv6 = FontVersion("tests/testfiles/Test-VersionMoreMeta.otf")
    assert fv4.get_metadata_list() == []
    assert fv5.get_metadata_list() == ["metadata string"]
    assert fv6.get_metadata_list() == ["metadata string", "another metadata string"]


def test_libfv_get_status_method_onlyversion():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    status_string = fv.get_state_status_substring()
    assert status_string == ""


def test_libfv_get_status_method_development(devfonts):
    fv = FontVersion(devfonts)
    status_string = fv.get_state_status_substring()
    assert status_string == fv.version_string_parts[1]


def test_libfv_get_status_method_release(relfonts):
    fv = FontVersion(relfonts)
    status_string = fv.get_state_status_substring()
    assert status_string == fv.version_string_parts[1]


def test_libfv_get_status_method_nostatus(metafonts):
    fv = FontVersion(metafonts)
    status_string = fv.get_state_status_substring()
    assert status_string == ""


def test_libfv_is_state_substring_return_match_valid():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")

    is_state_substring, state_substring = fv._is_state_substring_return_state_match("[abcd123]")
    assert is_state_substring is True
    assert state_substring == "abcd123"

    is_state_substring, state_substring = fv._is_state_substring_return_state_match("[abcd123]-dev")
    assert is_state_substring is True
    assert state_substring == "abcd123"

    is_state_substring, state_substring = fv._is_state_substring_return_state_match("[abcd123]-release")
    assert is_state_substring is True
    assert state_substring == "abcd123"


def test_libfv_is_state_substring_return_match_invalid():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")

    is_state_substring, state_substring = fv._is_state_substring_return_state_match("abcd123")
    assert is_state_substring is False
    assert state_substring == ""

    is_state_substring, state_substring = fv._is_state_substring_return_state_match("{abcd123}")
    assert is_state_substring is False
    assert state_substring == ""

    is_state_substring, state_substring = fv._is_state_substring_return_state_match("[&%$#@!]")
    assert is_state_substring is False
    assert state_substring == ""


def test_libfv_get_version_number_tuple():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    assert fv.get_version_number_tuple() == (1, 0, 1, 0)

    # mock new version numbers in memory and confirm that they are correct in tuples
    fv.version = "Version 1.1"
    assert fv.get_version_number_tuple() == (1, 1)
    fv.version = "Version 1.01"
    assert fv.get_version_number_tuple() == (1, 0, 1)
    fv.version = "Version 1.001"
    assert fv.get_version_number_tuple() == (1, 0, 0, 1)
    fv.version = "Version 10.1"
    assert fv.get_version_number_tuple() == (10, 1)
    fv.version = "Version 10.01"
    assert fv.get_version_number_tuple() == (10, 0, 1)
    fv.version = "Version 10.001"
    assert fv.get_version_number_tuple() == (10, 0, 0, 1)
    fv.version = "Version 100.001"
    assert fv.get_version_number_tuple() == (100, 0, 0, 1)


def test_libfv_get_version_number_tuple_bad_version_number():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    assert fv.get_version_number_tuple() == (1, 0, 1, 0)

    # mock a bad version number substring
    fv.set_version_number("x.xxx")
    response = fv.get_version_number_tuple()
    assert response is None


def test_libfv_get_version_string_method():
    fv1 = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    fv2 = FontVersion("tests/testfiles/Test-VersionMeta.ttf")
    fv3 = FontVersion("tests/testfiles/Test-VersionMoreMeta.ttf")
    assert fv1.get_version_string() == "Version 1.010"
    assert fv2.get_version_string() == "Version 1.010;metadata string"
    assert fv3.get_version_string() == "Version 1.010;metadata string;another metadata string"

    fv4 = FontVersion("tests/testfiles/Test-VersionOnly.otf")
    fv5 = FontVersion("tests/testfiles/Test-VersionMeta.otf")
    fv6 = FontVersion("tests/testfiles/Test-VersionMoreMeta.otf")
    assert fv4.get_version_string() == "Version 1.010"
    assert fv5.get_version_string() == "Version 1.010;metadata string"
    assert fv6.get_version_string() == "Version 1.010;metadata string;another metadata string"


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

    fv2 = FontVersion("tests/testfiles/Test-VersionOnly.otf")
    assert len(fv2.version_string_parts) == 1
    fv2.set_development_status()
    assert len(fv2.version_string_parts) == 2
    assert fv2.version_string_parts[0] == "Version 1.010"
    assert fv2.version_string_parts[1] == "DEV"
    assert fv2.is_development is True
    assert fv2.is_release is False
    assert fv2.contains_status is True
    assert fv2.contains_metadata is True


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

    fv2 = FontVersion("tests/testfiles/Test-VersionOnly.otf")
    assert len(fv2.version_string_parts) == 1
    fv2.set_release_status()
    assert len(fv2.version_string_parts) == 2
    assert fv2.version_string_parts[0] == "Version 1.010"
    assert fv2.version_string_parts[1] == "RELEASE"
    assert fv2.is_development is False
    assert fv2.is_release is True
    assert fv2.contains_status is True
    assert fv2.contains_metadata is True


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
        fv.set_state_git_commit_sha1(development=True, release=True)


def test_libfv_set_default_gitsha1_method(allfonts):
    fv = FontVersion(allfonts)
    fv.set_state_git_commit_sha1()
    sha_needle = fv.version_string_parts[1]
    assert _test_hexadecimal_sha1_formatted_string_matches(sha_needle) is True  # confirm that set with state label
    assert _test_hexadecimal_sha1_string_matches(fv.state) is True  # confirm that state property is properly set
    assert ("-dev" in sha_needle) is False
    assert ("-release" in sha_needle) is False
    assert ("DEV" in sha_needle) is False
    assert ("RELEASE" in sha_needle) is False


def test_libfv_set_development_gitsha1_method(allfonts):
    fv = FontVersion(allfonts)
    fv.set_state_git_commit_sha1(development=True)
    sha_needle = fv.version_string_parts[1]
    assert _test_hexadecimal_sha1_formatted_string_matches(sha_needle) is True  # confirm that set with state label
    assert _test_hexadecimal_sha1_string_matches(fv.state) is True  # confirm that state property is properly set
    assert ("-dev" in sha_needle) is True
    assert ("-release" in sha_needle) is False
    assert ("DEV" in sha_needle) is False
    assert ("RELEASE" in sha_needle) is False


def test_libfv_set_release_gitsha1_method(allfonts):
    fv = FontVersion(allfonts)
    fv.set_state_git_commit_sha1(release=True)
    sha_needle = fv.version_string_parts[1]
    assert _test_hexadecimal_sha1_formatted_string_matches(sha_needle) is True  # confirm that set with state label
    assert _test_hexadecimal_sha1_string_matches(fv.state) is True  # confirm that state property is properly set
    assert ("-dev" in sha_needle) is False
    assert ("-release" in sha_needle) is True
    assert ("DEV" in sha_needle) is False
    assert ("RELEASE" in sha_needle) is False


def test_libfv_set_gitsha1_both_dev_release_error(capsys):
    fv = FontVersion("tests/testfiles/Test-VersionMeta.ttf")
    with pytest.raises(ValueError) as pytest_wrapped_e:
        fv.set_state_git_commit_sha1(release=True, development=True)

    out, err = capsys.readouterr()
    assert pytest_wrapped_e.type == ValueError


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

    fv2 = FontVersion("tests/testfiles/Test-VersionOnly.otf")
    fv2.set_version_string("Version 2.000")
    assert len(fv2.version_string_parts) == 1
    assert fv2.version_string_parts[0] == "Version 2.000"


def test_libfv_set_version_string_two_substrings():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    fv.set_version_string("Version 2.000;DEV")
    assert len(fv.version_string_parts) == 2
    assert fv.version_string_parts[0] == "Version 2.000"
    assert fv.version_string_parts[1] == "DEV"

    fv2 = FontVersion("tests/testfiles/Test-VersionOnly.otf")
    fv2.set_version_string("Version 2.000;DEV")
    assert len(fv2.version_string_parts) == 2
    assert fv2.version_string_parts[0] == "Version 2.000"
    assert fv2.version_string_parts[1] == "DEV"


def test_libfv_set_version_string_three_substrings():
    fv = FontVersion("tests/testfiles/Test-VersionOnly.ttf")
    fv.set_version_string("Version 2.000;DEV;other stuff")
    assert len(fv.version_string_parts) == 3
    assert fv.version_string_parts[0] == "Version 2.000"
    assert fv.version_string_parts[1] == "DEV"
    assert fv.version_string_parts[2] == "other stuff"

    fv2 = FontVersion("tests/testfiles/Test-VersionOnly.otf")
    fv2.set_version_string("Version 2.000;DEV;other stuff")
    assert len(fv2.version_string_parts) == 3
    assert fv2.version_string_parts[0] == "Version 2.000"
    assert fv2.version_string_parts[1] == "DEV"
    assert fv2.version_string_parts[2] == "other stuff"


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


def test_libfv_write_version_string_method_ttfont_object(allfonts):
    temp_out_file_path = os.path.join("tests", "testfiles", "Test-Temp.ttf")  # temp file write path
    ttf = TTFont(allfonts)
    fv = FontVersion(ttf)
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

