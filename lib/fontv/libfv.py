#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ========================================================================================
#
#  libfv.py
#   A Python library module that supports read/modification/write of font version strings
#
#  Copyright 2017 Christopher Simpkins
#  MIT License
#
# ========================================================================================

from __future__ import unicode_literals

import os

from fontTools import ttLib
from fontTools.misc.py23 import tounicode, unicode
from git import Repo

from fontv.utilities import get_git_root_path


class FontVersion(object):
    """
    FontVersion is a ttf and otf font version string object that maintains version string state in memory, parses
    semicolon delimited parts of version strings included in binary files, and provides public methods for version
    string reads/writes.
    :raises: fontTools.ttLib.TTLibError if fontpath is not a ttf or otf font
    :raises: IOError if fontpath does not exist
    """
    def __init__(self, fontpath, develop="DEV", release="RELEASE", sha1_develop="-dev", sha1_release="-release"):
        self.fontpath = fontpath
        self.develop_string = develop
        self.release_string = release
        self.sha1_develop = sha1_develop
        self.sha1_release = sha1_release

        # fonttools TTFont for font on self.fontpath
        # raises IOError if filepath does not exist
        # raises fontTools.ttLib.TTLibError if fontpath is not a ttf or otf font
        self.ttf = ttLib.TTFont(self.fontpath)

        # data containers
        self._nameID_5_dict = {}
        self.version_string_parts = []
        self.version = ""
        self.status = ""
        self.metadata = []

        # truth test values for string contents
        self.contains_metadata = False
        self.contains_status = False
        self.is_development = False
        self.is_release = False

        # object instantiation methods
        self._read_version_string()  # read version string on fontpath at object instantiation

    def _read_version_string(self):
        """
        _read_version_string is a private method that reads OpenType name table ID 5 data from otf and ttf fonts
        and sets FontVersion object properties.  The method is called on instantiation of a FontVersion
        object
        :return: None
        """

        namerecord_list = self.ttf['name'].names
        # read in name records
        for record in namerecord_list:
            if record.nameID == 5:
                # map dictionary as {(platformID, platEncID, langID) : version string}
                recordkey = (record.platformID, record.platEncID, record.langID)
                self._nameID_5_dict[recordkey] = record.toUnicode()

        # begin parsing of the version string
        if (3, 1, 1033) in self._nameID_5_dict:
            version_string = self._nameID_5_dict[(3, 1, 1033)]
        elif (1, 0, 0) in self._nameID_5_dict:
            version_string = self._nameID_5_dict[(1, 0, 0)]
        else:
            version_string = ""  # TODO: raise exception?

        # parse version string into substrings
        self._parse_version_substrings(version_string)

        # define version as first substring
        self.version = self.version_string_parts[0]

        # metadata parsing
        self._parse_metadata()         # parse the metadata
        self._parse_status()           # parse the version substring dev/rel status indicator

    def _get_repo_commit(self):
        repo = Repo(get_git_root_path(self.fontpath))
        gitpy = repo.git
        # git rev-list --abbrev-commit --max-count=1 --format="%h" HEAD - abbreviated unique sha1 for the repository
        # number of sha1 hex characters determined by git (addresses https://github.com/source-foundry/font-v/issues/2)
        full_git_sha_string = gitpy.rev_list('--abbrev-commit', '--max-count=1', '--format="%h"', 'HEAD')
        unicode_full_sha_string = tounicode(full_git_sha_string)
        sha_string_list = unicode_full_sha_string.split("\n")
        final_sha_string = sha_string_list[1].replace('"', '')
        return final_sha_string

    def _parse_metadata(self):
        """
        _parse_metadata is a private method that parses a font version string for semicolon delimited font version
        string metadata.  Metadata are defined as anything beyond the first substring component of a version string
        that is defined to include the word 'Version' followed by the version number and semicolon
        :return: None
        """
        if len(self.version_string_parts) > 1:
            self.contains_metadata = True  # set to True if there are > 1 sub strings as others are defined as metadata
            self.metadata = []             # reset to empty and allow following code to define the list items
            for metadata_item in self.version_string_parts[1:]:
                self.metadata.append(metadata_item)
        else:
            self.metadata = []
            self.contains_metadata = False

    def _parse_status(self):
        """
        _parse_status is a private method that parses a font version string to determine if it contains
        substring labels that indicate development/release status of the font based.  It is called
        by the _read_version_string method on FontVersion instantiation.
        :return: None
        """
        if len(self.version_string_parts) > 1:
            status_needle = self.version_string_parts[1]  # define as the second substring in the version string
            self.contains_status = False  # reset each time there is a parse attempt and let logic below define
            self.status = ""  # reset each time there is a parse attempt and let logic below define

            if self._is_development_substring(status_needle):
                self.contains_status = True
                self.is_development = True
                self.status = status_needle
            else:
                self.is_development = False

            if self._is_release_substring(status_needle):
                self.contains_status = True
                self.is_release = True
                self.status = status_needle
            else:
                self.is_release = False
        else:
            self.contains_status = False
            self.is_development = False
            self.is_release = False
            self.status = ""

    def _parse_version_substrings(self, version_string):
        # split semicolon delimited list of version substrings
        if ";" in version_string:
            self.version_string_parts = version_string.split(";")
        else:
            self.version_string_parts = [version_string]

    def _set_status_indicator_string(self, status_string):
        if len(self.version_string_parts) > 1:
            teststring = self.version_string_parts[1]
            if self._is_release_substring(teststring) or self._is_development_substring(teststring):
                # directly replace when existing status substring
                self.version_string_parts[1] = status_string
            else:
                # if the second item of the substring list is not a status string, save it and all subsequent list items
                # then create a new list with inserted status string value
                self.version_string_parts = [self.version_string_parts[0]]  # redefine list as list with version number
                self.version_string_parts.append(status_string)       # define the status substring as next item
                for item in self.metadata:  # iterate through all previous metadata substrings and append to list
                    self.version_string_parts.append(item)
        else:
            # if the version string is defined as only a version number substring (i.e. list size = 1),
            # write the new status substring to the list.  Nothing else required
            self.version_string_parts.append(status_string)

        # update FontVersion truth testing properties based upon the new data
        self._parse_status()
        self._parse_metadata()

    def _is_development_substring(self, needle):
        if self.develop_string == needle.strip() or self.sha1_develop in needle:
            return True
        else:
            return False

    def _is_release_substring(self, needle):
        if self.release_string == needle.strip() or self.sha1_release in needle:
            return True
        else:
            return False

    def clear_metadata(self):
        """
        clear_metadata is a public method that clears all version string metadata in memory.  This results in the font
        version number substring as the only in memory component of the original (i.e. what was read from font binary)
        or modified (during execution of FontVersion methods or modification of object properties) version string.  The
        intent is to support removal of unnecessary version string data that is included in the font binary.
        :return: None
        """
        self.version_string_parts = [self.version_string_parts[0]]
        self._parse_metadata()
        self._parse_status()

    def get_version_string(self):
        """
        get_version_string is a public method that returns the full version string as the joined contents of the
        FontVersion.version_string_parts Python list.  It is joined with semicolon delimiters and returned as a
        Python 2 unicode object or Python 3 string object based upon the interpreter in use
        :return: string (Python 3) or unicode (Python 2)
        """
        return ";".join(self.version_string_parts)

    def set_git_commit_sha1(self, development=False, release=False):
        """
        set_git_commit_sha1 is a public method that adds a git commit sha1 hash label to the font version string
        at the second substring position.  This can be combined with a development/release status indicator as part
        of the substring if the calling code defines either the development or release parameter to a value of True.
        Note that development and release are mutually exclusive.  ValueError is raised if both are set to True.
        :param development: (boolean) False (default) = do not add development status indicator; True = add indicator
        :param release: (boolean) False (default) = do not add release status indicator; True = add indicator
        :raises: IOError when the git repository root cannot be identified using the directory traversal in the
                 fontv.utilities.get_git_root_path() function
        :raises: ValueError when calling code sets both development and release parameters to True as these are
                 mutually exclusive requests
        :return: None
        """
        git_sha1_hash = self._get_repo_commit()

        if development and release:
            raise ValueError("Cannot set both development parameter and release parameter to a value of True in "
                             "fontv.libfv.FontVersion.set_git_commit_sha1() method.  These are mutually exclusive.")

        if development:   # if request for development status label, append FontVersion.sha1_develop to hash digest
            hash_substring = git_sha1_hash + self.sha1_develop
        elif release:     # if request for release status label, append FontVersion.sha1_release to hash digest
            hash_substring = git_sha1_hash + self.sha1_release
        else:             # else just use the hash digest
            hash_substring = git_sha1_hash

        self._set_status_indicator_string(hash_substring)

    def set_development_status(self):
        """
        set_development_status is a public method that sets the in memory development status label for the font
        :return: None
        """
        self._set_status_indicator_string(self.develop_string)

    def set_release_status(self):
        """
        set_release_status is a public method that sets the in memory release status label for the font.
        :return:
        """
        self._set_status_indicator_string(self.release_string)

    def set_version_number(self, version_number):
        """
        set_version_number is a public method that sets the version number substring with the version_number parameter
        :param version_number: (string) version number in X.XXX format where X are integers
        :return: None
        """
        version_number_substring = "Version " + version_number
        self.version_string_parts[0] = version_number_substring
        self.version = self.version_string_parts[0]

    def set_version_string(self, version_string):
        """
        set_version_string is a public method that sets the full version string with a version_string parameter.
        This is parsed to component substring parts in a semicolon delimited fashion and the full string is maintained
        in the FontVersion.version_substring_parts Python list
        :param version_string: (string) The full semicolon delimited (if necessary) version string
        :return: None
        """
        self._parse_version_substrings(version_string)
        self._parse_metadata()
        self._parse_status()

    def write_version_string(self, fontpath=None):
        """
        write_version_string is a public method that writes the in memory version substring parts as a joined, semicolon
        delimited string to the nameID 5 OpenType tables of the font file path that was set at FontVersion instantiation
        (default) or new fontpath if defined as parameter on method call.
        :param: fontpath (string): optional file path to write out modified font file
        :return: None
        """
        version_string = self.get_version_string()
        namerecord_list = self.ttf['name'].names
        for record in namerecord_list:
            if record.nameID == 5:
                # write to fonttools ttLib object name ID 5 table record for each one found in the font
                record.string = version_string
        # write changes out to the font binary path
        if fontpath is None:
            self.ttf.save(self.fontpath)
        else:
            self.ttf.save(fontpath)

