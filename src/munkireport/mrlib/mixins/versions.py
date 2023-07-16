from packaging.version import parse, Version


class VersioningMixin:
    """A mixin for version parsing."""

    def float2vers(self, v: float) -> Version:
        """Convert an int representation of a version to a 'packaging.Version' instance.
        :param v: string representation of a version value"""
        return parse(str(v))

    def int2vers(self, v: int) -> Version:
        """Convert an int representation of a version to a 'packaging.Version' instance.
        :param v: string representation of a version value"""
        return parse(str(v))

    def str2vers(self, v: str) -> Version:
        """Convert a string representation of a version to a 'packaging.Version' instance.
        :param v: string representation of a version value"""
        return parse(v)
