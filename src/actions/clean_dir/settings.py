from __future__ import annotations

from pathlib import Path

from typed_settings import load_settings, option, settings

from actions.utilities import LOADER


@settings
class Settings:
    dir: Path = option(default=Path.cwd(), help="The directory to clean")


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["SETTINGS", "Settings"]
