from packaging.version import parse, Version


class Versioning:
    def str2vers(self, v: str) -> Version:
        """Convert a string representation of a version to a 'packaging.Version' instance.
        :param v: string representation of a version value"""
        return parse(v)
