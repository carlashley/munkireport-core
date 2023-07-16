from typing import Any, Iterable, Mapping, Optional

from .. import MunkiReport
from ..wrappers.binaries import system_profiler


class ApplicationsReport(MunkiReport):
    """Applications Report."""

    # Map the attributes that objects in the system_profiler output will have to the
    # attribute names required in Munki Report; the key is the system_profiler key
    # and the value is the value that is used when submiting the data to Munki Report.
    _SP_APPLICATION_ATTRS_MAP: dict[str, str] = {
        "_name": "name",
        "arch": "arch",
        "arch_kind": "arch",
        "info": "info",
        "lastModified": "last_modified",
        "obtained_from": "obtained_from",
        "path": "path",
        "runtime_environment": "runtime_environment",
        "signed_by": "signed_by",
        "version": "version",
    }

    # Internal use only, attributes to look for to determine an app has 64bit code.
    _ARCH_64_VALUES: list[str] = [
        "arch_i64",
        "arch_i32_i64",
        "arch_arm_i64",
    ]

    def __init__(self, dry_run: bool) -> None:
        self.report_fn = "applications.plist"
        super().__init__(dry_run)

    def _app_has_64bit_code(self, app_dict: Mapping[Any, Any], _intel: str = "has64BitIntelCode") -> int:
        """Return an int boolean representation of an application dictionary object if it has
        Intel 64bit code or ARM 64 bit code.
        :param app_dict: a mapping object, typically a dictionary, representing attributes of an
                         application as parsed from the system_profiler SPApplicationsDataType"""
        intel64 = app_dict.get(_intel, "no")
        arch64 = app_dict.get("arch_kind")

        if intel64 == "yes" or (arch64 and arch64 in self._ARCH_64_VALUES):
            return 1
        return 0

    def report_data(self) -> Optional[Iterable[Mapping]]:
        """Parses the output of the system_profiler with respect to the specified data type.
        :param dt: data type string to pass to the system_profiler call"""
        result = []
        dt = "SPApplicationsDataType"
        applications = system_profiler(dt).get(dt, [])

        for app in applications:
            data = {"has64bit": self._app_has_64bit_code(app)}

            for sp_key, db_attr in self._SP_APPLICATION_ATTRS_MAP.items():
                if sp_key == "signed_by":
                    value = "; ".join(app.get(sp_key))

                data[sp_key] = value

            result.append(data)

        return result
