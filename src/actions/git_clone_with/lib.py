from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from utilities.atomicwrites import writer
from utilities.functions import get_func_name
from utilities.subprocess import cp, git_clone
from utilities.tabulate import func_param_desc
from utilities.text import strip_and_dedent

from actions import __version__
from actions.constants import SSH
from actions.git_clone_with.settings import SETTINGS
from actions.logging import LOGGER
from actions.setup_ssh_config.lib import get_ssh_config, setup_ssh_config

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
    LOGGER.info(
        func_param_desc(
            git_clone_with,
            __version__,
            f"{path_key=}",
            f"{owner=}",
            f"{repo=}",
            f"{path_clone=}",
            f"{sudo=}",
            f"{branch=}",
        )
    )
    path_key = Path(path_key)
    setup_ssh_config()
    _setup_ssh_config_for_key(path_key)
    _setup_deploy_key(path_key)
    git_clone(
        f"git@{path_key.stem}:{owner}/{repo}", path_clone, sudo=sudo, branch=branch
    )
    LOGGER.info("Finished running %r", get_func_name(git_clone_with))


def _setup_ssh_config_for_key(path: PathLike, /) -> None:
    path = Path(path)
    stem = path.stem
    path_key = _get_deploy_key(path.name)
    text = strip_and_dedent(f"""
        Host {stem}
            HostName github.com
            User git
            IdentityFile {path_key}
            IdentitiesOnly yes
    """)
    with writer(get_ssh_config(stem), overwrite=True) as temp:
        _ = temp.write_text(text)


def _setup_deploy_key(path: PathLike, /) -> None:
    path = Path(path)
    cp(path, _get_deploy_key(path.name), perms="u=rw,g=,o=")


def _get_deploy_key(name: str, /) -> Path:
    return SSH / "deploy-keys" / name


__all__ = ["git_clone_with"]
