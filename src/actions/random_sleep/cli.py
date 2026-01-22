from __future__ import annotations

from typed_settings import click_options
from utilities.core import is_pytest
from utilities.logging import basic_config

from actions.logging import LOGGER
from actions.random_sleep.lib import random_sleep
from actions.random_sleep.settings import Settings
from actions.utilities import LOADER


@click_options(Settings, [LOADER], show_envvars_in_help=True)
def random_sleep_sub_cmd(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    random_sleep(
        min=settings.min,
        max=settings.max,
        step=settings.step,
        log_freq=settings.log_freq,
    )


__all__ = ["random_sleep_sub_cmd"]
