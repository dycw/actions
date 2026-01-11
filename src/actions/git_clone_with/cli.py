from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import click
from click import argument, command
from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.subprocess import git_clone_cmd

from actions.git_clone_with.lib import git_clone_with
from actions.git_clone_with.settings import Settings
from actions.logging import LOGGER
from actions.utilities import LOADER

if TYPE_CHECKING:
    from utilities.types import PathLike


@argument("path_key", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@argument("owner", type=str)
@argument("repo", type=str)
@argument("path_clone", type=click.Path(file_okay=False, path_type=Path))
@click_options(Settings, [LOADER], show_envvars_in_help=True)
def git_clone_with_sub_cmd(
    path_key: PathLike,
    owner: str,
    repo: str,
    path_clone: PathLike,
    settings: Settings,
    /,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)

    zz

    git_clone_with(
        path_key, owner, repo, path_clone, sudo=settings.sudo, branch=settings.branch
    )


__all__ = ["git_clone_with_sub_cmd"]
