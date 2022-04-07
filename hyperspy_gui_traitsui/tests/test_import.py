import pytest

import hyperspy.api as hs
import hyperspy.ui_registry


def test_ui_registry():
    if "traitsui" in hyperspy.ui_registry.TOOLKIT_REGISTRY:
        assert "traitsui" in hyperspy.ui_registry.TOOLKIT_REGISTRY
    else:
        if "ipywidgets" in hyperspy.ui_registry.TOOLKIT_REGISTRY:
            with pytest.raises(ValueError):
                hs.preferences.gui(toolkit="traitsui")
        else:
            # As ipywidgets is not installed it should raise an import error
            with pytest.raises(ImportError):
                hs.preferences.gui(toolkit="traitsui")


def test_import_version():
    from hyperspy_gui_traitsui import __version__


def test_import():
    import hyperspy_gui_traitsui
    for obj_name in hyperspy_gui_traitsui.__all__:
        getattr(hyperspy_gui_traitsui, obj_name)


def test_import_import_error():
    import hyperspy_gui_traitsui
    try:
        hyperspy_gui_traitsui.inexisting_module
    except AttributeError:
        pass


def test_dir():
    import hyperspy_gui_traitsui
    d = dir(hyperspy_gui_traitsui)
    assert d == [
        '__version__',
        'axes',
        'messages',
        'microscope_parameters',
        'model',
        'preferences',
        'tools',
        ]
