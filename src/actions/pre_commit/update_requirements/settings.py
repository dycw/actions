from __future__ import annotations

from typed_settings import load_settings, option, settings

from actions.utilities import LOADER


@settings
class Settings:
    index: str | None = option(
        default=None,
        help="Space-separated list of URLs as additional indexes when searching for packages",
    )


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["SETTINGS", "Settings"]
