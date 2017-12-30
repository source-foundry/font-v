## Changelog

# v0.5.0

- Changed invalid ttf/otf file error to std error stream from std output stream

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
