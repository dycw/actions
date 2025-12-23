from __future__ import annotations

from typed_settings import Secret, load_settings, secret, settings

from actions.utilities import LOADER, empty_str_to_none


@settings
class CommonSettings:
    token: Secret[str] | None = secret(
        default=None, converter=empty_str_to_none, help="GitHub token"
    )


COMMON_SETTINGS = load_settings(CommonSettings, [LOADER])


__all__ = ["COMMON_SETTINGS", "CommonSettings"]
