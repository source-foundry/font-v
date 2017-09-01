#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from commandlines import Command

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

if __name__ == '__main__':
    main()
