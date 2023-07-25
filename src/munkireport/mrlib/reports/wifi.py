from typing import Any, Mapping, Optional

from .. import MunkiReport
from ..wrappers.binaries import airport


class WiFiReport(MunkiReport):
    """WiFi Report.
    Note: macOS 12 Monterey removes the BSSID from the output of the 'airport' private framework binary tool, this
          change was made on privacy grounds.
          This implementation of this report explicitly excludes BSSID values and known network and channel  history
          for privacy reasons; SSID connection history can reveal information about users that can be used to build up
          identifiable habits or even where that user has been.
          Pull requests or feature requests to re-implement known network history will not be implemented."""

    _AIRPORT_ATTR_MAP: dict[str, str] = {
        "802.11 auth": "x802_11_auth",
    }

    def __init__(self, dry_run: bool) -> None:
        self.report_fn = "wifi.plist"
        super().__init__(dry_run)

    def _calc_snr(self, rssi: int, noise: int) -> int:
        """Calculate Signal to Noise Ratio using RSSI and Noise values.
        :param rssi: the agrCtlRSSI value
        :param noise: the agrCtlNoise value"""
        return rssi - noise

    def _clean_airport_key(self, s: str) -> str:
        """Clean the key from the output of the airport wrapper.
        :param s: key string to clean"""
        s = self._AIRPORT_ATTR_MAP.get(s, s)
        return s.lower().replace(".", "_").replace(" ", "_")

    def _parse_airport(self) -> Mapping[Any, Any]:
        """Parse the output of the airport wrapper."""
        result = {"state": "off"}
        data = airport("-I")

        if any(output in data for output in ["AirPort: Off", "AirPort is Off"]):
            return result

        for line in data.splitlines():
            key, *val = line.strip().split(": ")

            if val:
                val = "".join(val)

                # Attempt to convert stringified integers into actual int values
                try:
                    val = int(val)
                except ValueError:
                    pass

                result[self._clean_airport_key(key)] = val

        rssi, noise = int(result.get("agrctlrssi", 0)), int(result.get("agrctlnoise", 0))
        result["snr"] = self._calc_snr(rssi, noise)

        # Purposefully exclude BSSID values if present
        try:
            del result["bssid"]
        except KeyError:
            pass

        return result

    def report_data(self) -> Optional[Mapping]:
        """Parses the report output."""
        result = self._parse_airport()

        return result
