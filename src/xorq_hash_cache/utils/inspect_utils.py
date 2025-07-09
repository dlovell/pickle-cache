import inspect

import toolz


def get_enclosing_function(level=2):
    # let caller inspect it's caller's name with level=2
    return inspect.stack()[level].function


def maybe_unwrap(func, *args, **kwargs):
    if (
        hasattr(func, "func")
        and hasattr(func, "args")
        and hasattr(func, "keywords")
        and isinstance(func.args, tuple)
    ):
        _kwargs = {}
        if func.keywords:
            _kwargs.update(func.keywords)
        _kwargs.update(kwargs)
        kwargs = _kwargs
        args = func.args + args
        func = func.func
    elif hasattr(func, "func"):
        func = func.func
    return (func, args, kwargs)


def get_args_kwargs(f, *args, **kwargs):
    (f, args, kwargs) = maybe_unwrap(f, *args, **kwargs)
    signature = inspect.signature(f)
    bound = signature.bind(*args, **kwargs)
    bound.apply_defaults()
    return (bound.args, bound.kwargs)


def get_arguments(f, *args, **kwargs):
    (f, args, kwargs) = maybe_unwrap(f, *args, **kwargs)
    signature = inspect.signature(f)
    bound = signature.bind(*args, **kwargs)
    bound.apply_defaults()
    arguments = bound.arguments
    return arguments


def get_partial_arguments(f, *args, **kwargs):
    (f, args, kwargs) = maybe_unwrap(f, *args, **kwargs)
    signature = inspect.signature(f)
    bound = signature.bind_partial(*args, **kwargs)
    bound.apply_defaults()
    arguments = bound.arguments
    return arguments


@toolz.curry
def partial_args_match(f, pargs, pkwargs, args, kwargs):
    _pkwargs = get_partial_arguments(f, *pargs, **pkwargs)
    _kwargs = get_arguments(f, *args, **kwargs)
    return toolz.merge(_kwargs, _pkwargs) == _kwargs
