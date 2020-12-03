import traitsui.api as tu

from hyperspy_gui_traitsui.utils import add_display_arg


@add_display_arg
def span_roi_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            tu.Item('left',
                    label='Left',
                    format_str='%5g',),
            tu.Item('right',
                    label='Right',
                    format_str='%5g',),
            ),
        )
    return obj, {"view": view}


@add_display_arg
def point1d_roi_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            tu.Item('value',
                    label='value',
                    format_str='%5g',),
            ),
        )
    return obj, {"view": view}


@add_display_arg
def point2d_roi_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            tu.Item('x',
                    label='x',
                    format_str='%5g',),
            tu.Item('y',
                    label='y',
                    format_str='%5g',),
            ),
        )
    return obj, {"view": view}


@add_display_arg
def rectangular_roi_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            tu.Item('left',
                    label='Left',
                    format_str='%5g',),
            tu.Item('right',
                    label='Right',
                    format_str='%5g',),
            tu.Item('top',
                    label='Top',
                    format_str='%5g',),
            tu.Item('bottom',
                    label='Bottom',
                    format_str='%5g',),
            ),
        )
    return obj, {"view": view}


@add_display_arg
def circle_roi_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            tu.Item('cx',
                    label='x',
                    format_str='%5g',),
            tu.Item('cy',
                    label='y',
                    format_str='%5g',),
            tu.Item('r',
                    label='Radius',
                    format_str='%5g',),
            # Not working r_innner is explicitly defined.
            # tu.Item('r_inner',
            #         label='Inner radius',),
            ),
        )
    return obj, {"view": view}


@add_display_arg
def line2d_roi_traitsui(obj, **kwargs):
    view = tu.View(
        tu.Group(
            tu.Item('x1',
                    label='x1',
                    format_str='%5g',),
            tu.Item('y1',
                    label='y1',
                    format_str='%5g',),
            tu.Item('x2',
                    label='x2',
                    format_str='%5g',),
            tu.Item('y2',
                    label='y2',
                    format_str='%5g',),
            tu.Item('linewidth',
                    label='linewidth',
                    format_str='%5g',),
            ),
        )
    return obj, {"view": view}
