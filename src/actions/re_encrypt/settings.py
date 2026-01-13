from __future__ import annotations

from typing import TYPE_CHECKING

from typed_settings import Secret, load_settings, option, secret, settings

from actions.utilities import LOADER

if TYPE_CHECKING:
    from pathlib import Path


@settings
class Settings:
    key_file: Path | None = option(default=None, help="The key file")
    key: Secret[str] | None = secret(default=None, help="The age identity")
    new_key_file: Path | None = option(
        default=None, help="The new key file for encryption"
    )
    new_key: Secret[str] | None = secret(
        default=None, help="The new age identity for encryption"
    )


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["SETTINGS", "Settings"]
