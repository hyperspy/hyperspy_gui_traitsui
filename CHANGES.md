..
  Add a single entry in the corresponding section below.
  See https://keepachangelog.com for details

## v2.0.1 (2024-08-05)

* Fix getting matplotlib backend for matplotlib >= 3.10.dev ([#78](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/78)).
* Use `qt` instead of `qt4` when setting `ETSConfig.toolkit` ([#78](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/78)).
* Fix slider in image contrast editor on python >=3.10 ([#76](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/76)).
* Fix getting version with editable installation ([#75](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/75)).
* Add releasing guide and release script ([#75](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/75)).
* Fix regression with editable installation ([#74](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/74)).

## v2.0 (2023-11-16)

* Consolidate package metadata into `pyproject.toml` ([#67](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/67))
* Support HyperSpy 2.0 and set HyperSpy requirement to >=2.0 ([#65](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/65))
* Remove use of deprecated HyperSpy preferences `warn_if_guis_are_missing` ([#58](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/58))
* Remove `integrate_in_range` widgets, as the corresponding method has been removed in hyperspy 2.0. ([#53](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/53))
* Added github action for code scanning using the codeQL engine ([#51](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/51))

## v1.5.3 (2023-05-30)

* Add explicit support for python 3.11 ([#62](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/62))
* Fix typo in `ImageContractEditor` GUI ([#59](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/59))
* Exclude `traitsui` 8.0.0 because of a regression in the `BoundsEditor` ([#61](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/61))
* Fix pyqt installation on GitHub CI ([#52](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/52))

## v1.5.2 (2022-06-18)

* Fix error when pressing "OK" button after "Apply" was pressed in `crop_signal1D` ([#49](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/49))

## v1.5.1 (2022-05-03)

* Fix import tools error when running hyperspy test suite ([#47](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/47))

## v1.5.0 (2022-04-26)

* Add `is_binned` to axis GUI, make index of the navigation axis editable ([#39](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/39)).
* Fix loading GUI ([#38](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/38)).
* Improve rendering changelog on github and fix hyperlinks in `README.md` ([#42](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/42)).
* Speed up import time by importing submodules lazily and drop support for python 3.6 ([#41](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/41)).
* Add python 3.10 to github CI and update github actions versions ([#43](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/43)).
* Fix traistui deprecation warning and add oldest supported version of dependencies build to github CI ([#45](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/45))
* Add GUI for the calibration method of signal2D ([#3](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/3))

## v1.4.0 (2021-04-13)

The is a minor release:

* Fix closing contrast editor tool ([#35](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/35)).
* Add iterpath to fit component GUI ([#34](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/34)).
* Make axes gui compatible with non-unform axis ([#25](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/25)).
* Use GitHub Actions to run the test suite and make release ([#32](https://github.com/hyperspy/hyperspy_gui_traitsui/pull/32)).
