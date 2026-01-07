from __future__ import annotations

from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.setup_cronjob.lib import setup_cronjob
from actions.setup_cronjob.settings import Settings
from actions.utilities import LOADER


@click_options(Settings, [LOADER], show_envvars_in_help=True)
def setup_cronjob_sub_cmd(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
            %s
        """),
        setup_cronjob.__name__,
        __version__,
        pretty_repr(settings),
    )
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
