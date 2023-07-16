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

    def clean_dict(self, d: MutableMapping[Any, Any]) -> dict[Any, Any]:
        """Cleans out 'None' values in a dictionary.
        :param d: dictionary object to clean"""
        result = {}

        for k, v in d.items():
            if isinstance(v, dict):
                new_v = self.clean_dict(d=v)

                if len(new_v) > 0:
                    result[k] = new_v
            elif isinstance(v, list):
                new_v = []

                for elem in v:
                    if isinstance(elem, dict):
                        new_d = self.clean_dict(d=elem)

                        if len(new_d) > 0:
                            new_v.append(new_d)
                    elif elem is not None and not elem == "":
                        new_v.append(elem)
                result[k] = new_v
            elif isinstance(v, tuple):
                new_t = []

                for elem in v:
                    if isinstance(elem, dict):
                        new_d = self.clean_dict(d=elem)

                        if len(new_d) > 0:
                            new_t.append(new_d)
                    elif elem is not None and not elem == "":
                        new_t.append(elem)
                result[k] = tuple(new_t)
            elif isinstance(v, set):
                new_s = set()

                for elem in v:
                    if isinstance(elem, dict):
                        new_d = self.clean_dict(d=elem)

                        if len(new_d) > 0:
                            new_s.append(new_d)
                    elif elem is not None and not elem == "":
                        new_s.add(elem)
                result[k] = new_s
            elif not isinstance(v, (dict, list, tuple, set)) and v is not None or not v == "":
                result[k] = v

        return result

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

    def read_plist(self, fp: Path, _mode: str = "rb") -> MutableMapping[Any, Any]:
        """Convenience function for reading property list files.
        :param fp: file path object"""
        with fp.open(_mode) as f:
            return plistlib.load(f)

    def read_plist_string(self, b: bytes) -> MutableMapping[Any, Any]:
        """Convenience function for reading property list data from a bytestring.
        :param b"""
        return plistlib.loads(b)

    def write_plist(self, d: Mapping[Any, Any], fp: Path, _mode: str = "wb") -> None:
        """Convenience function for writing property list files.
        :param d: mapping object to write (for example, a dictionary)
        :param fp: file path object"""
        with fp.open(_mode) as f:
            return plistlib.dump(f)
