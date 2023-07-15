"""Wrappers for third party binaries that are optionally available.
All binaries will default to capturing the output of the binary and using 'utf-8' encoding for the output;
exceptions to this should be noted in the function doc string.

The default kwargs can be overridden by adding the appropriate argument, for example, to not capture output:
    system_profiler("SPHardwareDataType", capture_output=False)
or to change the encoding and not capture output:
    system_profiler("SPHardwareDataType", capture_output=False, encoding="latin1")

These default values should be sufficient for most wrapped binaries, overriding the default kwargs should be done
carefully and with a great deal of testing to ensure the output is as expected."""
import subprocess

from pathlib import Path
from typing import Optional

from ._internals import _default_subprocess_kwargs, _return


__all__ = ["smartctl", "smc"]


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def smartctl(*args, **kwargs) -> Optional[str | subprocess.CompletedProcess]:
    """Wrapper around the third party binary 'smartctl'.
    Note: This binary must be present at '/usr/local/sbin/smartctl'
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    smartctl_path = Path("/usr/local/sbin/smartctl")
    binary = smartctl_path if smartctl_path.exists() else None

    if binary:
        cmd = [str(binary), *args]
        p = subprocess.run(cmd, **kwargs)

        return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def smc(*args, **kwargs) -> Optional[str | subprocess.CompletedProcess]:
    """Wrapper around the third party binary 'smc'.
    Note: This binary must be present at either '/usr/local/munki/smc' or '/usr/local/munkireport/smc'
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    munki_smc = Path("/usr/local/munki/smc")
    munkireport_smc = Path("/usr/local/munkireport/smc")
    binary = munki_smc if munki_smc.exists() else munkireport_smc if munkireport_smc.exists() else None

    if binary:
        cmd = [str(binary), *args]
        p = subprocess.run(cmd, **kwargs)

        return _return(p, **kwargs)
