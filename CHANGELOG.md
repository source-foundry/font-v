## Changelog

### v0.6.5

- updated fontTools dependency to v3.25.0
- updated gitpython dependency to v2.1.9

### v0.6.4

- updated fontTools dependency to v3.24.1

### v0.6.3

- updated fontTools dependency to v3.23.0 - includes library bugfix

### v0.6.2

- updated fontTools dependency to v3.22.0

### v0.6.1

- added pin for fontTools dependency at version 3.21.2
- added pin for gitpython dependency at version 2.1.8
- updated PyPI documentation

### v0.6.0

font-v executable changes:

- added head table fontRevision record reporting to report subcommand output (default)
- added head table fontRevision record write support to write subcommand (default)
- refactored from deprecated libfv.FontVersion.get_version_string to new libfv.FontVersion.get_name_id5_version_string method
- updated in-application help documentation

libfv changes:

- added support for head.fontRevision read/writes
- added new public FontVersion class attribute head_fontRevision
- added new public FontVersion method get_head_fontrevision_version_number
- added new public FontVersion method get_version_number_string
- add new public FontVersion method get_name_id5_version_string (to replace get_version_string)
- deprecated FontVersion method get_version_string (warnings added as of this release)
- updated public FontVersion method set_version_number with head.fontRevision record write support
- updated public FontVersion method set_version_string with head.fontRevision record write support
- updated public FontVersion method write_version_string with head.fontRevision record write support
- refactor nameID 5 class attribute dictionary name

### v0.5.0

font-v executable changes:

- added full support for OpenFV font versioning specification (including version number substring, state metadata substring, status metadata substring, other metadata substring(s))
- refactored entire `write` subcommand implementation to the libfv library
- changed invalid ttf/otf file error to std error stream from std output stream
- fixed incorrect option argument string displayed in the error message for `write` with undefined `--ver=` argument

libfv changes:

- modified the formatting of git commit SHA1 hash string state writes to `[sha1]` from `sha1` to support OpenFV specification
- added FontVersion object attribute parsing after git commit sha1 hash writes to in memory version strings
- refactored development/release status substring truth testing method approach to eliminate matches against strings that fall outside of spec
- refactored FontVersion.get_status_substring method to FontVersion.get_state_status_substring with new implementation
- refactored FontVersion._set_status_substring to FontVersion._set_state_status_substring with new implementation
- eliminated FontVersion.status object attributed (unncessary)
- revised version strings in test fonts to support OpenFV specification
- modified all supporting tests for above changes

### v0.4.1

- Added `__str__` method to libfv.FontVersion class for informative human readable data on prints
- Added `is_font` function to utilities module
- Refactored `font-v report` subcommand on the new libfv library
- Removed encoding from the `font-v report --dev` report

### v0.4.0

- new: `libfv` library that exposes public FontVersion class for work with font version strings
- bugfix: `font-v` git commit SHA1 parsing error on Windows platform
- changed: refactored commandlines library to this project (from external dependency)

### v0.3.3

- added modified version string notification to standard output stream on new version writes (#13)

### v0.3.2

- bug fix for DEV/RELEASE version substring duplication when there are two version substrings (#7)

### v0.3.1

- bug fix for incorrect git sha1 string encoding in the version string (issue #12)

### v0.3.0

- added stdout reporting of name record encoding with new --dev flag for report command
- added new git sha1 string length approach to address collisions (issue #2)
- fixed duplicated dev/release strings
- added new command line subcommand error handling

### v0.2.0

- initial release
