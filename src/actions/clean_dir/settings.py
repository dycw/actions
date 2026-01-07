from __future__ import annotations

from pathlib import Path

from typed_settings import load_settings, option, settings

from actions.utilities import LOADER


@settings
class CleanDirSettings:
    dir: Path = option(default=Path.cwd(), help="The directory to clean")


CLEAN_DIR_SETTINGS = load_settings(CleanDirSettings, [LOADER])


__all__ = ["CLEAN_DIR_SETTINGS", "CleanDirSettings"]
