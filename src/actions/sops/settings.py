from __future__ import annotations

from typed_settings import Secret, load_settings, secret, settings

from actions.utilities import LOADER, convert_secret_str


@settings
class SopsSettings:
    token: Secret[str] | None = secret(
        default=None, converter=convert_secret_str, help="The GitHub token"
    )


SOPS_SETTINGS = load_settings(SopsSettings, [LOADER])


__all__ = ["SOPS_SETTINGS", "SopsSettings"]
