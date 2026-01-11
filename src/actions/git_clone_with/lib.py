from __future__ import annotations

from pathlib import Path
from shutil import copy
from typing import TYPE_CHECKING

from utilities.atomicwrites import writer
from utilities.subprocess import git_clone
from utilities.text import strip_and_dedent

from actions.git_clone_with.settings import SETTINGS
from actions.logging import LOGGER
from actions.setup_ssh_config.lib import setup_ssh_config
from actions.utilities import log_func_call

if TYPE_CHECKING:
    from utilities.types import PathLike


def git_clone_with(
    path_key: PathLike,
    owner: str,
    repo: str,
    /,
    *,
    path_clone: PathLike = SETTINGS.path_clone,
    sudo: bool = SETTINGS.sudo,
    branch: str | None = SETTINGS.branch,
) -> None:
    variables = [
        f"{path_key=}",
        f"{owner=}",
        f"{repo=}",
        f"{path_clone=}",
        f"{sudo=}",
        f"{branch=}",
    ]
    LOGGER.info(log_func_call(git_clone_with, *variables))
    path_key = Path(path_key)
    setup_ssh_config()
    _setup_ssh_config_for_key(path_key)
    _setup_deploy_key(path_key)
    git_clone(
        f"git@{path_key.stem}:{owner}/{repo}", path_clone, sudo=sudo, branch=branch
    )


def _setup_ssh_config_for_key(path: PathLike, /) -> None:
    path = Path(path)
    stem = path.stem
    dest = Path.home() / f".ssh/config.d/{stem}.conf"
    dest.parent.mkdir(parents=True, exist_ok=True)
    text = strip_and_dedent(f"""
        Host {stem}
            HostName github.com
            User git
            IdentityFile ~/.ssh/{path.name}
            IdentitiesOnly yes
    """)
    with writer(dest, overwrite=True) as temp:
        _ = temp.write_text(text)


def _setup_deploy_key(path: PathLike, /) -> None:
    dest = Path.home() / ".ssh" / Path(path).name
    dest.parent.mkdir(parents=True, exist_ok=True)
    _ = copy(path, dest)


__all__ = ["git_clone_with"]
