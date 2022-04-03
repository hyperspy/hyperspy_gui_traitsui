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
                                                format_str='%5g',
                                                mode='auto')))
        context[f'axis{i}'] = axis

    axis_group = tui.Group(*axis_group_args,
                           show_border=False,)

    return axis_group, context


@add_display_arg
def axis_gui(obj, **kwargs):
    context = {'axis0': obj}
    kwargs = {}
    if hasattr(obj, 'parameters_list'):
        kwargs["parameters_list"] = obj.parameters_list
        if hasattr(obj.x, 'scale'):
            kwargs["xscale"] = obj.x.scale
    ag = get_axis_group(n=0,
                        navigate=obj.navigate,
                        attribs=obj.__dict__.keys(),
                        **kwargs
                        )
    obj.trait_view("traits_view", tui.View(ag, title="Axis GUI"))
    return obj, {"context": context}


def get_axis_group(n, navigate, label='', attribs=[], **kwargs):
    group_args = [
        tui.Item(f'axis{n}.name'),
        tui.Item(f'axis{n}.size', style='readonly'),
        tui.Item(f'axis{n}.index_in_array', style='readonly'),
        tui.Item(f'axis{n}.low_index', style='readonly'),
        tui.Item(f'axis{n}.high_index', style='readonly'),
        tui.Item(f'axis{n}.units'),
    ]
    cal_args = [ ]
    if 'is_binned' in attribs:
        group_args.append(tui.Item(f'axis{n}.is_binned'))
    if navigate:
        group_args.extend([
            tui.Item(f'axis{n}.index', editor=tui.RangeEditor(
                                                low_name=f'axis{n}.low_index',
                                                high_name=f'axis{n}.high_index',
                                                label_width=28,
                                                format_str='%i',
                                                mode='auto')),
            tui.Item(f'axis{n}.value', style='readonly', format_str='%5g'), ])
    if 'scale' in attribs:
        cal_args.extend([
            tui.Item(f'axis{n}.scale'),
            tui.Item(f'axis{n}.offset'), ])
    if '_expression' in attribs:
        cal_args.extend([
            tui.Item(f'axis{n}._expression', style='readonly'), ])
        for j in range(len(kwargs['parameters_list'])):
            p = kwargs['parameters_list'][j]
            cal_args.extend([
                tui.Item(f'axis{n}.{p}', label=p), ])
        if 'xscale' in kwargs.keys():
            cal_args.extend([
                tui.Item(f'axis{n}.x.scale', label='x scale'),
                tui.Item(f'axis{n}.x.offset', label='x offset'), ])

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
        if hasattr(axis, 'parameters_list'):
            kwargs["parameters_list"] = axis.parameters_list
            if hasattr(axis.x, 'scale'):
                kwargs["xscale"] = axis.x.scale
        ag.append(get_axis_group(
            n, label=get_axis_label(axis), navigate=axis.navigate,
            attribs=axis.__dict__.keys(), **kwargs))
        context[f'axis{n}'] = axis
    ag = tuple(ag)
    obj.trait_view("traits_view", tui.View(*ag, title="Axes GUI"))
    return obj, {"context": context}
