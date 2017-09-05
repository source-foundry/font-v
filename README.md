


## About

font-v is a font version string reporting and modification tool.  It reports and modifies the OpenType name table nameID 5 record in ttf and otf fonts.  

font-v is built with Python and can be used from the command line on Linux, OS X, and Windows platforms.


## Installation

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

## Usage

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

This can be combined with other options (e.g. to modify the version number or add other metadata) in the same command.  All data that followed the version number prior to modification is preserved and appended after the SHA1 hash + a semicolon.

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

Any data that followed the original version string is maintained and appended after a semicolon.

## Acknowledgments

Built with the fantastic [fonttools](https://github.com/fonttools/fonttools) and [GitPython](https://github.com/gitpython-developers/GitPython) Python libraries.


## License

[MIT License](https://github.com/source-foundry/font-v/blob/master/docs/LICENSE)