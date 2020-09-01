# -*- coding: utf-8 -*-
# Copyright 2007-2020 The HyperSpy developers
#
# This file is part of  HyperSpy.
#
#  HyperSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
#  HyperSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with  HyperSpy.  If not, see <http://www.gnu.org/licenses/>.

from distutils.version import LooseVersion


default_changelog_template_minor = \
"""
.. _changes___VERSION__:

v__VERSION__ (UNRELEASED)
++++++

Follow the following links for details on all the
- `changes <https://github.com/hyperspy/hyperspy/pulls?q=is%3Apr+is%3Aclosed+milestone%3Av__VERSION__>`__
- `closed issues <https://github.com/hyperspy/hyperspy/issues?q=is%3Aissue+is%3Aclosed+milestone%3Av__VERSION__>`__.


.. Add one line to describe the new feature or the enhancement in one of the lists below

NEW
---
-


Enhancements
------------
-


API changes
-----------
-


"""


default_changelog_template_patch = \
"""
.. _changes___VERSION__:

v__VERSION__ (UNRELEASED)
++++++

Follow the following links for details on all the
- `changes <https://github.com/hyperspy/hyperspy/pulls?q=is%3Apr+is%3Aclosed+milestone%3Av__VERSION__>`__
- `closed issues <https://github.com/hyperspy/hyperspy/issues?q=is%3Aissue+is%3Aclosed+milestone%3Av__VERSION__>`__.


BUG FIXES
---------
.. Add one line to describe the bug fix in the list below
-


"""

def clean_changelog(filename):
    """
    Remove the label (UNRELEASED) from the changelog

    Parameters
    ----------
    filename : str
        Filename of the changelog file to be cleaned.

    Returns
    -------
    None.

    """
    with open(filename, 'r') as f:
        content = f.readlines()

    # Remove label "(UNRELEASED)"
    for i, line in enumerate(content[:100]):
        if '(UNRELEASED)' in line:
            content[i] = line.replace('(UNRELEASED)', '').replace(" ", "")
            print(f'(UNRELEASED) label removed at line {i}.')

    with open(filename, 'w') as f:
        f.writelines(content)


def get_new_version(version):
    version_digits = LooseVersion(version).version
    if len(version_digits) > 2 and version_digits[2] > 0:
        # This release is a patch
        # define new version as current version + patch incremented by 1
        release_type = 'patch'
        version_digits[2] += 1
        new_version = ".".join([str(v) for v in version_digits])
    else:
        # This release is a minor
        release_type = 'minor'
        version_digits[1] += 1
        new_version = ".".join([str(v) for v in version_digits])

    return new_version, release_type


def prepare_changelog_for_development(filename, version):
    """
    Prepare the changelog for development by inserting a template for minor
    or patch release at the beginning of the changelog file.


    Parameters
    ----------
    filename : str
        Filename of the changelog file to prepare for development.

    version : str
        Version of the current release.

    Returns
    -------
    None.

    """
    new_version, release_type = get_new_version(version)
    if release_type == 'patch':
        changelog_header = default_changelog_template_patch.replace('__VERSION__', new_version)
    else:
        changelog_header = default_changelog_template_minor.replace('__VERSION__', new_version)

    with open(filename, 'r') as f:
        content = f.readlines()

    # insert the content after the first 3 lines the first 3 lines
    content.insert(5, changelog_header)

    with open(filename, 'w') as f:
        f.writelines(content)

    print(f'{filename} ready for development of v{new_version}.')


def _write_version(filename, version):
    with open(filename, 'w') as f:
        f.write(f"__version__ = '{version}'")

    print(f'Version set to {version}')


def set_development_version(filename, version):
    """
    The commit following to a release must update the version number
    to the version number of the release followed by ".dev", e.g.
    if the version of the last release is 0.4.1 the version of the
    next development version afterwards must be 0.4.1.dev.
    When running setup.py the ".dev" string will be replaced (if possible)
    by the output of "git describe" if git is available or the git
    hash if .git is present.
    """
    version_dev, _ = get_new_version(version)
    version_dev += '.dev0'
    _write_version(filename, version_dev)


def set_release_version(filename, version):
    _write_version(filename, version)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description="Script to maintain the CHANGELOG file."
    )
    parser.add_argument('-f', '--filename', type=str)
    parser.add_argument('-t', '--tag', type=str)
    parser.add_argument('--prepare_dev', action='store_true')
    parser.add_argument('--clean', action='store_true')
    parser.add_argument('--set_dev_version', action='store_true')
    parser.add_argument('--set_release_version', action='store_true')

    args = parser.parse_args()

    if hasattr(args, 'filename'):
        filename = args.filename
    else:
        raise ValueError('The filename of the changelog is missing.')

    def _get_tag(args):
        if args.tag is not None:
            return args.tag
        else:
            raise ValueError('The tag of the release is missing.')

    if args.prepare_dev:
        version = _get_tag(args)
        prepare_changelog_for_development(filename, version)

    if args.clean:
        clean_changelog(filename)

    if args.set_dev_version:
        version = _get_tag(args)
        set_development_version(filename, version)

    if args.set_release_version:
        version = _get_tag(args)
        set_release_version(filename, version)
