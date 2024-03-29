## Changelog

## v2.1.0

- `get_git_root_path` now searches up to five directory levels for the root .git directory path before failing (broadens suppport for more deeply nested font paths)
- update fonttools dependency to v4.28.2

## v2.0.0

- drop support for Python interpreters < 3.7 (dropped by our fonttools dependency)
- drop Py 3.6 CI testing
- add Py 3.10 CI testing
- transition GitHub Actions workflows to Python 3.10 interpreter default
- use Py 3.10 in tox.ini config
- remove OpenFV spec references from source and repository documentation
- udpate fonttools dependency to v4.28.1
- update gitdb dependency to v4.0.9
- update gitpython dependency to v3.1.24
- update smmap dependency to v5.0.0

### v1.0.5

- add Python 3.9 classifier to `setup.py`
- minor `setup.py` source formatting updates
- update fonttools dependency to v4.17.0
- update gitpython dependency to v3.1.11

### v1.0.4

- add cPython 3.9 interpreter testing
- add CodeQL testing
- update fonttools dependency to v4.16.1
- update gitpython dependency to v3.1.10

### v1.0.3

- update fonttools dependency to v4.14.0
- update gitdb dependency to v4.0.5
- update gitpython dependency to v3.1.8
- update smmap dependency to v3.0.4
- transition CI testing to the GitHub Actions service

### v1.0.2

- add Production/Stable classifier to `setup.py`
- remove Python < 3.6 classifiers from `setup.py`
- add Python 3.7, Python 3.8 classifiers to `setup.py`

### v1.0.1

- remove Py2 wheel builds
- add requirements.txt defined build dependency installs in CI testing

### v1.0.0

- remove Py2.7 support
- remove Py3.5 and below support
- update project Python dependencies
- fix: CI testing configuration and unit tests, including those that were Py2.7 dependent tests

### v0.7.1

- added license to Python wheel distributions
- updated fontTools dependency to v3.28.0

### v0.7.0

- removed timestamp recalculations on version string modification file writes
- removed libfv method `FontVersion.get_version_string` (deprecated with warning since v0.6.0)
- updated fontTools dependency to v3.27.0
- updated gitpython dependency to v2.1.10

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
- refactored FontVersion.\_set_status_substring to FontVersion.\_set_state_status_substring with new implementation
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
