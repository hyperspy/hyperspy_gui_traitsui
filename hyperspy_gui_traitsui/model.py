import traitsui.api as tu

from hyperspy_gui_traitsui.utils import add_display_arg
from hyperspy_gui_traitsui.buttons import OurFitButton, OurCloseButton
from hyperspy_gui_traitsui.tools import SpanSelectorInSignal1DHandler


class ComponentFitHandler(SpanSelectorInSignal1DHandler):

    def fit(self, info):
        """Handles the **Apply** button being clicked.

        """
        obj = info.object
        obj._fit_fired()
        return


@add_display_arg
def fit_component_tratisui(obj, **kwargs):
    fit_component_view = tu.View(
        tu.Item('only_current', show_label=True,),
        buttons=[OurFitButton, OurCloseButton],
        title='Fit single component',
        handler=ComponentFitHandler,
    )
    return obj, {"view": fit_component_view}


class EstimateAndSetCorelossEdgeOnsetHandler(SpanSelectorInSignal1DHandler):

    def fit(self, info):
        """Handles the **Apply** button being clicked.

        """
        obj = info.object
        obj._set_onset_fired()
        return


@add_display_arg
def estimate_and_set_coreloss_edge_onset_traitsui(obj, **kwargs):
    estimate_and_set_coreloss_edge_onset_view = tu.View(
        tu.Item('percent_position', show_label=True,),
        tu.Item('only_current', show_label=True,),
        buttons=[OurFitButton, OurCloseButton],
        title='Set edge onset',
        handler=EstimateAndSetCorelossEdgeOnsetHandler,
    )
    return obj, {"view": estimate_and_set_coreloss_edge_onset_view}
