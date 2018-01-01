
![](https://github.com/source-foundry/font-v/raw/images/images/font-v-crunch.png)

[![Build Status](https://semaphoreci.com/api/v1/sourcefoundry/font-v/branches/master/badge.svg)](https://semaphoreci.com/sourcefoundry/font-v)  [![Build status](https://ci.appveyor.com/api/projects/status/mtbar0q307926xff/branch/master?svg=true)](https://ci.appveyor.com/project/chrissimpkins/font-v/branch/master)

## About

font-v is an open source font version string library (`libfv`) and executable (`font-v`) for reading, reporting, modifying, and writing OpenType name table name ID 5 records (i.e. version string records) in `*.otf` and `*.ttf` fonts.  It provides support for the [OpenFV semantic font versioning specification](https://github.com/openfv/openfv).

font-v is built with Python and can be used on Linux, macOS, and Windows platforms with Python 2 and Python 3 interpreters.

## Contents
- [Installation](#installation)
- [font-v Executable Usage](#font-v-executable-usage)
- [libfv Library Usage](https://github.com/source-foundry/font-v/tree/dev#libfv-usage)
- [libfv Library API Documentation](http://font-v.readthedocs.io)
- [Contributing to font-v](#contributing-to-font-v)
- [License](#license)

## Installation

The `libfv` library and the `font-v` executable are installed simultaneously with the following installation instructions.

Installation with the [pip package manager](https://pip.pypa.io/en/stable/) is the recommended approach.

### Install with pip

Install with pip using the following command:

```
$ pip install font-v
```

### Upgrade with pip

Upgrade to a new version of font-v with the following command:

```
$ pip install --upgrade font-v
```

## font-v Executable Usage

font-v is executed with a set of subcommands and options that define your command line request.

```
$ font-v [subcommand] (options) [font path 1] ([font path ...])
```

### Available subcommands and options

- `report` - report OpenType name table nameID 5 record
	- `--dev` - include all nameID 5 x platformID records in report
- `write` - modify the version string with the following options:
	- `--dev` - add development status metadata to the version string (mutually exclusive with `--rel`)
	- `--rel` -  add release status metadata to the version string (mutually exclusive with `--dev`)
	- `--sha1` - add git commit sha1 short hash state metadata to the version string (requires source under git version control)
	- `--ver=[version #]` - modify current version number with a new version number using `1.000`, `1_000` or `1-000` command line definition formatting (the latter two formats are provided to support definitions in shells where the period is a special shell character)


### Version string reporting with `report`

Enter the following to display the font version string for the font Example-Regular.ttf:

```
$ font-v report Example-Regular.ttf
```

Include the `--dev` flag to include the version string (nameID 5) contained in all platformID records:

```
$ font-v report --dev Example-Regular.ttf
```

### Version number modification with `write`

Enter the desired version number in `integer.integer` format after the `--ver=` flag. Support is provided for the intended period glyph to be replaced with an underscore `_` or dash `-` for users on platforms where the period is a special shell character.

All of the following result in modification of the version number to `2.020`:

```
$ font-v write --ver=2.020 Example-Regular.ttf
```

```
$ font-v write --ver=2_020 Example-Regular.ttf
```

```
$ font-v write --ver=2-020 Example-Regular.ttf
```

This request can be combined with other options to include state and status metadata simultaneously.

The font version number format should follow the [OpenFV specification](https://github.com/openfv/openfv) for the version number substring.

### git SHA1 commit short hash state metadata with `write`

If your typeface source is under git version control, you can stamp the version string with a short (generally 7-8 characters) SHA1 hash digest that represents the current commit at the time of the font modification with font-v.  The git commit SHA1 hash digest is defined by the `git rev-list` command at the HEAD of your active repository branch and will match the same number of initial characters in the git commit SHA1 hash digest that is displayed when you review the commits in your `git log` (or review the commit hashes in the UI of git repository hosting platforms like Github).  This is intended to maintain metadata in the font about source code state at build time and is defined according to the [OpenFV definition of the State metadata substring](https://github.com/openfv/openfv).

Use the `--sha1` option with the `write` subcommand like this:

```
$ font-v write --sha1 Example-Regular.ttf
```

The short SHA1 hash digest is added with the following version string formatting:

```
Version 1.000;[cf8dc25]
```

This can be combined with other options (e.g. to modify the version number or add status metadata) in the same command.  Other metadata are maintained and appended to the revised version string in a semicolon delimited format with this modification.

### Add development / release status metadata with `write`

You can modify the version string to indicate that a build is intended as a development build or release build with the `--dev` or `--rel` flag.  These are mutually exclusive options.  Include only one in your command.

To add development status metadata, use a command like this:

```
$ font-v write --dev Example-Regular.ttf
```

and the version string is modified to the following format:

```
Version 1.000;DEV
```

To add release status metadata, use a command like this:

```
$ font-v write --rel Example-Regular.ttf
```

and the version string is modified with the following format:

```
Version 1.000;RELEASE
```

Include the `--sha1` flag with either the `--dev` or `--rel` flag in the command to include both status and state metadata to the version string:

```
$ git write --sha1 --dev Example-Regular.ttf
$ git report Example-Regular.ttf
Example-Regular.ttf:
Version 1.000;[cf8dc25]-dev
```

or 

```
$ git write --sha1 --rel Example-Regular.ttf
$ git report Example-Regular.ttf
Example-Regular.ttf:
Version 1.000;[cf8dc25]-release
```

Any data that followed the original version number substring are maintained and appended after the status metadata in a semicolon delimited format.

## libfv Usage

The libfv Python library exposes the `FontVersion` object along with an associated set of attributes and public methods for reads, modifications, and writes of `.otf` and `.ttf` font version strings.

The library supports the [OpenFV semantic font versioning specification](https://github.com/openfv/openfv) and provides built-in OpenFV compliant parsing and formatting of the Version Number substring, State Metadata substring, Status Metadata substring, and Other Metadata substrings as defined in the specification. Font builds that follow the OpenFV specification are, by definition, in compliance with the OpenType name table nameID 5 record (OpenType version string) specification.  Full details are available at the OpenFV repository link above.

Full documentation of the libfv API is available at http://font-v.readthedocs.io/

### Import `libfv` Library into Your Project

To use the libfv library, install the font-v project with the instructions above and import the `FontVersion` class into your Python script with the following:

```python
from fontv.libfv import FontVersion
```

### Create an Instance of the `FontVersion` Class

Next, create an instance of the `FontVersion` class with one of the following approaches:

```python
# Instantiate with a file path to the .ttf or .otf font
fv = FontVersion("path/to/font")
```

or

```python
# Instantiate with a fontTools TTFont object
#  See the fonttools documentation for details (https://github.com/fonttools/fonttools)
fv = FontVersion(fontToolsTTFont)
```

The libfv library will automate parsing of the version string to a set of public `FontVersion` class attributes and expose public methods that you can use to examine and modify the version string.  Modified version strings can then be written back out to the font file or to a new font at a different file path.

Note that all modifications to the version string are made in memory. File writes with these modified data occur when the calling code explicitly calls the write method `FontVersion.write_version_string()` (details are available below).

### What You Can Do with the `FontVersion` Object

#### Read/write version string

You can examine the full version string in memory (including after modifications that you make with calling code) with the following:

##### Get version string (including associated metadata)

```python
fv = FontVersion("path/to/font")
vs = fv.get_version_string()
```

All modifications with the public methods are made in memory.  When you are ready to write them out to a font file, call the following method:

##### Write version string modifications to font file

```python
fv = FontVersion("path/to/font")
# do things to version string
fv.write_version_string()  # writes to file used to instantiate FontVersion object
fv.write_version_string(fontpath="path/to/differentfont") # writes to a different file path
```

`FontVersion.write_version_string()` provides an optional parameter `fontpath=` that can be used to define a different file path than that which was used to instantiate the `FontVersion` object.

#### Compare Version Strings

##### Test version equality / inequality

```python
fv1 = FontVersion("path/to/font1")
fv2 = FontVersion("path/to/font2")

print(fv1 == fv2)
print(fv1 != fv2)
```

#### Modify Version String

Some common font version string modification tasks that are supported by the `libfv` library include the following:

##### Set version number

```python
fv = FontVersion("path/to/font")
fv.set_version_number("1.001")
```

##### Set entire version string with associated metadata

```python
fv = FontVersion("path/to/font")
fv.set_version_string("Version 2.015; my metadata; more metadata")
```

##### Work with major/minor version number integers

```python
fv = FontVersion("path/to/font")
# version number = "Version 1.234"
vno = fv.get_version_number_tuple()
print(vno)
>>> (1, 2, 3, 4)
fv2 = FontVersion("path/to/font2")
# version number = "Version 10.234"
vno2 = fv2.get_version_number_tuple()
print(vno2)
>>> (10, 2, 3, 4)
```

##### Eliminate all metadata from a version string

```python
fv = FontVersion("path/to/font")
# pre modification version string = "Version 1.000; some metadata; other metadata"
fv.clear_metadata()
# post modification version string = "Version 1.000"
```

##### Set development/release status metadata of the font build

```python
fv = FontVersion("path/to/font")
# Label as development build
fv.set_development_status()
# adds `DEV` status metadata to version string

# Label as release build
fv.set_release_status()
# adds `RELEASE` status metadata to version string
```

##### Set git commit SHA1 hash state metadata to maintain documentation of build time source state

```python
fv = FontVersion("path/to/font")

# Set git commit SHA1 only
fv.set_state_git_commit_sha1()
# --> adds "[sha1 hash]" state metadata to build

# Set git commit SHA1 with development status indicator
fv.set_state_git_commit_sha1(development=True)
# --> adds "[sha1 hash]-dev" state metadata to build

# Set git commit SHA1 with release status indicator
fv.set_state_git_commit_sha1(release=True)
# --> adds "[sha1 hash]-release" state metadata to build
```


### libfv API

Full documentation of the `libfv` API is available at http://font-v.readthedocs.io/


## Contributing to font-v

Source contributions to the libfv library and font-v executable are encouraged and welcomed!  Please see the [CONTRIBUTING.md](CONTRIBUTING.md) documentation for details.


## Acknowledgments

Built with the fantastic [fonttools](https://github.com/fonttools/fonttools) and [GitPython](https://github.com/gitpython-developers/GitPython) Python libraries.


## License

[MIT License](https://github.com/source-foundry/font-v/blob/master/docs/LICENSE)