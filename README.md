
![](https://github.com/source-foundry/font-v/raw/images/images/font-v-crunch.png)

[![Build Status](https://semaphoreci.com/api/v1/sourcefoundry/font-v/branches/master/badge.svg)](https://semaphoreci.com/sourcefoundry/font-v)  [![Build status](https://ci.appveyor.com/api/projects/status/mtbar0q307926xff/branch/master?svg=true)](https://ci.appveyor.com/project/chrissimpkins/font-v/branch/master)

## About

font-v is an open source font version string library (`libfv`) and associated executable (`font-v`) for reading, modifying, and writing OpenType name table name ID 5 records (i.e. version string records) in `*.otf` and `*.ttf` fonts.  It is designed to support an extension to the OpenType font versioning specification.

font-v is built with Python and can be used on Linux, OS X, and Windows platforms with either Python 2 or Python 3 interpreters.

## Contents
- [Installation](#installation)
- [font-v Executable Usage](#font-v-executable-usage)
- [libfv Library Usage](https://github.com/source-foundry/font-v/tree/dev#libfv-usage)
- [libfv Library API documentation](https://font-v.rtfd.io/)

## Installation

The `libfv` library and the `font-v` executable are installed simultaneously.

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

font-v is executed with a set of subcommands and options that define your command.

```
$ font-v [subcommand] (options) [font path 1] ([font path ...])
```

### Available subcommands and options

- `report` - report OpenType name table nameID 5 record
	- `--dev` - include all nameID 5 x platformID records in report
- `write` - modify the version string with the following options
	- `--dev` - add *dev* build metadata tag to version string (mutually exclusive with `--rel`)
	- `--rel` -  add *release* build metadata tag to version string (mutually exclusive with `--dev`)
	- `--sha1` - add git sha1 short hash tag to version string (requires fonts in git repository)
	- `--ver=[version string]` - modify current version number with a new version number using `1_000` or `1-000` format


### Version string reporting

Enter the following to display the font version string for the font Example-Regular.ttf:

```
$ font-v report Example-Regular.ttf
```

Include the `--dev` flag to include the version string (nameID 5) contained in all platformID records:

```
$ font-v report --dev Example-Regular.ttf
```

### Version modification

Enter the desired version number in `integer.integer` format after the `--ver=` flag with the period replaced by an underscore `_` or dash `-` (period is a special shell character):

```
$ font-v write --ver=2_020 Example-Regular.ttf
```

or to achieve the same version string change:

```
$ font-v write --ver=2-020 Example-Regular.ttf
```

This can be combined with other options (e.g. to add git commit SHA1 hash tag or development/release tag) in the same command.  All data that followed the original version string is preserved and appended after a semicolon.

### git SHA1 commit short code stamp version string

If you are developing your typeface in a git repository, you can stamp the version string with a short (7 character) SHA1 hash digest that represents the current commit at the time of the font modification with font-v (and ideally the commit at the time of the font build as this is what it is intended to represent for versioning purposes).

Use the `--sha1` option in the `write` command like this:

```
$ font-v write --sha1 Example-Regular.ttf
```

The short SHA1 hash digest is added with the following version string formatting:

```
Version 1.000; cf8dc25
```

This can be combined with other options (e.g. to modify the version number or add other metadata) in the same command.  All data that followed the version number prior to modification are preserved and appended after the SHA1 hash + a semicolon.

### Add development / release metadata to version string

You can modify the version string to indicate that a build is intended as a development (testing) build or release build with the `--dev` or `--rel` flag.  These are mutually exclusive options.  You can combine these with the `--sha1` flag to create a combined git SHA1 + release/development string.

To indicate a development build, use a command like this:

```
$ font-v write --dev Example-Regular.ttf
```

and the version string is modified to the following format:

```
Version 1.000; DEV
```

To indicate a release build, use a command like this:

```
$ font-v write --rel Example-Regular.ttf
```

and the version string is modified with the following format:

```
Version 1.000; RELEASE
```

Include the `--sha1` flag with either the `--dev` or `--rel` flag in the command to include both types of information in the version string:

```
$ git write --sha1 --dev Example-Regular.ttf
$ git report Example-Regular.ttf
Example-Regular.ttf:
Version 1.000; cf8dc25-dev
```

or 

```
$ git write --sha1 --rel Example-Regular.ttf
$ git report Example-Regular.ttf
Example-Regular.ttf:
Version 1.000; cf8dc25-release
```

Any data that followed the original version string are maintained and appended after a semicolon.

## libfv Usage

The libfv Python library exposes the `FontVersion` object and associated set of attributes and public methods for reads, modifications, and writes of font version strings in your Python source code.

### Import Library into Your Project

To use the libfv library, import the `FontVersion` class into your Python script with the following:

```python
from fontv.libfv import FontVersion
```

### Create an Instance of the FontVersion Class

Next, create an instance of the `FontVersion` class with one of the following approaches:

```python
# Instantiate with a file path to the font
fv = FontVersion("path/to/font")
```

or

```python
# Instantiate with a fontTools TTFont object
#  See the fonttools documentation for further details (https://github.com/fonttools/fonttools)
fv = FontVersion(fontToolsTTFont)
```

The libfv library will automate parsing of the version string to a set of public `FontVersion` class attributes and expose public methods that you can use to examine and modify the string.  Modified version strings can then be written back out to the font file or to a new font at a different file path.

Note that all modifications to the version string are made in memory. File writes with these modified data occur when the calling code explicitly calls a write method.

### What You Can Do with the File Version Object

#### Read/Write Version String

As you make changes to the font version string, you can examine the full version string in memory with the following:

##### Get version string (including associated metadata)

```python
fv = FontVersion("path/to/font")
vs = fv.get_version_string()
```

All modifications with the public methods are made in memory.  When you are ready to write them out to a font file, call the following method:

##### Write Version String Modifications to Font File

```python
fv = FontVersion("path/to/font")
# do things to version string
fv.write_version_string()  # writes to file used to instantiate FontVersion object
fv.write_version_string(fontpath="path/to/difffont") # writes to a different file path
```

#### Compare Version Strings

##### Test Version Equality / Inequality

```python
fv1 = FontVersion("path/to/font1")
fv2 = FontVersion("path/to/font2")

print(fv1 == fv2)
print(fv1 != fv2)
```

#### Modify Version String

Some common font version string tasks that are supported by the `libfv` library include the following:

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

##### Work with Major/Minor Version Number Integers

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

##### Eliminate Metadata from a Version String

```python
fv = FontVersion("path/to/font")
# pre modification version string = "Version 1.000; some metadata; other metadata"
fv.clear_metadata()
# post modification version string = "Version 1.000"
```

##### Set Development/Release Status of the Font Build

```python
fv = FontVersion("path/to/font")

# Label as development build
fv.set_development_status()

# Label as release build
fv.set_release_status()
```

##### Set git Commit SHA1 Hash Label to Maintain Documentation of Source State at Build

```python
fv = FontVersion("path/to/font")

# Set git commit SHA1 only
fv.set_git_commit_sha1()

# Set git commit SHA1 with development status indicator
fv.set_git_commit_sha1(development=True)

# Set git commit SHA1 with release status indicator
fv.set_git_commit_sha1(release=True)
```


### libfv API

Full documentation of the `libfv` API is available at http://font-v.readthedocs.io/



## Acknowledgments

Built with the fantastic [fonttools](https://github.com/fonttools/fonttools) and [GitPython](https://github.com/gitpython-developers/GitPython) Python libraries.


## License

[MIT License](https://github.com/source-foundry/font-v/blob/master/docs/LICENSE)