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

    # Attached displays, includes displayport items nested in 'spdisplays_ndrvs'
    _SP_DISPLAYS_ATTRS_MAP: dict[str, str] = {
        "_name": "model",
        "_spdisplays_EDR_Enabled": "edr_enabled",
        "_spdisplays_EDR_Limit": "edr_limit",
        "_spdisplays_EDR_Supported": "edr_supported",
        "_spdisplays_display-serial-number": "display_serial",
        "_spdisplays_pixels": "native",
        "_spdisplays_resolution": "ui_resolution",
        "display_type": "display_type",
        "manufactured": "manufactured",
        "retina": "retina",
        "spdisplays_ambient_brightness": "ambient_brightness",
        "spdisplays_asleep": "display_asleep",
        "spdisplays_automatic_graphics_switching": "automatic_graphics_switching",
        "spdisplays_builtin": "type",
        "spdisplays_connection_type": "connection_type",
        "spdisplays_depth": "color_depth",
        "spdisplays_display_type": "display_type",
        "spdisplays_displayport_adapter_firmware_version": "dp_adapter_firmware_version",
        "spdisplays_displayport_current_bandwidth": "dp_current_bandwidth",
        "spdisplays_displayport_current_lanes": "dp_current_lanes",
        "spdisplays_displayport_current_spread": "dp_current_spread",
        "spdisplays_displayport_dpcd_version": "dp_dpcd_version",
        "spdisplays_displayport_hdcp_capability": "dp_hdcp_capability",
        "spdisplays_displayport_max_bandwidth": "dp_max_bandwidth",
        "spdisplays_displayport_max_lanes": "dp_max_lanes",
        "spdisplays_displayport_max_spread": "dp_max_spread",
        "spdisplays_dynamic_range": "dynamic_range",
        "spdisplays_interlaced": "interlaced",
        "spdisplays_main": "main_display",
        "spdisplays_mirror": "mirror",
        "spdisplays_mirror_status": "mirror_status",
        "spdisplays_online": "online",
        "spdisplays_resolution": "resolution",
        "spdisplays_rotation": "rotation_supported",
        "spdisplays_television": "television",
        "type": "type",
        "vendor": "vendor",
        "virtual_device": "virtual_device",
    }

    _SP_DISPLAY_ATTRS_BOOL_TRUE: list[Any] = ["On", "Online", "Supported", "Yes", True]
    _SP_DISPLAY_ATTRS_BOOL_FALSE: list[Any] = ["No", "Off", "Offline", "Not HDCP-capable Sink", "Not Supported", False]

    _RETINA_KEYS = [
        "spdisplays_pixelresolution",
        "_spdisplays_pixelresolution",
        "spdisplays_display_type",
        "_spdisplays_display_type",
    ]
    _SERIAL_KEYS = ["_spdisplays_display-serial-number", "spdisplays_display-serial-number"]
    _VIRTUAL_VENDORS = ["756e6b6e", "6161706c"]  # Virtual Display, AirPlay

    def __init__(self, dry_run: bool) -> None:
        self.report_fn = "displays.plist"
        super().__init__(dry_run)

        # Deliberately get the English localisation for internal parsing
        self._localisation_strings = self.read_system_profiler_localisation("SPDisplaysReporter.spreporter")["en"]

    def _localise_values(self, d: Mapping[Any, Any]) -> Mapping[Any, Any]:
        """Localise values in an object and return a dictionary of the keys and values, if a value has no localised
        value, the raw value is retained in the returned mapping.
        :param d: mapping object containing data to parse"""
        return {key: self._localisation_strings.get(val, val) for key, val in d.items()}

    def _parse_mfg_value(self, d: Mapping[Any, Any]) -> str:
        """Parse manufacturing data per EDID v1.4 data spec. Returns 'YYYY Model' if manufacturer week is
        255 or 0, or 'YYYY-WW' if not.
         - https://en.wikipedia.org/wiki/Extended_Display_Identification_Data#EDID_1.4_data_format
        :param d: mapped object with display info."""
        mfg_week = d.get("_spdisplays_display-week")
        mfg_year = d.get("_spdisplays_display-year")

        if mfg_week in ["255", "0"]:
            return f"{mfg_year} Model"

        return f"{mfg_year}-{mfg_week}"

    def _parse_display_type(self, d: Mapping[Any, Any]) -> str:
        """Parse whether the display is an LCD, Projector, CRT, returns LCD if device is a television.
        :param d: mapped object with display info."""
        return "LCD" if d.get("spdisplays_television") else d.get("spdisplays_display_type")

    def _parse_virutal_display_and_vendor_id(self, d: Mapping[Any, Any]) -> tuple[bool, str]:
        """Parse a value for vendor id.
        :param d: mapped object with display info."""
        _vendor_id = d.get("_spdisplays_display-vendor-id")
        is_virtual = (
            _vendor_id in self._VIRTUAL_VENDORS if _vendor_id else False or d.get("_spdisplays_virtualdevice", False)
        )
        vendor_id = "Virtual Display" if _vendor_id and _vendor_id == self._VIRTUAL_VENDORS[0] else _vendor_id

        return (is_virtual, vendor_id)

    def _parse_display_data(self, d: Mapping[Any, Any]) -> Mapping[Any, Any]:
        """Merges data from the '_spdisplays_displayport_device' object in any 'spdisplays_ndrvs' object.
        :param d: mapping object from 'spdisplays_ndrvs'"""
        result = {key: val for key, val in d.items() if not key == "_spdisplays_displayport_device"}
        result = self._localise_values(result)
        disp_port_data = d.get("_spdisplays_displayport_device")

        # Parse the "displayport" data and delete the '_name' key to avoid merging with the parent dict object
        if disp_port_data:
            del disp_port_data["_name"]
            disp_port_data = self._localise_values(disp_port_data)
            result.update(disp_port_data)

        # Make sure a display _always_ has a value for the 'builtin' attribute.
        if "spdisplays_builtin" not in result:
            result["spdisplays_builtin"] = "No" if any(result.get(k) for k in self._SERIAL_KEYS) else "No"

        # Make sure display always has a display type
        if "spdisplays_display_type" not in result:
            result["spdisplays_display_type"] = self._parse_display_type(result)

        # Set virtual device and vendor values
        result["virtual_device"], result["vendor"] = self._parse_virutal_display_and_vendor_id(result)

        # Retina supported
        result["retina"] = any("retina" in result.get(k, "") for k in self._RETINA_KEYS)

        # Insert a manufactured date
        result["manufactured"] = self._parse_mfg_value(result)

        return result

    def _parse_graphics_data(self, d: Mapping[Any, Any]) -> Mapping[Any, Any]:
        """Parses the graphics device data from the system_profiler output with correct localised values or raw
        value if no localisation available. Excludes the 'spdisplays_ndrvs' values as they are processed elsewhere.
        :param d: mapping object from 'system_profiler'"""
        return {k: self._localisation_strings.get(v, v) for k, v in d.items() if not k == "spdisplays_ndrvs"}

    def report_data(self) -> Optional[Iterable[Mapping]]:
        """Parses the output of the system_profiler with respect to the specified data type."""
        result = []
        dt = "SPDisplaysDataType"
        graphics_displays = system_profiler(dt).get(dt, [])

        # Note, each graphics object will have a list of displays attached to it in the 'spdisplays_ndrvs' key
        for gpu in graphics_displays:
            displays = [self._parse_display_data(disp) for disp in gpu.get("spdisplays_ndrvs", [])]

            for display in displays:
                data = {}

                # Construct the object to return in the results
                for key, val in display.items():
                    if isinstance(val, str):
                        val = val.strip()

                    if key in self._SP_DISPLAYS_ATTRS_MAP:
                        if val in self._SP_DISPLAY_ATTRS_BOOL_TRUE:
                            val = 1
                        elif val in self._SP_DISPLAY_ATTRS_BOOL_FALSE:
                            val = 0

                        data[self._SP_DISPLAYS_ATTRS_MAP.get(key, key)] = val

            result.append(data)

        return result
