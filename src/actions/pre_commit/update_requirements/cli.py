from __future__ import annotations

from typing import TYPE_CHECKING

from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest

from actions.logging import LOGGER
from actions.pre_commit.click import path_argument
from actions.pre_commit.update_requirements.lib import update_requirements
from actions.pre_commit.update_requirements.settings import Settings
from actions.utilities import LOADER

if TYPE_CHECKING:
    from pathlib import Path


@path_argument
@click_options(Settings, [LOADER], show_envvars_in_help=True)
def update_requirements_sub_cmd(
    settings: Settings, /, *, paths: tuple[Path, ...]
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    update_requirements(*paths, index=settings.index)


__all__ = ["update_requirements_sub_cmd"]
