import traits.api as t
import traitsui.api as tui

from hyperspy_gui_traitsui.utils import add_display_arg
from hyperspy.misc.utils import ordinal


def get_axis_label(axis):
    idx = ordinal(axis.index_in_axes_manager)
    type_ = "navigation" if axis.navigate else "signal"
    label = "{} ({}) axis".format(idx, type_)
    return label


@add_display_arg
def navigation_sliders(obj, title=None, **kwargs):
    """Raises a windows with sliders to control the index of DataAxis

    Parameters
    ----------
    obj : list of DataAxis instances

    """

    class NavigationSliders(t.HasTraits):
        pass

    nav = NavigationSliders()
    view_tuple = ()
    for axis in obj:
        name = str(axis).replace(" ", "_")
        nav.add_class_trait(name, axis)
        nav.trait_set([name, axis])
        view_tuple += (
            tui.Item(name,
                     style="custom",
                     editor=tui.InstanceEditor(
                         view=tui.View(
                             tui.Item(
                                 "index",
                                 show_label=False,
                                 # The following is commented out
                                 # due to a traits ui bug
                                 # editor=tui.RangeEditor(mode="slider"),
                             ),
                         ),
                     ),
                     ),
        )

    view = tui.View(tui.VSplit(view_tuple), title="Navigation sliders"
                    if title is None
                    else title)
    nav.trait_view("traits_view", view)
    return nav, {}


def get_navigation_sliders_group(obj):
    """Raises a windows with sliders to control the index of DataAxis

    Parameters
    ----------
    obj : list of DataAxis instances

    """
    axis_group_args = []
    context = {}

    def get_axis_label(axis):
        return (axis.name if axis.name != t.Undefined
                else f"Axis {axis.index_in_axes_manager}")

    for i, axis in enumerate(obj):
        axis_group_args.append(tui.Item(f'axis{i}.value',
                                        label=get_axis_label(axis),
                                        editor=tui.RangeEditor(
                                                low_name=f'axis{i}.low_value',
                                                high_name=f'axis{i}.high_value',
                                                label_width=28,
                                                format='%i',
                                                mode='auto')))
        context[f'axis{i}'] = axis

    axis_group = tui.Group(*axis_group_args,
                           show_border=False,)

    return axis_group, context


def _get_data_axis_view(obj):
    label = get_axis_label(obj)

    group_args = [
        tui.Item(name='name'),
        tui.Item(name='size', style='readonly'),
        tui.Item(name='index_in_array', style='readonly'),
        tui.Item(name='units'),
    ]
    cal_args = [ ]

    if obj.navigate:
        group_args.extend([
            tui.Item(name='index'),
            tui.Item(name='value', style='readonly'), ])
    if hasattr(obj, 'scale'):
        cal_args.extend([
            tui.Item(name='scale'),
            tui.Item(name='offset'), ])
    if hasattr(obj, '_expression'):
        cal_args.extend([
            tui.Item(name='_expression', style='readonly'), ])
            #tui.Item(name='_expression', style='readonly'), ]) # Add parameter of expression
        for i in obj.parameters_list:
            cal_args.extend([
                tui.Item(name=obj.parameters_list[i], style='readonly'), ])
        if hasattr(obj.x, 'scale'):
            cal_args.extend([
                tui.Item(name='x.scale'),
                tui.Item(name='x.offset'), ])

    if cal_args == [ ]:
        data_axis_view = tui.View(
            tui.Group(
                tui.Group(*group_args,
                          show_border=True,),
                # label="Data Axis properties",
                show_border=True,),
            title=label,)
    else:
        data_axis_view = tui.View(
            tui.Group(
                tui.Group(*group_args,
                          show_border=True,),
                tui.Group(*cal_args,
                          label='Calibration', show_border=True, ),
                # label="Data Axis properties",
                show_border=True,),
            title=label,)

    return data_axis_view


@add_display_arg
def data_axis_traitsui(obj, **kwargs):
    return obj, {"view": _get_data_axis_view(obj)}


def get_axis_group(n, navigate, label='', attribs = [], **kwargs):
    group_args = [
        tui.Item('axis%i.name' % n),
        tui.Item('axis%i.size' % n, style='readonly'),
        tui.Item('axis%i.index_in_array' % n, style='readonly'),
        tui.Item('axis%i.low_index' % n, style='readonly'),
        tui.Item('axis%i.high_index' % n, style='readonly'),
        tui.Item('axis%i.units' % n),
    ]
    cal_args = [ ]
    # The style of the index is chosen to be readonly because of
    # a bug in Traits 4.0.0 when using context with a Range traits
    # where the limits are defined by another traits_view
    if navigate:
        group_args.extend([
            tui.Item('axis%i.index' % n, style='readonly'),
            tui.Item('axis%i.value' % n, style='readonly'), ])
    if 'scale' in attribs:
        cal_args.extend([
            tui.Item('axis%i.scale' % n),
            tui.Item('axis%i.offset' % n), ])
    if '_expression' in attribs:
        cal_args.extend([
            tui.Item('axis%i._expression' % n, style='readonly'), ])
        for j in range(len(kwargs['parameters_list'])):
            cal_args.extend([
                tui.Item('axis{n}.{p}'.format(n = n,p = kwargs['parameters_list'][j]), label = kwargs['parameters_list'][j]), ])
        if 'xscale' in kwargs.keys():
            cal_args.extend([
                tui.Item('axis%i.x.scale' % n, label='x scale'),
                tui.Item('axis%i.x.offset' % n, label='x offset'), ])

    if cal_args == [ ]:
        group = tui.Group(
            tui.Group(*group_args,
                      show_border=True,),
            label=label,
            show_border=True,)
    else:
        group = tui.Group(
            tui.Group(*group_args,
                      show_border=True,),
            tui.Group(*cal_args,
                      label='Calibration', show_border=True, ),
            label=label,
            show_border=True,)
    return group


@add_display_arg
def axes_gui(obj, **kwargs):
    context = {}
    ag = []
    for n, axis in enumerate(obj._get_axes_in_natural_order()):
        kwargs = {}
        if hasattr(axis,'parameters_list'):
            kwargs["parameters_list"] = axis.parameters_list
            if hasattr(axis.x,'scale'):
                kwargs["xscale"] = axis.x.scale
        ag.append(get_axis_group(
            n, label=get_axis_label(axis), navigate=axis.navigate,
            attribs=axis.__dict__.keys(),**kwargs))
        context['axis%i' % n] = axis
    ag = tuple(ag)
    obj.trait_view("traits_view", tui.View(*ag, title="Axes GUI"))
    return obj, {"context": context}
