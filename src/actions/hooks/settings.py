from __future__ import annotations

from typed_settings import load_settings, option, settings

from actions.utilities import LOADER


@settings
class HooksSettings:
    repos: list[str] | None = option(
        default=None, help="The repos whose hooks are to be run"
    )
    hooks: list[str] | None = option(default=None, help="The hooks to be run")


HOOKS_SETTINGS = load_settings(HooksSettings, [LOADER])


__all__ = ["HOOKS_SETTINGS", "HooksSettings"]
