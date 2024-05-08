# -*- coding: utf-8 -*-
# Copyright 2007-2016 The HyperSpy developers
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


import importlib
from importlib.metadata import version
import logging
from pathlib import Path

import matplotlib
from traits.etsconfig.api import ETSConfig

from hyperspy.defaults_parser import preferences


__version__ = version("hyperspy_gui_traitsui")

# For development version, `setuptools_scm` will be used at build time
# to get the dev version, in case of missing vcs information (git archive,
# shallow repository), the fallback version defined in pyproject.toml will
# be used

# if we have a editable install from a git repository try to use
# `setuptools_scm` to find a more accurate version:
# `importlib.metadata` will provide the version at installation
# time and for editable version this may be different

# we only do that if we have enough git history, e.g. not shallow checkout
_root = Path(__file__).resolve().parents[1]
if (_root / ".git").exists() and not (_root / ".git/shallow").exists():
    try:
        # setuptools_scm may not be installed
        from setuptools_scm import get_version

        __version__ = get_version(_root)
    except ImportError:  # pragma: no cover
        # setuptools_scm not install, we keep the existing __version__
        pass



__all__ = [
    'axes',
    'messages',
    'microscope_parameters',
    'model',
    'preferences',
    'tools',
    '__version__',
    ]


def __dir__():
    return sorted(__all__)


def __getattr__(name):
    if name in __all__:
        if name == "__version__":
            return __version__
        else:
            return importlib.import_module("." + name, 'hyperspy_gui_traitsui')

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


_logger = logging.getLogger(__name__)
_logger.debug("Initial ETS toolkit set to {}".format(ETSConfig.toolkit))


def set_ets_toolkit(toolkit):
    try:
        if ETSConfig.toolkit == "":
            ETSConfig.toolkit = toolkit
            _logger.debug('Current ETS toolkit set to: %s', toolkit)
        elif ETSConfig.toolkit != toolkit:
            # ETS toolkit already set to a different value
            _logger.debug(
                'ETS toolkit and matplotlib backend mismatch: the ETS toolkit '
                'is {} while the matplotlib toolkit is {}. '
                'Things may not works as expected.'.format(
                    ETSConfig.toolkit, toolkit))
    except ValueError:
        _logger.debug("Setting ETS toolkit to %s failed" % toolkit)
        set_ets_toolkit("null")


# Get the backend from matplotlib
backend = matplotlib.get_backend().lower()
_logger.debug('Loading hyperspy.traitsui_gui')
_logger.debug('Current MPL backend: %s', backend)
if "wx" in backend:
    set_ets_toolkit("wx")
elif "qt" in backend:
    set_ets_toolkit("qt")
elif ETSConfig.toolkit == "":
    # The toolkit has not been set and no supported toolkit is available, so
    # setting it to "null"
    set_ets_toolkit("null")
    _logger.warning(
        f"The {backend} matplotlib backend is not compatible with the "
        "traitsui GUI elements. For more information, read "
        "http://hyperspy.readthedocs.io/en/stable/user_guide/getting_started.html#possible-warnings-when-importing-hyperspy"
        ".")
