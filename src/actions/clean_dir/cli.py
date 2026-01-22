from __future__ import annotations

from typed_settings import click_options
from utilities.core import is_pytest
from utilities.logging import basic_config

from actions.clean_dir.lib import clean_dir
from actions.clean_dir.settings import Settings
from actions.logging import LOGGER
from actions.utilities import LOADER


@click_options(Settings, [LOADER], show_envvars_in_help=True)
def clean_dir_sub_cmd(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    clean_dir(dir_=settings.dir)


__all__ = ["clean_dir_sub_cmd"]
