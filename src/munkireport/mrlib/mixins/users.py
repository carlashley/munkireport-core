from os import geteuid
from typing import Optional

from ..wrapers.binaries import scutil


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
