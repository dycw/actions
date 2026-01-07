from __future__ import annotations

from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest

from actions.logging import LOGGER
from actions.setup_cronjob.lib import setup_cronjob
from actions.setup_cronjob.settings import Settings
from actions.utilities import LOADER


@click_options(Settings, [LOADER], show_envvars_in_help=True)
def setup_cronjob_sub_cmd(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    setup_cronjob(
        name=settings.name,
        prepend_path=settings.prepend_path,
        schedule=settings.schedule,
        user=settings.user,
        timeout=settings.timeout,
        kill_after=settings.kill_after,
        command=settings.command,
        args=settings.args,
        logs_keep=settings.logs_keep,
    )


__all__ = ["setup_cronjob_sub_cmd"]
