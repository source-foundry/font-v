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
minor_version = "5"
patch_version = "0"

# ------------------------------------------------------------------------------
# Help String
# ------------------------------------------------------------------------------

HELP = """====================================================
font-v
Copyright 2018 Christopher Simpkins
MIT License
Source: https://github.com/source-foundry/font-v
====================================================

font-v is a font version string reporting and modification tool for ttf and otf fonts.  It is built with the libfv library and supports the OpenFV semantic font versioning specification.

USAGE:

Include a subcommand and desired options in your command line request:

   font-v [subcommand] (options) [font file path 1] ([font file path ...])

Subcommands and options:

 report - report OpenType name table nameID 5 record (default: single record)
    --dev - include all nameID 5 x platformID records in report
    
 write - modify the version string with the following options:
   --dev - add development status metadata (mutually exclusive with --rel)
   --rel -  add release status metadata (mutually exclusive with --dev)
   --sha1 - add git commit sha1 short hash state metadata
   --ver=[version #] - change version number to `version #` definition

NOTES:

The write subcommand --dev and --rel flags are mutually exclusive. Include up to one of these options.

For platforms that treat the period as a special shell character, the --ver=[version #] an underscore or dash glyph can be used in place of a period to define the version number on the command line.  For example, 2.001 can be defined with either of the following:

   $ font-v write --ver=2_001
   $ font-v write --ver=2-001
   
You can include version number, status, and state options in the same request to make all of these modifications simultaneously.

The write subcommand modifies all nameID 5 records identified in the OpenType name table of the font (i.e. across all platformID).

font-v and the underlying libfv library follow the OpenFV semantic font versioning specification.  This specification can be viewed at https://github.com/openfv/openfv.

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