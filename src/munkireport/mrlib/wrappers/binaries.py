"""Wrappers for binaries that are included with macOS.

All binaries will default to capturing the output of the binary and using 'utf-8' encoding for the output;
exceptions to this should be noted in the function doc string.

The default kwargs can be overridden by adding the appropriate argument, for example, to not capture output:
    system_profiler("SPHardwareDataType", capture_output=False)
or to change the encoding and not capture output:
    system_profiler("SPHardwareDataType", capture_output=False, encoding="latin1")

These default values should be sufficient for most wrapped binaries, overriding the default kwargs should be done
carefully and with a great deal of testing to ensure the output is as expected."""
import subprocess

from typing import Any, Optional

from ._internals import _default_subprocess_kwargs, _return


__all__ = [
    "airport",
    "arch",
    "assetcachelocatorutil",
    "assetcachemanagerutil",
    "codesign",
    "csrutil",
    "curl",
    "diskutil",
    "dsconfigad",
    "dsmemberutil",
    "dscl",
    "fdesetup",
    "firmwarepasswd",
    "get_uid",
    "ifconfig",
    "ioreg",
    "ipconfig",
    "lpadmin",
    "lpoptions",
    "networksetup",
    "nvram",
    "openssl",
    "pkgutil",
    "pmset",
    "powermetrics",
    "profiles",
    "ps",
    "scutil",
    "sw_vers",
    "spctl",
    "sysctl",
    "systemsetup",
    "system_profiler",
]


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def airport(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the Apple private binary 'airport' from the Apple80211 system framework.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def arch(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'arch'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/arch", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def assetcachelocatorutil(**kwargs) -> dict[str, Any]:
    """Wrapper around the sytem binary 'AssetCacheLocatorUtil'.
    Note: this binary returns output on stderr only if -j/--json is not passed to it, so this
          wrapper will always default to passing the -j/--json argument with the command, thus
          this should always return a dictionary object as the output of the function.
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/AssetCacheLocatorUtil", "--json"]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, "json", **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def assetcachemanagerutil(*args, **kwargs) -> dict[str, Any]:
    """Wrapper around the sytem binary 'AssetCacheManagerUtil'.
    Note: this binary returns output on stderr only if -j/--json is not passed to it, so this
          wrapper will always default to passing the -j/--json argument with the command, thus
          this should always return a dictionary object as the output of the function.
          The -l/--linger argument is not supported with this wrapper.
    :param **kwargs: arguments passed on to the subprocess call"""
    if "-l" in args:
        args.remove("-l")

    if "--linger" in args:
        args.remove("--linger")

    cmd = ["/usr/bin/AssetCacheLocatorUtil", "--json", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, "json", **kwargs)


@_default_subprocess_kwargs(stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
def codesign(_as_object: bool = True, *args, **kwargs) -> subprocess.CompletedProcess:
    """Wrapper around the system binary 'codesign'.
    Note: this binary returns some information on stdout and other information on stderr, so this
          will always return a subprocess.CompletedProcess object for further parsing data from.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/codesign", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def csrutil(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'csrutil'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/csrutil", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def curl(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'curl'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/curl", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def diskutil(*args, **kwargs) -> dict[str, Any] | subprocess.CompletedProcess:
    """Wrapper around the Apple system binary 'diskutil'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/diskutil", *args]
    p = subprocess.run(cmd, **kwargs)

    if any(plist in args for plist in ["-plist", "plist"]):
        return _return(p, "plist", **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def dsconfigad(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'dsconfigad'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/dsconfigad", *args]
    p = subprocess.run(cmd, **kwargs)

    if all(plist in args for plist in ["-show", "-xml"]):
        return _return(p, "plist", **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def dsmemberutil(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'dsmemberutil'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/dsmemberutil", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def dscl(*args, **kwargs) -> str | dict[str, Any] | subprocess.CompletedProcess:
    """Wrapper around the Apple system binary 'dscl'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/dscl", *args]
    p = subprocess.run(cmd, **kwargs)

    if any(plist in args for plist in ["-plist", "plist"]):
        return _return(p, "plist", **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def fdesetup(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'fdesetup'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/fdesetup", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def firmwarepasswd(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'firmwarepasswd'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/firmwarepasswd", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def get_uid(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'id'.
    Note: this wrapper uses an alternate function name as 'id' is an internal
          Python function.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/id", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def ifconfig(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'ifconfig'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/sbin/ifconfig", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def ioreg(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'ioreg'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/ioreg", *args]
    p = subprocess.run(cmd, **kwargs)

    if any(plist in args for plist in ["-a"]):
        return _return(p, "plist", **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def ipconfig(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'ipconfig'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/ipconfig", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def lpadmin(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'lpadmin'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/lpadmin", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def lpoptions(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'lpoptions'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/lpoptions", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def networksetup(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'networksetup'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/networksetup", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def nvram(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'nvram'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/nvram", *args]
    p = subprocess.run(cmd, **kwargs)

    if "-x" in args:
        return _return(p, "plist", **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def openssl(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'openssl'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/local/bin/openssl", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def pkgutil(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'pkgutil'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/pkgutil", *args]
    p = subprocess.run(cmd, **kwargs)

    if any("plist" in arg for arg in args):
        return _return(p, "plist", **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def pmset(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'pmset'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/pmset", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def powermetrics(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'powermetrics'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/powermetrics", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def profiles(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'profiles'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/profiles", *args]
    p = subprocess.run(cmd, **kwargs)

    if all(plist in args for plist in ["-output", "stdout-xml"]):
        return _return(p, "plist", **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def ps(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'ps'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/bin/ps", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def scutil(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'scutil'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/scutil", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def sw_vers(opt: Optional[str] = None, **kwargs) -> dict[str, Any] | subprocess.CompletedProcess:
    """Wrapper around the Apple system binary 'sw_vers'.
    :param opt: the valid version option to pass to the wrapped command; valid values are 'buildVersion',
                'productName', 'productVersion', 'productVersionExtra'* - *this is only present on macOS 13.x or newer
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/bin/sw_vers", opt] if opt else ["/usr/bin/sw_vers"]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def spctl(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'spctl'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/spctl", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def sysctl(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'sysctl'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/sysctl", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
def systemsetup(*args, **kwargs) -> str | subprocess.CompletedProcess:
    """Wrapper around the system binary 'systemsetup'.
    :param *args: arguments passed on to the wrapped command
    :param **kwargs: arguments passed on to the subprocess call"""
    cmd = ["/usr/sbin/systemsetup", *args]
    p = subprocess.run(cmd, **kwargs)

    return _return(p, **kwargs)


@_default_subprocess_kwargs(capture_output=True, encoding="utf-8")
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
