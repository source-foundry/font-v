## Contributing

### Issue Reports

Please search the existing issue reports (including open and closed) for a history of the issue that you would like to report in order to confirm that we have not already addressed it.  If your issue is a new one, please file a new issue report here on the Github repository.


### Source Code Contributions

Contributions to the source code are highly encouraged and welcomed!  We recommend that you open a new issue report to discuss a major source code refactor, implementation of a major new feature, or any other major modification that requires an extended amount of time/effort before you invest the time in the work (assuming that the intent is for this to be merged upstream).

#### License

To contribute source code to this project you must be willing to contribute your source changes under the existing [MIT license](https://github.com/source-foundry/font-v/blob/master/docs/LICENSE).

#### Development Installs

git clone the font-v repository and install a development version locally with the following command:

```
$ python setup.py develop
```

This will allow you to test with the source code changes that you make immediately (i.e. without a new install).

#### Testing

We use tox and pytest for source code testing.  You can install these packages locally with:

```
$ pip install tox
$ pip install pytest
```

To run the `font-v` project tests locally across different Python interpreter versions, use a command like the following from the root of the repository, specifying your target Python interpreter versions:

```
$ tox -e py27, py36
```

See the tox documentation for additional details and further information about available Python interpreter versions.

Please include pytest tests with all source changes!

#### Contribute Source Upstream

Submit a pull request to the `font-v` repository using the Github UI.  Please refer to Github documentation for details on the pull request workflow or feel free to contact us to ask for additional information if you have not previously attempted a pull request on Github.  We would be glad to help!