from os import geteuid
from packaging.version import parse, Version
from typing import Optional

from ..wrappers.binaries import scutil, sw_vers


class VersioningMixin:
    """A mixin for version parsing."""

    def str2vers(self, v: str) -> Version:
        """Convert a string representation of a version to a 'packaging.Version' instance.
        :param v: string representation of a version value"""
        return parse(v)


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


class CurrentUserMixin:
    """A mixin for current user information, such as effective uid, etc."""

    @property
    def current_uid(self) -> Optional[int]:
        """Returns the current user id value if there is a currently logged in user."""
        return geteuid()

    @property
    def has_current_user(self) -> Optional[str]:
        """Returns a boolean value indicating a user is logged in.
        Note: ignores any usernames that start with '_', this typically denotes a service
              account."""
        data = scutil(input="show State:/Users/ConsoleUser")

        if data:
            for line in [ln.strip() for ln in data.splitlines()]:
                if line.startswith("Name : "):
                    username = line.removeprefix("Name : ").strip()

                    if username:
                        return not username == "" or not username.startswith("_")

    @property
    def is_root(self) -> bool:
        """Returns a boolean value indicating the current user is root or not."""
        return geteuid() == 0
