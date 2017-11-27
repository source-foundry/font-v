#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fontv.settings import lib_name, major_version, minor_version, patch_version, HELP, VERSION, USAGE

import pytest


def test_settings_lib_name():
    assert lib_name == "font-v"


def test_settings_major_version():
    assert len(major_version) > 0


def test_settings_minor_version():
    assert len(minor_version) > 0


def test_settings_patch_version():
    assert len(patch_version) > 0


def test_settings_help_string():
    assert len(HELP) > 0


def test_settings_version_string():
    assert len(VERSION) > 0


def test_settings_usage_string():
    assert len(USAGE) > 0

