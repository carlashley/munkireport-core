"""Core MunkiReport Class"""
from pathlib import Path

from .mixins import VersioningMixin, SystemAttrsMixin

__title__ = "mrlib"
__summary__ = "munkireport-core package for munkireport"
__uri__ = "https://github.com/carlashley/munkireport-core"
__version__ = "1.0.20230715"
__author__ = "Carl Ashley"
__license__ = "MIT License"
__copyright__ = f"2023 {__author__}"


class MunkiReport(VersioningMixin, SystemAttrsMixin):
    """The MunkiReport parent class."""

    def __init__(self, dry_run: bool = False, tmp_dir: Path = Path("/tmp/mrclient")) -> None:
        self.dry_run = dry_run
        self.tmp_dir = tmp_dir
