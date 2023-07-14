"""Core MunkiReport Class"""
from pathlib import Path


class MunkiReport:
    """The MunkiReport parent class."""

    def __init__(self, dry_run: bool = False, tmp_dir: Path = Path("/tmp/mrclient")) -> None:
        self.dry_run = dry_run
        self.tmp_dir = tmp_dir
