#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from commandlines import Command
from fontTools import ttLib

from fontv import settings


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
                # TODO: add filepath exists check

                tt = ttLib.TTFont(font_path)
                namerecord_list = tt['name'].names
                for record in namerecord_list:
                    if record.nameID == 5:
                        print(" ")
                        print(font_path + " [" + str(record.platformID) + "/" + str(record.platEncID) + "/" + str(record.langID) + "/" + str(record.nameID) + "]:")
                        print(record.string)
            else:
                sys.stderr.write("[font-v] ERROR: The arguments did not include a ttf or otf font file" + os.linesep)
                sys.exit(1)

    elif c.subcmd == "write":
        pass

if __name__ == '__main__':
    main()
