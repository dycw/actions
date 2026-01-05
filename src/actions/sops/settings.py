from __future__ import annotations

from pathlib import Path
from platform import platform, system

from typed_settings import Secret, load_settings, option, secret, settings

from actions.utilities import LOADER, convert_secret_str


@settings
class SopsSettings:
    token: Secret[str] | None = secret(
        default=None, converter=convert_secret_str, help="The GitHub token"
    )
    system: str = option(default=system(), help="System name")
    platform: str = option(default=platform(), help="Platform name")
    path: Path = option(default=Path("/usr/bin/local/sops"), help="Download path")
    timeout: int = option(default=60, help="Download timeout")
    chunk_size: int = option(default=8192, help="Streaming chunk size")


SOPS_SETTINGS = load_settings(SopsSettings, [LOADER])


__all__ = ["SOPS_SETTINGS", "SopsSettings"]
