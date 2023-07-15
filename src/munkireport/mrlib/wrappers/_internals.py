"""Internal wrapper functions only. No direct useage."""
import json
import plistlib
import subprocess
import sys

from functools import wraps
from typing import Any, Callable, Optional


def _default_subprocess_kwargs(**_kwargs):
    """A private decorator for providing default kwarg values to wrapper functions."""

    def outer_decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def inner(*args, **kwargs) -> Any:
            _kwargs.update(kwargs)

            return fn(*args, **_kwargs)

        return inner

    return outer_decorator


def _return(
    p: subprocess.CompletedProcess,
    fmt: Optional[str] = None,
    sc: Optional[int] = 0,
    ec: Optional[int] = None,
    **kwargs,
) -> Any | subprocess.CompletedProcess:
    """Basic test and return method for returning a completed subprocess object or the capture stdout/stderr.
    :param p: a subprocess.CompletedProcess instance
    :param fmt: use 'json' or 'plist' to indicate the stdout format type, default is None (returns stdout as is),
                'json' or 'plist' values return a native dictionary object
    :param sc: specify the returncode value to use indicating a successful process call; default is 0
    :param ec: specify the returncode value to use indicating a failed process call; default is None
    :param **kwargs: the kwargs passed to the subprocess call"""
    valid_fmts = ["json", "plist"]

    if fmt and fmt not in valid_fmts:
        raise ValueError(f"{fmt!r} is not a valid value from {valid_fmts}")

    if p.returncode == sc:
        if kwargs.get("capture_output"):
            if fmt == "plist":
                return plistlib.loads(p.stdout.encode() if not isinstance(p.stdout, bytes) else p.stdout)
            elif fmt == "json":
                return json.loads(p.stdout.strip())
            else:
                return p.stdout.strip()

        return p
    if (ec and p.returncode == ec) or not p.returncode == sc:
        print(f"Error [{p.returncode}]: {p.stderr.strip()}", file=sys.stderr)
    print(f"Error [{p.returncode}]: {p.stderr.strip()}", file=sys.stderr)
