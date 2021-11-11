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
import logging

import matplotlib
from traits.etsconfig.api import ETSConfig

from hyperspy.defaults_parser import preferences


__all__ = [
    'axes',
    'messages',
    'microscope_parameters',
    'model',
    'preferences',
    'tools',
    '__version__',
    ]


# mapping following the pattern: from value import key
_import_mapping = {
    '__version__':'.version',
    }


def __dir__():
    return sorted(__all__)


def __getattr__(name):
    if name in __all__:
        if name in _import_mapping.keys():
            import_path = 'hyperspy_gui_traitsui' + _import_mapping.get(name)
            return getattr(importlib.import_module(import_path), name)
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
backend = matplotlib.get_backend()
_logger.debug('Loading hyperspy.traitsui_gui')
_logger.debug('Current MPL backend: %s', backend)
if "WX" in backend:
    set_ets_toolkit("wx")
elif "Qt" in backend:
    set_ets_toolkit("qt4")
elif ETSConfig.toolkit == "":
    # The toolkit has not been set and no supported toolkit is available, so
    # setting it to "null"
    set_ets_toolkit("null")
    if preferences.GUIs.warn_if_guis_are_missing:
        _logger.warning(
            f"The {backend} matplotlib backend is not compatible with the "
            "traitsui GUI elements. For more information, read "
            "http://hyperspy.readthedocs.io/en/stable/user_guide/getting_started.html#possible-warnings-when-importing-hyperspy"
            ".")
