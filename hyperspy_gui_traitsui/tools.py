import traitsui
import traitsui.api as tu
from traitsui.menu import OKButton, CancelButton, OKCancelButtons

from hyperspy_gui_traitsui.axes import get_navigation_sliders_group
from hyperspy_gui_traitsui.buttons import (
    OurApplyButton,HelpButton, OurResetButton
    )
from hyperspy_gui_traitsui.utils import add_display_arg


class SmoothingHandler(tu.Handler):

    def close(self, info, is_ok):
        # Removes the span selector from the plot
        if is_ok is True:
            info.object.apply()
        else:
            info.object.close()
        return True


class LineSelectorInSignal2DHandler(tu.Handler):
    def close(self, info, is_ok):
        info.object.on = False
        if is_ok is True:
            self.apply(info)

        return True

    def close_directly(self, info):
        if (info.ui.owner is not None) and self.close(info, False):
            info.ui.owner.close()

    def apply(self, info, *args, **kwargs):
        """Handles the **Apply** button being clicked."""
        obj = info.object
        obj.is_ok = True
        if hasattr(obj, "apply"):
            obj.apply()
        return

    def next(self, info, *args, **kwargs):
        """Handles the **Next** button being clicked."""
        obj = info.object
        obj.is_ok = True
        if hasattr(obj, "next"):
            next(obj)
        return


class SpanSelectorInSignal1DHandler(tu.Handler):

    def close(self, info, is_ok):
        # Removes the span selector from the plot
        obj = info.object

        # Apply before switching off the selector
        if is_ok is True:
            self.apply(info)
        obj.span_selector_switch(False)

        if hasattr(obj, 'close'):
            obj.close()

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
        if is_ok is True:
            self.apply(info)

        # Removes the span selector from the plot
        info.object.span_selector_switch(False)

        return True

    def apply(self, info, *args, **kwargs):
        """Handles the **Apply** button being clicked.

        """
        obj = info.object
        extents = obj.span_selector.extents
        # when the traits and span extent are out of sync, which happen after
        # "apply" and before making a new selection
        if obj.ss_left_value == obj.ss_right_value or extents[0] == extents[1]:
            return

        obj.span_selector_switch(False)
        for method, cls in obj.on_close:
            method(cls, obj.ss_left_value, obj.ss_right_value)
        obj.span_selector_switch(True)

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


class Calibration2DHandler(LineSelectorInSignal2DHandler):
    def apply(self, info, *args, **kwargs):
        """Handles the **Apply** button being clicked."""
        if info.object.signal is None:
            return
        info.object.apply()
        self.close_directly(info)
        return


class ImageContrastHandler(tu.Handler):

    def close(self, info, is_ok):
        obj = info.object
        obj.close()
        return True

    def apply(self, info):
        """Handles the **Apply** button being clicked.

        """
        obj = info.object
        obj.apply()

        return

    def show_help(self, info):
        """Handles the **Help** button being clicked.

        """
        obj = info.object
        obj._show_help_fired()

        return

    def reset(self, info):
        """Handles the **Reset** button being clicked.

        """
        obj = info.object
        obj.reset()
        return


def get_spanner_left_right_items():
    """
    Return the list of items for the left and right values of the spanner.
    """
    return [tu.Item('ss_left_value',
                    label='Left',
                    style='readonly',
                    format_str='%5g',),
            tu.Item('ss_right_value',
                    label='Right',
                    style='readonly',
                    format_str='%5g',),
            ]


@add_display_arg
def calibration_traitsui(obj, **kwargs):
    spanner_items = get_spanner_left_right_items()
    view = tu.View(
        tu.Group(
            'left_value',
            'right_value',
            *spanner_items,
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


@add_display_arg
def calibration2d_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            "new_length",
            tu.Item("length", label="Current length", style="readonly"),
            tu.Item(name="scale", style="readonly"),
            "units",
        ),
        handler=Calibration2DHandler,
        buttons=[OurApplyButton, CancelButton],
        kind="live",
        title="Calibration parameters",
    )
    return obj, {"view": view}


@add_display_arg
def interactive_range_selector(obj, **kwargs):
    spanner_items = get_spanner_left_right_items()
    view = tu.View(
        *spanner_items,
        handler=Signal1DRangeSelectorHandler,
        buttons=[OKButton, OurApplyButton, CancelButton],)
    return obj, {"view": view}


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


@add_display_arg
def load(obj, **kwargs):
    view = tu.View(
        tu.Group(tu.Item('filename', editor=tu.FileEditor(dialog_style='open')),
                  "lazy"),
        kind='livemodal',
        buttons=[OKButton, CancelButton],
        title='Load file')
    return obj, {"view": view}


@add_display_arg
def image_contrast_editor_traitsui(obj, **kwargs):
    from hyperspy_gui_traitsui._external.bounds_editor import BoundsEditor

    view = tu.View(
        tu.Group(
            tu.Item('ss_left_value',
                    label='Min',
                    show_label=True,
                    style='readonly',
                    format_str='%5g',
                    ),
            tu.Item('ss_right_value',
                    label='Max',
                    show_label=True,
                    style='readonly',
                    format_str='%5g',
                    ),
            show_border=True
            ),
        tu.Group(
            tu.Item('auto',
                    label='Auto',
                    show_label=True,
                    ),
            tu.Item('percentile_range',
                    label='vmin/vmax percentile',
                    editor=BoundsEditor(
                        low_name='vmin_percentile',
                        high_name='vmax_percentile',
                        format_str='%.2f',
                        )),
            show_border=True,
            ),
        tu.Group(
            tu.Item('bins',
                    label='Bins',
                    show_label=True,
                    ),
            tu.Item('norm',
                    label='Norm',
                    show_label=True,
                    ),
            tu.Item('gamma',
                    label='Gamma',
                    show_label=True,
                    visible_when='norm == "Power"',
                    editor=tu.RangeEditor(low=0.1,
                                          high=3.,
                                          mode="slider",
                                          format_str='%.2f',
                                          ),
                    ),
            tu.Item('linthresh',
                    label='Linear threshold',
                    show_label=True,
                    visible_when='norm == "Symlog"',
                    editor=tu.RangeEditor(low=0.01,
                                          high=1.,
                                          mode="slider",
                                          format_str='%.2f',
                                          ),
                    ),
            tu.Item('linscale',
                    label='Linear scale',
                    show_label=True,
                    visible_when='norm == "Symlog"',
                    editor=tu.RangeEditor(low=0.,
                                          high=10.,
                                          mode="slider",
                                          format_str='%.2f',
                                          ),
                    ),
            show_border=True,
            ),
        tu.Item('_'),
        handler=ImageContrastHandler,
        buttons=[OKButton,
                 HelpButton,
                 OurApplyButton,
                 OurResetButton,],
        title='Contrast adjustment tool',
        resizable=True)
    return obj, {"view": view}


@add_display_arg
def remove_background_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            tu.Item('ss_left_value',
                    label='Left',
                    style='readonly',
                    format_str='%5g',
                    tooltip="Left value of the selected range.",
                    ),
            tu.Item('ss_right_value',
                    label='Right',
                    style='readonly',
                    format_str='%5g',
                    tooltip="Right value of the selected range.",
                    ),
            tu.Item('red_chisq',
                    label='red-χ²',
                    show_label=True,
                    style='readonly',
                    format_str='%5g',
                    tooltip="Reduced chi-squared of the fit in the selected range.",
                    ),
            'background_type',
            'fast',
            'zero_fill',
            tu.Group(
                'polynomial_order',
                visible_when="background_type == 'Polynomial'"), ),
        buttons=[OKButton, CancelButton],
        handler=SpanSelectorInSignal1DHandler,
        close_result=False, # is_ok=False when using window close butto.
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
            'default_spike_width',
            'spline_order',
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
        obj.close()
        return True

    def compute_navigation(self, info):
        """Handles the **Compute** button being clicked.

        """
        obj = info.obj
        obj.compute_navigation()
        obj.signal._plot.close()
        obj.close()
        info.ui.dispose()
        return


@add_display_arg
def find_peaks2D_traitsui(obj, **kwargs):
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
                tu.Item('obj.local_max_distance', label='Distance'),
                tu.Item('obj.local_max_threshold', label='Threshold'),
                visible_when='obj.method == "Local max"',
                label='Method parameters',
                show_border=True),
            tu.Group(
                tu.Item('obj.max_alpha', label='Alpha'),
                tu.Item('obj.max_distance', label='Distance'),
                visible_when='obj.method == "Max"',
                label='Method parameters',
                show_border=True),
            tu.Group(
                tu.Item('obj.minmax_distance', label='Distance'),
                tu.Item('obj.minmax_threshold', label='Threshold'),
                visible_when='obj.method == "Minmax"',
                label='Method parameters',
                show_border=True),
            tu.Group(
                tu.Item('obj.zaefferer_grad_threshold', label='Grad threshold'),
                tu.Item('obj.zaefferer_window_size', label='Window size'),
                tu.Item('obj.zaefferer_distance_cutoff', label='Distance cutoff'),
                visible_when='obj.method == "Zaefferer"',
                label='Method parameters',
               show_border=True),
            tu.Group(
                tu.Item('obj.stat_alpha', label='Alpha'),
                tu.Item('obj.stat_window_radius', label='Window radius'),
                tu.Item('obj.stat_convergence_ratio', label='Convergence ratio'),
                visible_when='obj.method == "Stat"',
                label='Method parameters',
                show_border=True),
            tu.Group(
                tu.Item('obj.log_min_sigma', label='Min sigma'),
                tu.Item('obj.log_max_sigma', label='Max sigma'),
                tu.Item('obj.log_num_sigma', label='Num sigma'),
                tu.Item('obj.log_threshold', label='Threshold'),
                tu.Item('obj.log_overlap', label='Overlap'),
                tu.Item('obj.log_log_scale', label='Log scale'),
                visible_when="obj.method == 'Laplacian of Gaussian'",
                label='Method parameters',
                show_border=True),
            tu.Group(
                tu.Item('obj.dog_min_sigma', label='Min sigma'),
                tu.Item('obj.dog_max_sigma', label='Max sigma'),
                tu.Item('obj.dog_sigma_ratio', label='Sigma ratio'),
                tu.Item('obj.dog_threshold', label='Threshold'),
                tu.Item('obj.dog_overlap', label='Overlap'),
                visible_when="obj.method == 'Difference of Gaussian'",
                label='Method parameters',
                show_border=True),
            tu.Group(
                tu.Item('obj.xc_distance', label='Distance'),
                tu.Item('obj.xc_threshold', label='Threshold'),
                visible_when="obj.method == 'Template matching'",
                label='Method parameters',
                show_border=True),
            show_border=True),
        buttons=[ComputeButton,
                 CancelButton],
        handler=FindPeaks2DHandler,
        title='Find Peaks 2D',
        resizable=True,
        width=500,
    )

    context.update({"obj":obj})

    return obj, {"view": view, "context": context}
