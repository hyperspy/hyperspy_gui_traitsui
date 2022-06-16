
import numpy as np
import hyperspy.api as hs

from hyperspy_gui_traitsui.tests.utils import KWARGS


class TestAxes:

    def setup_method(self, method):
        s = hs.signals.Signal1D(np.empty((2, 3, 4)))
        am = s.axes_manager
        am[0].scale = 0.5
        am[0].name = "a"
        am[0].units = "eV"
        am[1].scale = 1000
        am[1].name = "b"
        am[1].units = "meters"
        am[2].scale = 5
        am[2].name = "c"
        am[2].units = "e"
        am.indices = (2, 1)
        self.s = s

    def test_navigation_sliders(self):
        am = self.s.axes_manager
        am.gui_navigation_sliders(**KWARGS)

    def test_axes_manager_gui(self):
        s = self.s
        s.axes_manager.gui(**KWARGS)


def test_non_uniform_axes():
    dict0 = {'scale': 1.0, 'size':2}
    dict1 = {'expression': 'a / (x+b)', 'a': 1240, 'b': 1, 'size': 3,
             'name': 'plumage', 'units': 'beautiful', 'navigate': False}
    dict2 = {'axis': np.arange(4), 'name': 'norwegianblue', 'units': 'ex',
             'navigate': False, }
    dict3 = {'expression': 'a / (x+b)', 'a': 1240, 'b': 1, 'x': dict2,
             'name': 'pushing up', 'units': 'the daisies', 'navigate': False}
    s = hs.signals.Signal2D(np.empty((2, 3, 4, 4)), axes=[dict0, dict1, dict2, dict3])

    s.axes_manager.gui(**KWARGS)

    s2 = hs.signals.Signal1D(np.empty((3, 4, 4, 2)), axes=[dict1, dict2, dict3, dict0])
    s2.axes_manager.gui_navigation_sliders(**KWARGS)
    s2.axes_manager.gui(**KWARGS)

