from __future__ import annotations

from typed_settings import Secret, load_settings, option, secret, settings

from actions.utilities import LOADER, convert_secret_str, convert_str


@settings
class HooksSettings:
    repos: list[str] | None = option(
        default=None, help="The repos whose hooks are to be run"
    )
    hooks: list[str] | None = option(default=None, help="The hooks to be run")


HOOKS_SETTINGS = load_settings(HooksSettings, [LOADER])


__all__ = ["HOOKS_SETTINGS", "HooksSettings"]
