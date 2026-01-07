from __future__ import annotations

from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from actions import __version__
from actions.clean_dir.lib import clean_dir
from actions.clean_dir.settings import Settings
from actions.logging import LOGGER
from actions.utilities import LOADER


@click_options(Settings, [LOADER], show_envvars_in_help=True)
def clean_dir_sub_cmd(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
            %s
        """),
        clean_dir.__name__,
        __version__,
        pretty_repr(settings),
    )
    clean_dir(dir_=settings.dir)


__all__ = ["clean_dir_sub_cmd"]
