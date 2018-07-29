import traitsui.api as tu

from hyperspy_gui_traitsui.utils import (
    register_traitsui_widget, add_display_arg)
from hyperspy_gui_traitsui.buttons import OurFitButton, OurCloseButton
from hyperspy_gui_traitsui.tools import SpanSelectorInSignal1DHandler


class ComponentFitHandler(SpanSelectorInSignal1DHandler):

    def fit(self, info):
        """Handles the **Apply** button being clicked.

        """
        obj = info.object
        obj._fit_fired()
        return


@register_traitsui_widget(toolkey="Model1D.fit_component")
@add_display_arg
def fit_component_tratisui(obj, **kwargs):
    fit_component_view = tu.View(
        tu.Item('only_current', show_label=True,),
        buttons=[OurFitButton, OurCloseButton],
        title='Fit single component',
        handler=ComponentFitHandler,
    )
    return obj, {"view": fit_component_view}


class SetCorelossEdgeOnsetHandler(SpanSelectorInSignal1DHandler):

    def fit(self, info):
        """Handles the **Apply** button being clicked.

        """
        obj = info.object
        obj._set_onset_fired()
        return


@register_traitsui_widget(toolkey="EELSModel.set_coreloss_edge_onset")
@add_display_arg
def set_coreloss_edge_onset_traitsui(obj, **kwargs):
    set_coreloss_edge_onset_view = tu.View(
        tu.Item('percent_position', show_label=True,),
        tu.Item('only_current', show_label=True,),
        buttons=[OurFitButton, OurCloseButton],
        title='Set edge onset',
        handler=SetCorelossEdgeOnsetHandler,
    )
    return obj, {"view": set_coreloss_edge_onset_view}
