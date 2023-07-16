from packaging.version import Version

from ..wrappers.binaries import scutil, sw_vers


class SystemAttrsMixin:
    """A mixin for system attributes, such as OS versions, architecture type, etc."""

    @property
    def is_apple_silicon(self) -> bool:
        """Returns a boolean value indicating the platform is Apple Silicon or not."""
        result = scutil("-in", "hw.optional.arm64")

        if result:
            return int(result) == 1
        return False

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
