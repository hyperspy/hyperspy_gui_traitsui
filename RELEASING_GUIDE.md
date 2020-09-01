## Release

To make a new release, push a tag to the `hyperspy/hyperspy_gui_traitsui` repository.
The tag must start with `v` and follow semantic versioning.

Once the tag has been pushed, the github release workflow will:
1. Create a github release
2. set library version from tag
3. build source and binary distribution using pep517
4. install and test the new package (check if suitable for upload to pypi)
5. upload to pypi
6. set library version to development version and push this change to repository

If the release github workflow is run from a fork, no package will be uploaded to
pypi and instead the packages will be available as a github artifat.