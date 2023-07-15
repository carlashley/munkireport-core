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

from pathlib import Path
from typing import Any, Optional

from . import _default_kwargs


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
def curl(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'curl'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/curl", *args]
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
def dscl(*args, **kwargs) -> str | dict[str, Any] | subprocess.CompletedProcess:
    """Wrapper around the Apple system binary 'dscl'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/dscl", *args]
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
def get_uid(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'id'.
    Note: this wrapper uses an alternate function name as 'id' is an internal
          Python function.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/id", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def ioreg(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'ioreg'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/ioreg", *args]
    p = subprocess.run(cmd, **kwargs)

    if any(plist in args for plist in ["-a"]):
        return _return(p, "plist", **kwargs)

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
def networksetup(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'networksetup'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/networksetup", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def pmset(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'pmset'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/pmset", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def powermetrics(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'powermetrics'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/powermetrics", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def profiles(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'profiles'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/profiles", *args]
    p = subprocess.run(cmd, **kwargs)

    if all(plist in args for plist in ["-output", "stdout-xml"]):
        return _return(p, "plist", **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def ps(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'ps'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/bin/ps", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def scutil(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'scutil'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/scutil", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_kwargs(capture_output=True, encoding="utf-8")
def smc(*args, **kwargs) -> Optional[str | subprocess.CompletedProcess]:
    """Wrapper around the third party binary 'smc'.
    Note: This binary must be present at either '/usr/local/munki/smc' or '/usr/local/munkireport/smc'
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    munki_smc = Path("/usr/local/munki/smc")
    munkireport_smc = Path("/usr/local/munkireport/smc")
    binary = munki_smc if munki_smc.exists() else munkireport_smc if munkireport_smc.exists() else None

    if binary:
        cmd = [binary, *args]
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
def sysctl(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'sysctl'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/sysctl", *args]
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
