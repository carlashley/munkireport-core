import plistlib

from collections import OrderedDict
from pathlib import Path
from typing import Any, Mapping, MutableMapping


class UtilsMixin:
    """A mixin for various utilities."""

    def bool2int(self, b: bool) -> int:
        """Convert a boolean to 1 (True) or 0 (False).
        :param b: boolean value"""
        return 1 if b else 0

    def flat_dict(self, d: MutableMapping[Any, Any], sep: str = ".", parent: str = "") -> dict[Any, Any]:
        """Return a flat dictionary. Sub keys are merged with parent key and separated with the
        provided separator string value to avoid key name collisions.
        :param d: dictionary object to flatten
        :param sep: string value to use as the separator between parent and child keys; default is '.'
        :param parent: the current parent key, on the initial call the default is an empty string"""
        result = {}

        for key, val in d.items():
            if val and isinstance(val, (dict, OrderedDict)):
                new_parent = f"{parent}{key}{sep}"
                deeper = self.flat_dict(val, sep=sep, parent=new_parent)
                result.update({_key: _val for _key, _val in deeper.items()})
            elif val and isinstance(val, (list, set, tuple)):
                for index, sub_iter in enumerate(val, start=1):
                    if sub_iter and isinstance(sub_iter, (dict, OrderedDict)):
                        new_parent = f"{parent}{key}{sep}{str(index)}{sep}"
                        deeper = self.flat_dict(d=sub_iter, sep=sep, parent=new_parent)
                        result.update({_key: _val for _key, _val in deeper.items()})
                    else:
                        new_parent = f"{parent}{key}{sep}{str(index)}"
                        result[new_parent] = val
            else:
                result[f"{parent}{key}"] = val

        return result

    def read_plist(self, fp: Path, _mode: str = "rb", **kwargs) -> MutableMapping[Any, Any]:
        """Convenience function for reading property list files.
        :param fp: file path object
        :param **kwargs: additional arguments to pass on to the plistlib call"""
        with fp.open(_mode) as f:
            return plistlib.load(f)

    def read_plist_string(self, b: bytes, **kwargs) -> MutableMapping[Any, Any]:
        """Convenience function for reading property list data from a bytestring.
        :param b
        :param **kwargs: additional arguments to pass on to the plistlib call"""
        return plistlib.loads(b, **kwargs)

    def write_plist(self, d: Mapping[Any, Any], fp: Path, _mode: str = "wb", **kwargs) -> None:
        """Convenience function for writing property list files.
        Note: when writing a property list file as an XML format property list (default behaviour),
              the 'plistlib.dump' method will raise a 'TypeError' if _any_ value is 'None' or contains 'None',
              for example, a list with a 'None' value will raise this error just as a key with a 'None' value;
              the binary property list format does not share the same limitation. Forcing the 'plistlib.dump'
              method to output a binary property list file is achieved by using the 'fmt=plistlib.FMT_BINARY'
              parameter.
        :param d: mapping object to write (for example, a dictionary)
        :param fp: file path object
        :param **kwargs: additional arguments to pass on to the plistlib call"""
        with fp.open(_mode) as f:
            return plistlib.dump(d, f, **kwargs)
