from __future__ import annotations

from typed_settings import load_settings, option, settings

from actions.utilities import LOADER, convert_list_strs


@settings
class Settings:
    repos: list[str] | None = option(
        default=None,
        converter=convert_list_strs,
        help="The repos whose hooks are to be run",
    )
    hooks: list[str] | None = option(
        default=None, converter=convert_list_strs, help="The hooks to be run"
    )
    hooks_exclude: list[str] | None = option(
        default=None, converter=convert_list_strs, help="The hooks not to be run"
    )
    sleep: int = option(default=1, help="Sleep in between runs")


SETTINGS = load_settings(Settings, [LOADER])


__all__ = ["SETTINGS", "Settings"]
