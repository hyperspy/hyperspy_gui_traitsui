from traitsui.menu import (OKButton, CancelButton, OKCancelButtons)
import traitsui.api as tu

from hyperspy_gui_traitsui.buttons import *
from hyperspy_gui_traitsui.utils import (
    register_traitsui_widget, add_display_arg)
from hyperspy_gui_traitsui.axes import get_navigation_sliders_group


class SmoothingHandler(tu.Handler):

    def close(self, info, is_ok):
        # Removes the span selector from the plot
        if is_ok is True:
            info.object.apply()
        else:
            info.object.close()
        return True


class SpanSelectorInSignal1DHandler(tu.Handler):

    def close(self, info, is_ok):
        # Removes the span selector from the plot
        info.object.span_selector_switch(False)
        if is_ok is True:
            self.apply(info)

        return True

    def close_directly(self, info):
        if (info.ui.owner is not None) and self.close(info, False):
            info.ui.owner.close()

    def apply(self, info, *args, **kwargs):
        """Handles the **Apply** button being clicked.

        """
        obj = info.object
        obj.is_ok = True
        if hasattr(obj, 'apply'):
            obj.apply()

        return

    def next(self, info, *args, **kwargs):
        """Handles the **Next** button being clicked.

        """
        obj = info.object
        obj.is_ok = True
        if hasattr(obj, 'next'):
            next(obj)
        return


class Signal1DRangeSelectorHandler(tu.Handler):

    def close(self, info, is_ok):
        # Removes the span selector from the plot
        info.object.span_selector_switch(False)
        if is_ok is True:
            self.apply(info)
        return True

    def apply(self, info, *args, **kwargs):
        """Handles the **Apply** button being clicked.

        """
        obj = info.object
        if obj.ss_left_value != obj.ss_right_value:
            info.object.span_selector_switch(False)
            for method, cls in obj.on_close:
                method(cls, obj.ss_left_value, obj.ss_right_value)
            info.object.span_selector_switch(True)

        obj.is_ok = True

        return


class CalibrationHandler(SpanSelectorInSignal1DHandler):

    def apply(self, info, *args, **kwargs):
        """Handles the **Apply** button being clicked.
        """
        if info.object.signal is None:
            return
        info.object.apply()
        return


class ImageContrastHandler(tu.Handler):

    def close(self, info, is_ok):
        # Removes the span selector from the plot
        #        info.object.span_selector_switch(False)
        #        if is_ok is True:
        #            self.apply(info)
        if is_ok is False:
            info.object.image.update()
        info.object.close()
        return True

    def apply(self, info):
        """Handles the **Apply** button being clicked.

        """
        obj = info.object
        obj.apply()

        return

    def reset(self, info):
        """Handles the **Reset** button being clicked.

        """
        obj = info.object
        obj.reset()
        return


@register_traitsui_widget(toolkey="Signal1D.calibrate")
@add_display_arg
def calibration_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            'left_value',
            'right_value',
            tu.Item('ss_left_value',
                    label='Left',
                    style='readonly'),
            tu.Item('ss_right_value',
                    label='Right',
                    style='readonly'),
            tu.Item(name='offset',
                    style='readonly'),
            tu.Item(name='scale',
                    style='readonly'),
            'units',),
        handler=CalibrationHandler,
        buttons=[OurApplyButton, CancelButton],
        kind='live',
        title='Calibration parameters')
    return obj, {"view": view}


@register_traitsui_widget(toolkey="interactive_range_selector")
@add_display_arg
def interactive_range_selector(obj, **kwargs):
    view = tu.View(
        tu.Item('ss_left_value', label='Left', style='readonly'),
        tu.Item('ss_right_value', label='Right', style='readonly'),
        handler=Signal1DRangeSelectorHandler,
        buttons=[OKButton, OurApplyButton, CancelButton],)
    return obj, {"view": view}


@register_traitsui_widget(toolkey="Signal1D.smooth_savitzky_golay")
@add_display_arg
def smooth_savitzky_golay_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            tu.Group(
                'window_length',
                tu.Item(
                    'decrease_window_length',
                    show_label=False),
                tu.Item(
                    'increase_window_length',
                    show_label=False),
                orientation="horizontal"),
            'polynomial_order',
            tu.Item(
                name='differential_order',
                tooltip='The order of the derivative to compute. This must '
                'be a nonnegative integer. The default is 0, which '
                'means to filter the data without differentiating.',
            ),
            # 'line_color',
        ),
        kind='live',
        handler=SmoothingHandler,
        buttons=OKCancelButtons,
        title='Savitzky-Golay Smoothing',
    )
    return obj, {"view": view}


@register_traitsui_widget(toolkey="Signal1D.smooth_lowess")
@add_display_arg
def smooth_lowess_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            'smoothing_parameter',
            'number_of_iterations',
            # 'line_color',
        ),
        kind='live',
        handler=SmoothingHandler,
        buttons=OKCancelButtons,
        title='Lowess Smoothing',)
    return obj, {"view": view}


@register_traitsui_widget(toolkey="Signal1D.smooth_total_variation")
@add_display_arg
def smooth_tv_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            'smoothing_parameter',
            # 'line_color',
        ),
        kind='live',
        handler=SmoothingHandler,
        buttons=OKCancelButtons,
        title='Total Variation Smoothing',)
    return obj, {"view": view}


@register_traitsui_widget(toolkey="Signal1D.smooth_butterworth")
@add_display_arg
def smooth_butterworth(obj, **kwargs):
    view = tu.View(
        tu.Group(
            'cutoff_frequency_ratio',
            'order',
            'type'),
        kind='live',
        handler=SmoothingHandler,
        buttons=OKCancelButtons,
        title='Butterworth filter',)
    return obj, {"view": view}


@register_traitsui_widget(toolkey="load")
@add_display_arg
def load(obj, **kwargs):
    view = tu.View(
        tu.Group('filename', "lazy"),
        kind='livemodal',
        buttons=[OKButton, CancelButton],
        title='Load file')
    return obj, {"view": view}


@register_traitsui_widget(toolkey="Signal1D.contrast_editor")
@add_display_arg
def image_constast_editor_traitsui(obj, **kwargs):
    view = tu.View(tu.Item('ss_left_value',
                           label='vmin',
                           show_label=True,
                           style='readonly',),
                   tu.Item('ss_right_value',
                           label='vmax',
                           show_label=True,
                           style='readonly'),
                   handler=ImageContrastHandler,
                   buttons=[OKButton,
                            OurApplyButton,
                            OurResetButton,
                            CancelButton, ],
                   title='Constrast adjustment tool',
                   )
    return obj, {"view": view}


@register_traitsui_widget(toolkey="Signal1D.integrate_in_range")
@add_display_arg
def integrate_in_range_traitsui(obj, **kwargs):
    view = tu.View(
        buttons=[OKButton, CancelButton],
        title='Integrate in range',
        handler=SpanSelectorInSignal1DHandler,
    )
    return obj, {"view": view}


@register_traitsui_widget(toolkey="Signal1D.remove_background")
@add_display_arg
def remove_background_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            'background_type',
            'fast',
            'zero_fill',
            tu.Group(
                'polynomial_order',
                visible_when='background_type == "Polynomial"'), ),
        buttons=[OKButton, CancelButton],
        handler=SpanSelectorInSignal1DHandler,
        title='Background removal tool',
        resizable=True,
        width=300,
    )
    return obj, {"view": view}


class SpikesRemovalHandler(tu.Handler):

    def close(self, info, is_ok):
        # Removes the span selector from the plot
        info.object.span_selector_switch(False)
        return True

    def apply(self, info, *args, **kwargs):
        """Handles the **Apply** button being clicked.

        """
        obj = info.object
        obj.is_ok = True
        if hasattr(obj, 'apply'):
            obj.apply()

        return

    def find(self, info, *args, **kwargs):
        """Handles the **Next** button being clicked.

        """
        obj = info.object
        obj.is_ok = True
        if hasattr(obj, 'find'):
            obj.find()
        return

    def back(self, info, *args, **kwargs):
        """Handles the **Next** button being clicked.

        """
        obj = info.object
        obj.is_ok = True
        if hasattr(obj, 'find'):
            obj.find(back=True)
        return


@register_traitsui_widget(toolkey="Signal1D.spikes_removal_tool")
@add_display_arg
def spikes_removal_traitsui(obj, **kwargs):

    thisOKButton = tu.Action(name="OK",
                             action="OK",
                             tooltip="Close the spikes removal tool")

    thisApplyButton = tu.Action(name="Remove spike",
                                action="apply",
                                tooltip="Remove the current spike by "
                                "interpolating\n"
                                       "with the specified settings (and find\n"
                                       "the next spike automatically)")
    thisFindButton = tu.Action(name="Find next",
                               action="find",
                               tooltip="Find the next (in terms of navigation\n"
                               "dimensions) spike in the data.")

    thisPreviousButton = tu.Action(name="Find previous",
                                   action="back",
                                   tooltip="Find the previous (in terms of "
                                   "navigation\n"
                                          "dimensions) spike in the data.")
    view = tu.View(tu.Group(
        tu.Group(
            tu.Item('click_to_show_instructions',
                    show_label=False, ),
            tu.Item('show_derivative_histogram',
                    show_label=False,
                    tooltip="To determine the appropriate threshold,\n"
                    "plot the derivative magnitude histogram, \n"
                    "and look for outliers at high magnitudes \n"
                    "(which represent sudden spikes in the data)"),
            'threshold',
            show_border=True,
        ),
        tu.Group(
            'add_noise',
            'interpolator_kind',
            'default_spike_width',
            tu.Group(
                'spline_order',
                enabled_when='interpolator_kind == "Spline"'),
            show_border=True,
            label='Advanced settings'),
    ),
        buttons=[thisOKButton,
                 thisPreviousButton,
                 thisFindButton,
                 thisApplyButton, ],
        handler=SpikesRemovalHandler,
        title='Spikes removal tool',
        resizable=False,
    )
    return obj, {"view": view}


class FindPeaks2DHandler(tu.Handler):

    def close(self, info, is_ok=False):
        obj = info.obj
        obj.signal._plot.close()
        info.obj.close(info, True)
        return True

    def compute_navigation(self, info):
        """Handles the **Compute** button being clicked.

        """
        obj = info.obj
        obj.compute_navigation()
        return


@register_traitsui_widget(toolkey="Signal2D.find_peaks2D")
@add_display_arg
def find_peaks2D_traitsui(obj, **kwargs):   
    thisCloseButton = tu.Action(name="Close",
                             action="close",
                             tooltip="Close the peaks finder tool.")

    ComputeButton = tu.Action(name="Compute over navigation axes",
                              action="compute_navigation",
                              tooltip="Find the peaks by iterating over \n"
                                "the navigation axes.")

    axis_group, context = get_navigation_sliders_group(
            obj.signal.axes_manager.navigation_axes)

    view = tu.View(
        tu.Group(
            tu.Group(axis_group,
                    tu.Item('obj.random_navigation_position',
                            show_label=False,
                            name='Set navigation index randomly',
                            tooltip='Set the navigation index to a random \n'
                              'value.',),
                    visible_when='show_navigation_sliders==True',
                    label='Navigator',
                    show_border=True),
            tu.Item('obj.method',
                    show_label=True),
            tu.Group(
                    'obj.local_max_distance',
                    'obj.local_max_threshold',
                    visible_when='obj.method == "Local max"',
                    show_border=True),
            tu.Group(
                'obj.max_alpha',
                'obj.max_size',
                visible_when='obj.method == "Max"',
                label='Method parameters',
                show_border=True),
            tu.Group(
                'obj.minmax_separation',
                'obj.minmax_threshold',
                visible_when='obj.method == "Minmax"',
                show_border=True),
            tu.Group(
                'obj.zaefferer_grad_threshold',
                'obj.zaefferer_window_size',
                'obj.zaefferer_distance_cutoff',
                visible_when='obj.method == "Zaefferer"',
                show_border=True),
            tu.Group(
                'obj.stat_alpha',
                'obj.stat_window_radius',
                'obj.stat_convergence_ratio',
                visible_when='obj.method == "Stat"',
                show_border=False),
            tu.Group(
                'obj.log_min_sigma',
                'obj.log_max_sigma',
                'obj.log_num_sigma',
                'obj.log_threshold',
                'obj.log_overlap',
                'obj.log_log_scale',
                visible_when="obj.method == 'Laplacian of Gaussian'",
                show_border=False),
            tu.Group(
                'obj.dog_min_sigma',
                'obj.dog_max_sigma',
                'obj.dog_sigma_ratio',
                'obj.dog_threshold',
                'obj.dog_overlap',
                visible_when="obj.method == 'Difference of Gaussian'",
                show_border=False),
            show_border=True),
        buttons=[ComputeButton,
                 thisCloseButton],
        handler=FindPeaks2DHandler,
        title='Find Peaks 2D',
        resizable=True,
        width=500,
    )

    context.update({"obj":obj})

    return obj, {"view": view, "context": context}
