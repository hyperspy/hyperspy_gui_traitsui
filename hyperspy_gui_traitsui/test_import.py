import unittest
import hyperspy.api as hs
import hyperspy.ui_registry


class Test(unittest.TestCase):

    def test_registry(self):
        if "traitsui" in hyperspy.ui_registry.TOOLKIT_REGISTRY:
            self.assertTrue("traitsui" in hyperspy.ui_registry.TOOLKIT_REGISTRY)
        else:
            if "ipywidgets" in hyperspy.ui_registry.TOOLKIT_REGISTRY:
                with self.assertRaises(ValueError):
                    hs.preferences.gui(toolkit="traitsui")
            else:
                # As ipywidgets is not installed it should raise an import error
                with self.assertRaises(ImportError):
                    hs.preferences.gui(toolkit="traitsui")
