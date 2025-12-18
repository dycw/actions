from __future__ import annotations

from typed_settings import Secret, load_settings, option, secret, settings

from actions.utilities import ENV_LOADER, empty_str_to_none


@settings
class CommonSettings:
    token: Secret[str] | None = secret(
        default=None, converter=empty_str_to_none, help="GitHub token"
    )
    dry_run: bool = option(default=False, help="Dry run the CLI")


COMMON_SETTINGS = load_settings(CommonSettings, [ENV_LOADER])


__all__ = ["COMMON_SETTINGS", "CommonSettings"]
