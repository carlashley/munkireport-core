from typing import Any, Iterable, Mapping, Optional

from .. import MunkiReport
from ..wrappers.binaries import system_profiler


class DisplaysReport(MunkiReport):
    """Displays Report."""

    # Map the attributes that objects in the system_profiler output will have to the
    # attribute names required in Munki Report; the key is the system_profiler key
    # and the value is the value that is used when submiting the data to Munki Report.
    # Graphics card
    _SP_GRAPHICS_ATTRS_MAP: dict[str, str] = {
        "_name": "name",
        "spdisplays_mtlgpufamilysupport": "metal_support",
        "spdisplays_vendor": "vendor",
        "sppci_bus": "bus",
        "sppci_cores": "gpu_cores",
        "sppci_device_type": "device_type",
        "sppci_model": "model",
    }

    # Attached displays
    _SP_DISPLAYS_ATTRS_MAP: dict[str, str] = {
        "_name": "name",
        "_spdisplays_display-serial-number": "display_serial",
        "_spdisplays_display-week": "mfg_week",
        "_spdisplays_display-year": "mfg_year",
        "_spdisplays_displayID": "display_id",
        "_spdisplays_virtualdevice": "virtual_device",
        "spdisplays_main": "main_display",
        "spdisplays_online": "is_online",
        "spdisplays_pixelresolution": "pixel_resolution",
        "spdisplays_resolution": "resolution",
    }

    def __init__(self, dry_run: bool) -> None:
        self.report_fn = "displays.plist"
        super().__init__(dry_run)

        self._localisation_strings = self.read_system_profiler_localisation("SPDisplaysReporter.spreporter")

    def _parse_graphics_or_displays(self, d: Mapping[Any, Any], attrs_map: Mapping[Any, Any]) -> Mapping[Any, Any]:
        """Parse details from the output of system_profiler with respect to the specified data type.
        :param d: dictionary object from system_profiler output
        :param attrs_map: dictionary object of attributes mapped from system_profiler output to database column
                          names"""
        result = {}

        for key, val in d.items():
            if key in attrs_map:
                new_key = attrs_map.get(key, key)

                try:
                    result[new_key] = self._localisation_strings[self.locale][val]
                except (KeyError, TypeError):  # not all values are localised or need to be
                    result[new_key] = val

        return result

    def _parse_displays(self, d: Mapping[Any, Any]) -> Mapping[Any, Any]:
        """Parse display device details from the output of system_profiler with respect to the specified data type.
        :param d: dictionary object from system_profiler output"""
        return self._parse_graphics_or_displays(d, self._SP_DISPLAYS_ATTRS_MAP)

    def _parse_graphics(self, d: Mapping[Any, Any]) -> Mapping[Any, Any]:
        """Parse graphic device details from the output of system_profiler with respect to the specified data type.
        :param d: dictionary object from system_profiler output"""
        return self._parse_graphics_or_displays(d, self._SP_GRAPHICS_ATTRS_MAP)

    def report_data(self) -> Optional[Iterable[Mapping]]:
        """Parses the output of the system_profiler with respect to the specified data type."""
        result = []
        dt = "SPDisplaysDataType"
        graphics_displays = system_profiler(dt).get(dt, [])

        # Note, each graphics object will have a list of displays attached to it in the 'spdisplays_ndrvs' key
        for gfx_item in graphics_displays:
            graphics = self._parse_graphics(gfx_item)
            graphics["displays"] = [self._parse_displays(disp) for disp in gfx_item.get("spdisplays_ndrvs", [])]
            result.append(graphics)

        return result
