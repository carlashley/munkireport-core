import csv

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, MutableMapping, Optional

ReportTypes = Iterable | Mapping | MutableMapping


@dataclass
class InvalidReportFormat(Exception):
    fmt: str
    valid_fmts: list[str]

    def __str__(self) -> str:
        fmts = [f"'{ft}'" for ft in self.valid_fmts]
        suffix = f"{', '.join(fmts[0:-1])} or {fmts[-1]}" if len(fmts) > 1 else ", ".join(fmts)
        return f"Report format value {self.fmt!r} invalid, must be one of: {suffix}"


@dataclass
class MissingRequiredFieldnames(TypeError):
    func: str
    arg: str

    def __str__(self) -> str:
        return f"TypeError: {self.func} missing 1 required positional argument: {self.arg}"


class ReportWriterMixin:
    """A mixin for writing report data."""

    def _dict2csv(self, fp: Path, fn: list[str], data: list[dict[Any, Any]], _mode: str = "w", **kwargs) -> None:
        """Write a report object to a CSV file path.
        :param fp: destination as a path object
        :param fn: fieldnames (all fieldnames must be in the data object)
        :param data: list of dictionary objects to write
        :param **kwargs: additional arguments to pass on to the dictionary write"""
        with fp.open(_mode) as f:
            w = csv.DictWriter(f, fieldnames=fn, **kwargs)
            w.writeheader()

            for row in data:
                w.writerow()

    def _list2csv(self, fp: Path, data: list[Any], _mode: str = "w", **kwargs) -> None:
        """Write a report object to a CSV file path.
        :param fp: destination as a path object
        :param data: list of dictionary objects to write
        :param **kwargs: additional arguments to pass on to the dictionary write"""
        with fp.open(_mode) as f:
            w = csv.Writer(f, **kwargs)

            for row in data:
                w.writerow()

    def write_report(self, data: ReportTypes, fp: str, fmt: str, fn: Optional[list[str]] = None, **kwargs) -> None:
        """Write a report to file.
        :param data: data object to write
        :param fp: the string representing the filename of the report, this is joined to the default
                   temporary working directory path object in the MunkiReport class
        :param fmt: the format the report file takes, valid values are 'csv', 'plist'
        :param fn: optional list of fieldnames for writing a list of dictionary objects to CSV file
        :param **kwargs: additional arguments to pass on to the underlying report writer"""
        valid_fmts = ["csv", "plist"]

        if fmt not in valid_fmts:
            raise InvalidReportFormat(fmt, valid_fmts)

        fp = self.tmp_dir.joinpath(fp)

        if fmt == "csv":
            if isinstance(data, Iterable) and all(isinstance(r, (list, set, tuple)) for r in data):
                self._list2csv(fp, data, **kwargs)
            elif isinstance(data, Iterable) and all(isinstance(r, (Mapping, MutableMapping)) for r in data):
                if not fn:
                    raise MissingRequiredFieldnames("write_report", "fn")

                self._dict2csv(fp, data, fn, **kwargs)

        if fmt == "plist":
            self.write_plist(data, fp)
