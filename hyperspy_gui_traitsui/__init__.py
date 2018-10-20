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

__version__ = "1.1.1"
import logging

import matplotlib
from traits.etsconfig.api import ETSConfig
from hyperspy.defaults_parser import preferences


_logger = logging.getLogger(__name__)


_logger.debug("Initial ETS toolkit set to {}".format(ETSConfig.toolkit))


WARN = (
    not hasattr(preferences.GUIs, "warn_if_guis_are_missing") # hspy < v.1.3.1
    or preferences.GUIs.warn_if_guis_are_missing)

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
backend = matplotlib.rcParams["backend"]
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
    if WARN:
        _logger.warning(
            "The {} matplotlib backend is not supported by the "
            "installed traitsui version and the ETS toolkit has been set to null. "
            "To set the ETS toolkit independently from the matplotlib backend, "
            "set it before importing matplotlib. See "
            "http://hyperspy.readthedocs.io/en/stable/user_guide/getting_started.html "
            "for more information.".format(matplotlib.get_backend()))

if ETSConfig.toolkit and ETSConfig.toolkit != "null":
    import hyperspy.api_nogui # necessary to register the toolkeys
    # Register the GUI elements
    import hyperspy_gui_traitsui.axes
    import hyperspy_gui_traitsui.model
    import hyperspy_gui_traitsui.tools
    import hyperspy_gui_traitsui.preferences
    import hyperspy_gui_traitsui.microscope_parameters
    import hyperspy_gui_traitsui.messages
elif WARN:
    _logger.warning("The traitsui GUI elements are not available.")
