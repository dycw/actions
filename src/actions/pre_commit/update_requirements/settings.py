from __future__ import annotations

from typed_settings import load_settings, option, settings

from actions.utilities import LOADER


@settings
class Settings:
    indexes: list[str] | None = option(
        factory=list,
        help="List of URLs as additional indexes when searching for packages",
    )


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["SETTINGS", "Settings"]
