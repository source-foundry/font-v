#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
# Library Name
# ------------------------------------------------------------------------------
lib_name = 'font-v'

# ------------------------------------------------------------------------------
# Version Number
# ------------------------------------------------------------------------------
major_version = "0"
minor_version = "4"
patch_version = "0"

# ------------------------------------------------------------------------------
# Help String
# ------------------------------------------------------------------------------

HELP = """====================================================
font-v
Copyright 2017 Christopher Simpkins
MIT License
Source: https://github.com/source-foundry/font-v
====================================================

font-v is a font version string reporting and modification tool for ttf and otf fonts.

Subcommands and options:

 report - report OpenType name table nameID 5 record (default: single record)
    --dev - include all nameID 5 x platformID records in report
    
 write - modify the version string with the following options:
   --dev - add *dev* build metadata tag (mutually exclusive with --rel)
   --rel -  add *release* build metadata tag (mutually exclusive with --dev)
   --sha1 - add git sha1 short hash tag
   --ver=[version string] - change version number with `1_000` or `1-000` format

Please note:

The write subcommand --dev and --rel flags are mutually exclusive. 

The --ver= definition should replace the desired version period character with an underscore or dash.  This means that 2.001 is defined with either of the following:

   $ font-v write --ver=2_001
   $ font-v write --ver=2-001
   
You can use more than one option in the same command to combine desired changes to the version string.

The write subcommand modifies all nameID 5 records identified in the OpenType name table (i.e. across all platformID)

"""

# ------------------------------------------------------------------------------
# Version String
# ------------------------------------------------------------------------------

VERSION = "font-v v" + major_version + "." + minor_version + "." + patch_version


# ------------------------------------------------------------------------------
# Usage String
# ------------------------------------------------------------------------------

USAGE = """
font-v [subcommand] (options) [font file path 1] ([font file path ...])
"""