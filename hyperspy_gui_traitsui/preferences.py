import traitsui.api as tui
from traitsui.menu import CancelButton

from hyperspy_gui_traitsui.buttons import SaveButton
from hyperspy_gui_traitsui.utils import (
    register_traitsui_widget, add_display_arg)


class PreferencesHandler(tui.Handler):

    def save(self, info):
        # Removes the span selector from the plot
        info.object.save()
        return True

PREFERENCES_VIEW = tui.View(
    tui.Group(tui.Item('General', style='custom', show_label=False, ),
              label='General'),
    tui.Group(tui.Item('GUIs', style='custom', show_label=False, ),
              label='GUIs'),
    tui.Group(tui.Item('Plot', style='custom', show_label=False, ),
              label='Plot'),
    tui.Group(tui.Item('EELS', style='custom', show_label=False, ),
              label='EELS'),
    tui.Group(tui.Item('EDS', style='custom', show_label=False, ),
              label='EDS'),
    title='Preferences',
    buttons=[SaveButton, CancelButton],
    handler=PreferencesHandler,)


@register_traitsui_widget(toolkey="Preferences")
@add_display_arg
def preferences_traitsui(obj, **kwargs):
    obj.trait_view("traits_view", PREFERENCES_VIEW)
    return obj, {}
