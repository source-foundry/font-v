#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest

from fontv.utilities import file_exists, dir_exists, get_git_root_path, is_font


def test_utilities_file_exists_function_passes():
    testfile = "tests/testfiles/Hack-Regular.ttf"
    assert file_exists(testfile) is True


def test_utilities_file_exists_function_fails():
    testfile = "tests/testfiles/bogus.in"
    assert file_exists(testfile) is False


def test_utilities_dir_exists_function_passes():
    testdir = "tests/testfiles"
    assert dir_exists(testdir) is True


def test_utilities_dir_exists_function_fails():
    testdir = "tests/bogus"
    assert dir_exists(testdir) is False


def test_utilities_get_gitrootpath_function_returns_proper_path_cwd():
    filepath = "CHANGELOG.md"
    gitdir_path = get_git_root_path(filepath)
    assert os.path.basename(gitdir_path) == "font-v"
    assert os.path.isdir(gitdir_path) is True


def test_utilities_get_gitrootpath_function_returns_proper_path_one_level_up():
    filepath = "tests/test_utilities.py"
    gitdir_path = get_git_root_path(filepath)
    assert os.path.basename(gitdir_path) == "font-v"
    assert os.path.isdir(gitdir_path) is True


def test_utilities_get_gitrootpath_function_returns_proper_path_two_levels_up():
    filepath = "tests/testfiles/Hack-Regular.ttf"
    gitdir_path = get_git_root_path(filepath)
    assert os.path.basename(gitdir_path) == "font-v"
    assert os.path.isdir(gitdir_path) is True


def test_utilities_get_gitrootpath_function_returns_proper_path_three_levels_up():
    filepath = "tests/testfiles/deepdir/test.txt"
    gitdir_path = get_git_root_path(filepath)
    assert os.path.basename(gitdir_path) == "font-v"
    assert os.path.isdir(gitdir_path) is True


def test_utilities_get_gitrootpath_function_raises_ioerror_six_levels_up():
    with pytest.raises(IOError):
        filepath = "tests/testfiles/deepdir/deepdir2/deepdir3/deepdir4/test.txt"
        get_git_root_path(filepath)


def test_utilities_is_font_ttf():
    assert is_font("Test-Regular.ttf") is True


def test_utilities_is_font_otf():
    assert is_font("Test-Regular.otf") is True


def test_utilities_is_font_long_ttf():
    assert is_font(os.path.join("tests", "deeper", "Test-Regular.ttf")) is True


def test_utilities_is_font_long_otf():
    assert is_font(os.path.join("tests", "deeper", "Test-Regular.otf")) is True


def test_utilities_is_font_badpath_no_extension():
    assert is_font("Test-Regular") is False


def test_utilities_is_font_badpath_bad_extension():
    assert is_font("Test-Regular.gif") is False


def test_utilities_is_font_badpath_too_short():
    assert is_font(".ttf") is False
