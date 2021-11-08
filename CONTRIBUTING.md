# Contributing

## Issue Reports

Please review the existing issue reports (including open and closed) for a history of the issue that you would like to report in order to confirm that we have not already addressed it.  If your issue is new, please [file a new issue report](https://github.com/source-foundry/font-v/issues/new) here on the Github repository.

## Source Code Contributions

Contributions to the source code are highly encouraged and welcomed!  We recommend that you open a new issue report to discuss a major source code refactor, implementation of a major new feature, or any other major modification that requires an extended amount of time/effort before you invest the time in the work (assuming that your intent is for this to be merged upstream).

### License

To contribute source code to this project you must be willing to contribute your source changes under the existing [MIT license](https://github.com/source-foundry/font-v/blob/master/docs/LICENSE).  If this is not acceptable, please do not submit your changes for review.

### Development Installs

git clone the font-v repository and base your work on the `dev` branch.  Install a local development version of the project with the following command (executed in the root of the repository):

```
$ python setup.py develop
```

This will allow you to immediately test source code changes that you make in the Python modules (i.e. without a new install with every change).

### Source Code Testing

The font-v project is tested against current versions of the Python 3.7+ interpreters across Linux, macOS, and Windows platforms.  We intend to maintain this breadth of cross platform and Python interpreter release history support as new Python releases become available.  Please submit an issue report on the repository to discuss any proposed changes that will narrow the level of Python interpreter or platform support in the project.

We use [tox](https://tox.readthedocs.io/en/latest/) and [pytest](https://docs.pytest.org/en/latest/) for Python source code testing.  You can install these testing packages on your development system with:

```
$ pip install tox
$ pip install pytest
```

To run the `font-v` project tests locally across different Python interpreter versions, install all Python interpreter versions that you intend to use for testing and then use a command like the following from the root of the repository, specifying the target Python interpreter versions:

```
$ tox -e py310
```

See the tox documentation for additional details and further information about available Python interpreter versions.

Please include new pytest tests (or update existing tests if appropriate) with all source changes!  This will greatly accelerate the review process for your changes.

Cross platform continuous integration testing is performed on all pull requests that are submitted to the project.  You may view the results of the tests on your source code changes in the pull request thread.

### Propose your changes

When you are ready to propose your source code changes for upstream review, submit a pull request to the `font-v` repository using the Github UI.  Please include sufficient information in the initial post of the pull request to orient the project maintainer to your changes as well as links to any pertinent open issue report threads.

Please refer to Github documentation for details on the pull request workflow or feel free to contact us to ask for additional information if you have not previously attempted a pull request on Github.  We would be glad to help so that this is not a barrier to your contribution!