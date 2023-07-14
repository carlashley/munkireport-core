"""System binary wrappers.
All binaries will default to capturing the output of the binary and using 'utf-8' encoding for the output.

The default kwargs can be overridden by adding the appropriate argument, for example, to not capture output:
    system_profiler("SPHardwareDataType", capture_output=False)
or to change the encoding and not capture output:
    system_profiler("SPHardwareDataType", capture_output=False, encoding="latin1")

These default values should be sufficient for most wrapped binaries, overriding the default kwargs should be done
carefully and with a great deal of testing to ensure the output is as expected."""
import json
import plistlib
import subprocess
import sys

from functools import wraps
from typing import Any, Callable, Optional


def _default_kwargs(**_kwargs):
    """A private decorator for providing default kwarg values to wrapper functions."""

    def outer_decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def inner(*args, **kwargs) -> Any:
            _kwargs.update(kwargs)

            return fn(*args, **_kwargs)

        return inner

    return outer_decorator


def _return(p: subprocess.CompletedProcess, _in: Optional[str] = None, **kwargs) -> Any | subprocess.CompletedProcess:
    """Basic test and return method for returning a completed subprocess object or the capture stdout/stderr.
    :param p: a subprocess.CompletedProcess instance
    :param **kwargs: the kwargs passed to the subprocess call"""
    if p.returncode == 0:
        if kwargs.get("capture_output"):
            if _in == "plist":
                return plistlib.loads(p.stdout.encode() if not isinstance(p.stdout, bytes) else p.stdout)
            elif _in == "json":
                return json.loads(p.stdout.strip())
            else:
                return p.stdout.strip()

        return p
    print(f"Error [{p.returncode}]: {p.stderr.strip()}", file=sys.stderr)


@_default_kwargs(capture_output=True, encoding="utf-8")
def airport(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the Apple private binary 'airport' from the Apple80211 system framework.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def diskutil(*args, **kwargs) -> dict[str, Any] | subprocess.CompletedProcess:
    """Wrapper around the Apple system binary 'diskutil'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/diskutil", *args]
    p = subprocess.run(cmd, **kwargs)

    if any(plist in args for plist in ["-plist", "plist"]):
        return _return(p, "plist", **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def fdesetup(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'fdesetup'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/fdesetup", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def lpadmin(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'lpadmin'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/lpadmin", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def lpoptions(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'lpoptions'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/lpoptions", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def sw_vers(opt: Optional[str] = None, **kwargs) -> dict[str, Any] | subprocess.CompletedProcess:
    """Wrapper around the Apple system binary 'sw_vers'.
    :param opt: the valid version option to pass to the wrapped command; valid values are 'buildVersion',
                'productName', 'productVersion', 'productVersionExtra'* - *this is only present on macOS 13.x or newer
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/sw_vers", opt] if opt else ["/usr/bin/sw_vers"]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def system_profiler(dt: str, **kwargs) -> dict[str, Any] | subprocess.CompletedProcess:
    """Wrapper around the Apple system binary 'system_profiler'.
    Note: this is implemented using the -json flag which was only added to macOS in macOS 10.15 (Catalina),
          therefore the minimum macOS version that this wrapper is supported on is macOS 10.15; this is a deliberate
          implementation choice and will not be changed to output XML.
    :param dt: the data type value to pass to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/system_profiler", "-detaillevel", "full", "-json", dt]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, "json", **kwargs)
