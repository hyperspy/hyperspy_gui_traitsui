import functools



def add_display_arg(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        display = kwargs.pop("display", True)
        obj, kwargs = f(*args, **kwargs)
        if display:
            obj.edit_traits(**kwargs)
            return None
        else:
            return obj
    return wrapper
