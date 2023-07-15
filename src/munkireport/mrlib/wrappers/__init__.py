"""Internal functions for wrapper usage"""
from functools import wraps
from typing import Any, Callable


def _default_kwargs(**_kwargs):
    """A private decorator for providing default kwarg values to wrapper functions."""

    def outer_decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def inner(*args, **kwargs) -> Any:
            _kwargs.update(kwargs)

            return fn(*args, **_kwargs)

        return inner

    return outer_decorator
