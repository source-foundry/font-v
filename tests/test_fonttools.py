#!/usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

import sys
import pytest

from fontTools.misc.py23 import unicode, tounicode, tobytes, tostr


def test_fontv_fonttools_lib_unicode():
    test_string = tobytes("hello")
    test_string_str = tostr("hello")
    test_string_unicode = tounicode(test_string, 'utf-8')
    test_string_str_unicode = tounicode(test_string_str, 'utf-8')

    assert (isinstance(test_string, unicode)) is False
    if sys.version_info[0] == 2:
        assert (isinstance(test_string_str, unicode)) is False     # str != unicode in Python 2
    elif sys.version_info[0] == 3:
        assert (isinstance(test_string_str, unicode)) is True      # str = unicode in Python 3
    assert (isinstance(test_string_unicode, unicode)) is True      # after cast with fonttools function, Py2+3 = unicode
    assert (isinstance(test_string_str_unicode, unicode)) is True  # ditto
    assert test_string_unicode == "hello"
