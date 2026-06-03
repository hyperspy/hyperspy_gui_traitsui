# -*- coding: utf-8 -*-
# Copyright 2007-2026 The HyperSpy developers
#
# This file is part of HyperSpy.
#
# HyperSpy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HyperSpy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HyperSpy. If not, see <https://www.gnu.org/licenses/#GPL>.


import traitsui.api as tui
from traitsui.menu import CancelButton

from hyperspy.misc.utils import grouped_editable_traits
from hyperspy_gui_traitsui.buttons import SaveButton
from hyperspy_gui_traitsui.utils import add_display_arg


class PreferencesHandler(tui.Handler):

    def save(self, info):
        # Removes the span selector from the plot
        info.object.save()
        return True


def _plot_groups():
    """Build tui.Group items for the Plot tab from grouped editable traits."""
    from hyperspy.defaults_parser import preferences

    grouped = grouped_editable_traits(preferences.Plot)
    groups = []
    for label, traits in grouped.items():
        content = [tui.Item(f"object.Plot.{trait_name}") for trait_name in traits]
        groups.append(tui.Group(*content, label=label, show_border=True))
    return groups


PREFERENCES_VIEW = tui.View(
    tui.Group(tui.Item('General', style='custom', show_label=False, ),
              label='General'),
    tui.Group(tui.Item('GUIs', style='custom', show_label=False, ),
              label='GUIs'),
    tui.Group(*_plot_groups(), layout='tabbed', label='Plot'),
    title='Preferences',
    buttons=[SaveButton, CancelButton],
    handler=PreferencesHandler,)


@add_display_arg
def preferences_traitsui(obj, **kwargs):
    obj.trait_view("traits_view", PREFERENCES_VIEW)
    return obj, {}


EXSPY_PREFERENCES_VIEW = tui.View(
    tui.Group(tui.Item('EELS', style='custom', show_label=False, ),
              label='EELS'),
    tui.Group(tui.Item('EDS', style='custom', show_label=False, ),
              label='EDS'),
    title='Preferences',
    buttons=[SaveButton, CancelButton],
    handler=PreferencesHandler,)


@add_display_arg
def exspy_preferences_traitsui(obj, **kwargs):
    obj.trait_view("traits_view", EXSPY_PREFERENCES_VIEW)
    return obj, {}
