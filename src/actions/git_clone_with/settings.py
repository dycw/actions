from __future__ import annotations

from pathlib import Path

from typed_settings import load_settings, option, settings

from actions.utilities import LOADER


@settings
class Settings:
    path_clone: Path = option(default=Path.cwd(), help="Path to clone to")
    sudo: bool = option(default=False, help="Run as sudo")
    branch: str | None = option(default=None, help="Branch to check out")


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["SETTINGS", "Settings"]
