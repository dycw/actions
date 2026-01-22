from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import click
from click import argument
from typed_settings import click_options
from utilities.core import is_pytest
from utilities.logging import basic_config

from actions.logging import LOGGER
from actions.re_encrypt.lib import re_encrypt
from actions.re_encrypt.settings import Settings
from actions.utilities import LOADER

if TYPE_CHECKING:
    from utilities.types import PathLike


@argument("path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click_options(Settings, [LOADER], show_envvars_in_help=True)
def re_encrypt_sub_cmd(settings: Settings, /, *, path: PathLike) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    re_encrypt(
        path,
        key_file=settings.key_file,
        key=settings.key,
        new_key_file=settings.new_key_file,
        new_key=settings.new_key,
    )


__all__ = ["re_encrypt_sub_cmd"]
