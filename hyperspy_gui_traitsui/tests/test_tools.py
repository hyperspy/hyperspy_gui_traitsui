# -*- coding: utf-8 -*-
# Copyright 2007-2021 The HyperSpy developers
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

import numpy as np
import hyperspy.api as hs

from hyperspy.signal_tools import ImageContrastEditor

from hyperspy_gui_traitsui.tests.utils import KWARGS


def test_image_contrast_tool():

    s = hs.signals.Signal2D(np.random.random(10000).reshape((100, 100)))
    s.plot()

    ceditor = ImageContrastEditor(s._plot.signal_plot)
    ceditor.gui(**KWARGS)

    vmin = 5
    ceditor.vmin_percentile = vmin
    assert ceditor.vmin_percentile == vmin

    vmax = 95
    ceditor.vmax_percentile = vmax
    assert ceditor.vmax_percentile == vmax
    
    auto = False
    ceditor.auto = auto
    assert ceditor.auto == auto

    for norm in ['Linear', 'Power', 'Log', 'Symlog']:
        ceditor.norm = norm
        assert ceditor.norm == norm
