from __future__ import annotations

from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.sleep.lib import random_sleep
from actions.sleep.settings import SleepSettings
from actions.utilities import LOADER


@click_options(SleepSettings, [LOADER], show_envvars_in_help=True)
def sleep_sub_cmd(settings: SleepSettings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
            %s
        """),
        random_sleep.__name__,
        __version__,
        pretty_repr(settings),
    )
    random_sleep(
        min_=settings.min,
        max_=settings.max,
        step=settings.step,
        log_freq=settings.log_freq,
    )


__all__ = ["sleep_sub_cmd"]
