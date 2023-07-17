import os
import re

from packaging.version import Version

from ..wrappers.binaries import scutil, sw_vers


class SystemAttrsMixin:
    """A mixin for system attributes, such as OS versions, architecture type, etc."""

    @property
    def cpu_arch(self) -> str:
        """Return the platform architecture type. Uses the version string of os.uname().version and
        a regex pattern to parse the actual architecture type as binaries can be executed with the
        arch binary to run in arm64/x86_64/etc via use of applicable arch param."""
        pattern = re.compile(r"RELEASE_\w+\d+_|RELEASE\w+_\d+")
        return "".join(pattern.findall(os.uname().version)).lower().removeprefix("release_").removesuffix("_")

    @property
    def darwin_version(self) -> Version:
        """Return a version object instance of the Darwin kernel release number."""
        v = os.uname().release
        return self.str2vers(v)

    @property
    def is_apple_silicon(self) -> bool:
        """Returns a boolean value indicating the platform is Apple Silicon or not."""
        result = scutil("-in", "hw.optional.arm64")

        if result:
            return int(result) == 1
        return False

    @property
    def locale(self) -> str:
        """Return the system locale value from the 'LANG' environment; defaults to 'en' if no export is found."""
        return os.environ.get("LANG", "en").partition(".")[0]

    @property
    def os_build(self) -> Version:
        """Returns the OS build only, for example: '22F66'"""
        v = sw_vers("-buildVersion")
        return self.str2vers(v)

    @property
    def os_name(self) -> Version:
        """Returns the OS name value only, for example: 'macOS'"""
        v = sw_vers("-productName")
        return v

    @property
    def os_rsr(self) -> Version:
        """Returns the OS rapid security release version only, for example: 'a'"""
        v = sw_vers("-productVersionExtra")
        return self.str2vers(v)

    @property
    def os_version(self) -> Version:
        """Returns the OS version only, for example: '13.4'"""
        v = sw_vers("-productVersion")
        return self.str2vers(v)
