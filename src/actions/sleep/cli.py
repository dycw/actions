from __future__ import annotations

from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.logging import basic_config

from actions import __version__
from actions.logging import LOGGER
from actions.settings import CommonSettings
from actions.sleep.lib import random_sleep
from actions.sleep.settings import SleepSettings
from actions.utilities import ENV_LOADER


@click_options(
    CommonSettings, [ENV_LOADER], show_envvars_in_help=True, argname="common"
)
@click_options(SleepSettings, [ENV_LOADER], show_envvars_in_help=True, argname="sleep")
def sleep_sub_cmd(*, common: CommonSettings, sleep: SleepSettings) -> None:
    basic_config(obj=LOGGER)
    LOGGER.info(
        """\
Running '%r' (version %s) with settings:
%s
%s""",
        random_sleep.__name__,
        __version__,
        pretty_repr(common),
        pretty_repr(sleep),
    )
    if common.dry_run:
        LOGGER.info("Dry run; exiting...")
        return
    random_sleep(
        min_=sleep.min, max_=sleep.max, step=sleep.step, log_freq=sleep.log_freq
    )


__all__ = ["sleep_sub_cmd"]
