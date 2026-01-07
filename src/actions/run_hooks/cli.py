from __future__ import annotations

from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest

from actions.logging import LOGGER
from actions.run_hooks.lib import run_hooks
from actions.run_hooks.settings import Settings
from actions.utilities import LOADER


@click_options(Settings, [LOADER], show_envvars_in_help=True)
def run_hooks_sub_cmd(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    run_hooks(repos=settings.repos, hooks=settings.hooks, sleep=settings.sleep)


__all__ = ["run_hooks_sub_cmd"]
