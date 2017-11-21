## Changelog

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
