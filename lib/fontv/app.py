#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from commandlines import Command
from fontTools import ttLib

from fontv import settings
from fontv.utilities import file_exists


def main():
    c = Command()

    if c.does_not_validate_missing_args():
        sys.stderr.write("[font-v] ERROR: Please include the appropriate arguments with your command." + os.linesep)
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
        for arg in c.argv[1:]:
            if arg[-4:].lower() == ".ttf" or arg[-4:].lower() == ".otf":
                font_path = arg
                if file_exists(font_path):
                    tt = ttLib.TTFont(font_path)
                    namerecord_list = tt['name'].names
                    for record in namerecord_list:
                        if record.nameID == 5:
                            print(" ")
                            print(font_path + " [" + str(record.platformID) + "/" + str(record.platEncID) + "/" + str(record.langID) + "/" + str(record.nameID) + "]:")
                            print(record.string)
                else:
                    print("[font-v] ERROR: " + font_path + " does not appear to be a valid ttf or otf font file path")
                    sys.exit(1)
            else:
                sys.stderr.write("[font-v] ERROR: The arguments did not include a ttf or otf font file" + os.linesep)
                sys.exit(1)
    elif c.subcmd == "write":
        # argument parsing flags
        add_sha1 = False
        add_release_string = False
        add_dev_string = False
        add_new_version = False
        delete_post_string = False
        fontpath_list = []            # list of font paths that user submits on command line
        version_substring_one = ""    # used for 'Version X.XXX part'
        version_substring_two = ""    # used for sha1 commit part (optional, if requested)
        version_substring_three = ""  # used for anything that existed after first ; in pre-modified nameID 5 string

        # test for mutually exclusive arguments
        # do not refactor this below the level of the argument tests that follow
        if "--rel" in c.argv and "--dev" in c.argv:
            sys.stderr.write("[font-v] ERROR: Please use either --dev or --rel argument, not both" + os.linesep)
            sys.exit(1)

        # test arguments
        for arg in c.argv[1:]:
            if arg == "--sha1":
                add_sha1 = True
            elif arg == "--rel":
                add_release_string = True
            elif arg == "--dev":
                add_dev_string = True
            elif arg == "--delete":
                delete_post_string = True
            elif arg[0:6] == "--ver=":
                add_new_version = True
            elif len(arg) > 4 and (arg[-4:].lower() == ".ttf" or arg[-4:].lower() == ".otf"):
                if file_exists(arg):
                    fontpath_list.append(arg)
                else:
                    sys.stderr.write("[font-v] ERROR: " + arg + " does not appear to be a valid font file path." + os.linesep)
                    sys.exit(1)

        print(fontpath_list)








if __name__ == '__main__':
    main()
