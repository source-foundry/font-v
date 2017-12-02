#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ====================================================
# Copyright 2017 Christopher Simpkins
# MIT License
# ====================================================

from __future__ import unicode_literals

import os
import sys

from fontTools import ttLib
from fontTools.misc.py23 import tounicode, unicode
from fontTools.misc.encodingTools import getEncoding
from git import Repo

from fontv import settings
from fontv.commandlines import Command
from fontv.utilities import file_exists, dir_exists


def main():
    c = Command()

    if c.does_not_validate_missing_args():
        sys.stderr.write("[font-v] ERROR: Please include a subcommand and appropriate optional arguments in "
                         "your command." + os.linesep)
        sys.exit(1)

    if c.is_help_request():
        print(settings.HELP)
        sys.exit(0)
    elif c.is_version_request():
        print(settings.VERSION)
        sys.exit(0)
    elif c.is_usage_request():
        print(settings.USAGE)
        sys.exit(0)

    if c.subcmd == "report":
        # argument test
        if c.argc < 2:
            sys.stderr.write("[font-v] ERROR: Command is missing necessary arguments. Check "
                             "`font-v --help`." + os.linesep)
            sys.exit(1)

        for arg in c.argv[1:]:
            if arg[-4:].lower() == ".ttf" or arg[-4:].lower() == ".otf":
                font_path = arg
                if file_exists(font_path):
                    tt = ttLib.TTFont(font_path)
                    namerecord_list = tt['name'].names
                    for record in namerecord_list:
                        if record.nameID == 5:
                            fobj = FontVersionObj(font_path, record)
                            if "--dev" in c.argv:   # --dev flag prints every version string in name records
                                print(fobj.get_dev_print_string())
                            else:
                                print(fobj.get_print_string())
                                break  # print a single version string if there are multiple name records by default
                else:
                    print("[font-v] ERROR: " + font_path + " does not appear to be a valid ttf or otf font file path.")
                    sys.exit(1)
    elif c.subcmd == "write":
        # argument test
        if c.argc < 2:
            sys.stderr.write("[font-v] ERROR: Command is missing necessary arguments. "
                             "Check `font-v --help`." + os.linesep)
            sys.exit(1)

        # argument parsing flags
        add_sha1 = False
        add_release_string = False
        add_dev_string = False
        add_new_version = False
        fontpath_list = []            # list of font paths that user submits on command line
        version = ""

        # test for mutually exclusive arguments
        # do not refactor this below the level of the argument tests that follow
        if "--rel" in c.argv and "--dev" in c.argv:
            sys.stderr.write("[font-v] ERROR: Please use either --dev or --rel argument, not both." + os.linesep)
            sys.exit(1)

        # test arguments
        for arg in c.argv[1:]:
            if arg == "--sha1":
                add_sha1 = True
            elif arg == "--rel":
                add_release_string = True
            elif arg == "--dev":
                add_dev_string = True
            elif arg[0:6] == "--ver=":
                add_new_version = True
                version_list = arg.split("=")  # split on the = symbol and use second part as definition
                if len(version_list) < 2:
                    sys.stderr.write("[font-v] ERROR: --arg=version argument is not properly specified." + os.linesep)
                    sys.exit(1)
                # use fonttools library to cast terminal input from user to fontTools.misc.py23.unicode type (imported)
                # this will be Python 3 str object and Python 2 unicode object
                # try to cast to this type and catch decoding exceptions, handle with error message to user.
                try:
                    version_pre = tounicode(version_list[1], encoding='ascii')
                except UnicodeDecodeError as e:
                    sys.stderr.write("[font-v] ERROR: You appear to have entered a non ASCII character in your"
                                     "version string.  Please try again." + os.linesep)
                    sys.stderr.write("[fontTools library]: error message: " + str(e))
                    sys.exit(1)

                version_pre = version_pre.replace("-", ".")   # specified on command line as 1-000
                version_final = version_pre.replace("_", ".")   # or as 1_000
                version = "Version " + version_final
            elif len(arg) > 4 and (arg[-4:].lower() == ".ttf" or arg[-4:].lower() == ".otf"):
                if file_exists(arg):
                    fontpath_list.append(arg)
                else:
                    sys.stderr.write("[font-v] ERROR: " + arg + " does not appear to be a valid "
                                     "font file path." + os.linesep)
                    sys.exit(1)

        if add_sha1 is False and add_release_string is False and add_dev_string is False and add_new_version is False:
            print("[font-v]  No changes specified.  Nothing to do.")
            sys.exit(0)

        for fontpath in fontpath_list:
            tt = ttLib.TTFont(fontpath)
            namerecord_list = tt['name'].names
            for record in namerecord_list:
                if record.nameID == 5:
                    fvo = FontVersionObj(fontpath, record)

                    if add_new_version is True:
                        version_string = version
                    else:
                        version_string = fvo.get_version_string()

                    if add_sha1 is True:
                        sha_string = "; " + fvo.get_repo_commit()
                        version_string += sha_string

                    if add_release_string is True:
                        if add_sha1 is True:
                            version_string += "-release"
                        else:
                            version_string += "; RELEASE"
                    elif add_dev_string is True:
                        if add_sha1 is True:
                            version_string += "-dev"
                        else:
                            version_string += "; DEV"

                    post_string = fvo.get_post_string()
                    if len(post_string) > 0:
                        post_string_add = ";" + post_string
                        version_string += post_string_add
                    # write to fonttools ttLib object name table record
                    record.string = version_string
            # then write out the name table modifications to the font binary
            tt.save(fontpath)
            print("[✓] " + fontpath + " version string was successfully changed "
                  "to:" + os.linesep + version_string + os.linesep)
    else:  # user did not enter an acceptable subcommand
        sys.stderr.write("[font-v] ERROR: Please enter a font-v subcommand with your request." + os.linesep)
        sys.exit(1)


class FontVersionObj(object):
    def __init__(self, font_path, name_id5_record):
        self.fontpath = font_path
        self.platformID = name_id5_record.platformID
        self.platEncID = name_id5_record.platEncID
        self.langID = name_id5_record.langID
        self.nameID = name_id5_record.nameID
        self.version_string = name_id5_record.toUnicode()  # name_id5_record.string cast to str in Py3 / unicode in Py2
        self.version_parts_list = []

        self._make_version_parts_list()

    def _make_version_parts_list(self):
        if ";" in self.version_string:
            self.version_parts_list = self.version_string.split(";")
        else:
            self.version_parts_list = [self.version_string]

    def get_repo_commit(self):
        repo = Repo(get_git_root_path())
        gitpy = repo.git
        # git rev-list --abbrev-commit --max-count=1 --format="%h" HEAD - abbreviated unique sha1 for the repository
        # number of sha1 hex characters determined by git (addresses https://github.com/source-foundry/font-v/issues/2)
        full_git_sha_string = gitpy.rev_list('--abbrev-commit', '--max-count=1', '--format="%h"', 'HEAD')
        unicode_full_sha_string = tounicode(full_git_sha_string)
        sha_string_list = unicode_full_sha_string.split("\n")
        final_sha_string = sha_string_list[1].replace('"', '')
        return final_sha_string

    def get_print_string(self):
        return self.fontpath + ":" + os.linesep + self.version_string

    def get_dev_print_string(self):
        encoding_str = getEncoding(self.platformID, self.platEncID, self.langID)
        if encoding_str is None:
            encoding_str = "unknown"  # if fontTools.misc.encodingTools.getEncoding returns None, encoding not detected
        recordtype_list = [str(self.platformID), str(self.platEncID), str(self.langID), str(self.nameID)]
        recordtype_string = "/".join(recordtype_list)
        print_string = self.fontpath + " [" + recordtype_string + " (encoding='" \
                                       "" + encoding_str + "')]:" + os.linesep + self.version_string
        return print_string

    def get_version_string(self):
        return self.version_parts_list[0]   # anything before first ';' in version string name record

    def get_post_string(self):
        if len(self.version_parts_list) > 1:
            filtered_post_list = []   # maintains a list of string parts that pass filters below
            for part in self.version_parts_list[1:]:
                if part.strip() in ["DEV", "RELEASE"]:
                    pass
                elif part[-4:] == "-dev":
                    pass
                elif part[-8:] == "-release":
                    pass
                else:
                    filtered_post_list.append(part)
            if len(filtered_post_list) > 1:
                return ";".join(self.version_parts_list[1:])  # return ; delimited string if there were multiple parts
            elif len(filtered_post_list) == 1:
                return filtered_post_list[0]               # return the value only if this filter eliminated all but one
            else:
                return ""                                 # return empty string if filter removed all other strings
        elif len(self.version_parts_list) == 2:
            return self.version_parts_list[1]            # return just the post string if only one post part
        else:
            return ""                                   # return empty list if there was no string after version string


def get_git_root_path():
    """
    Recursively searches for git root path over 4 directory levels above working directory
    :return: validated git root path as string OR raises SystemExit if not found
    """
    try:
        # begin by defining current working directory as root of git repository
        unverified_gitroot_path = os.path.abspath('.')

        # check to see if this assumption is correct
        if dir_exists(os.path.join(unverified_gitroot_path, '.git')):
            verified_gitroot_path = os.path.join(unverified_gitroot_path, '.git')
        else:  # if not, recursive search up to three directories above for the git repo root
            one_level_up = os.path.abspath(os.path.join(unverified_gitroot_path, os.pardir))
            two_levels_up = os.path.dirname(one_level_up)
            three_levels_up = os.path.dirname(two_levels_up)

            one_level_up_path = os.path.join(one_level_up, '.git')
            two_levels_up_path = os.path.join(two_levels_up, '.git')
            three_levels_up_path = os.path.join(three_levels_up, '.git')

            if dir_exists(one_level_up_path):  # check one directory level up
                verified_gitroot_path = os.path.dirname(one_level_up_path)
            elif dir_exists(two_levels_up_path):  # check two directory levels up
                verified_gitroot_path = os.path.dirname(two_levels_up_path)
            elif dir_exists(three_levels_up_path):  # check three directory levels up
                verified_gitroot_path = os.path.dirname(three_levels_up_path)
            else:
                sys.stderr.write("[font-v] ERROR: Unable to identify the root of your git repository. "
                                 "Please try again from the root of your repository." + os.linesep)
                sys.exit(1)
    except Exception as e:
        sys.stderr.write("[font-v] ERROR: Unable to identify the root of your git repository. "
                         "Please try again from the root of your repository. " + str(e) + os.linesep)
        sys.exit(1)

    return verified_gitroot_path


if __name__ == '__main__':
    main()
