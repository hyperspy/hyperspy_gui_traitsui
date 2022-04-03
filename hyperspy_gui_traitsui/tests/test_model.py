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
from hyperspy.models.model1d import ComponentFit

from hyperspy_gui_traitsui.tests.utils import KWARGS


def test_fit_component():
    np.random.seed(0)
    s = hs.signals.Signal1D(np.random.normal(size=1000, loc=1)).get_histogram()
    s = hs.stack([s, s])
    m = s.create_model()
    m.extend([hs.model.components1D.Gaussian(),
              hs.model.components1D.Gaussian()])
    g1, g2 = m
    g1.centre.value = 0
    g2.centre.value = 8
    fc = ComponentFit(model=m, component=g1)
    fc.only_current = True
    fc.gui(**KWARGS)
    fc.ss_left_value = -2
    fc.ss_right_value = 4
    fc.only_current = False
    fc.iterpath = 'serpentine'
    fc.iterpath = 'flyback'