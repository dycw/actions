from __future__ import annotations

from string import Template
from typing import TYPE_CHECKING

from utilities.constants import SYSTEM, USER
from utilities.core import to_logger
from utilities.subprocess import chmod, chown, tee

from actions.setup_cronjob.constants import (
    KILL_AFTER,
    LOGS_KEEP,
    PATH_CONFIGS,
    SCHEDULE,
    TIMEOUT,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from utilities.types import PathLike


_LOGGER = to_logger(__name__)


def setup_cronjob(
    name: str,
    command: str,
    /,
    *args: str,
    prepend_path: Sequence[PathLike] | None = None,
    schedule: str = SCHEDULE,
    user: str = USER,
    timeout: int = TIMEOUT,
    kill_after: int = KILL_AFTER,
    logs_keep: int = LOGS_KEEP,
) -> None:
    """Set up a cronjob & logrotate."""
    _LOGGER.info("Setting up cronjob...")
    if SYSTEM != "linux":
        msg = f"System must be 'linux'; got {SYSTEM!r}"
        raise TypeError(msg)
    text = _get_crontab(
        name,
        command,
        *args,
        prepend_path=prepend_path,
        schedule=schedule,
        user=user,
        timeout=timeout,
        kill_after=kill_after,
    )
    _tee_and_perms(f"/etc/cron.d/{name}", text)
    _tee_and_perms(
        f"/etc/logrotate.d/{name}", _get_logrotate(name, logs_keep=logs_keep)
    )
    _LOGGER.info("Finished setting up cronjob")


def _get_crontab(
    name: str,
    command: PathLike,
    /,
    *args: str,
    prepend_path: Sequence[PathLike] | None = None,
    schedule: str = SCHEDULE,
    user: str = USER,
    timeout: int = TIMEOUT,
    kill_after: int = KILL_AFTER,
) -> str:
    return Template((PATH_CONFIGS / "cron.tmpl").read_text()).substitute(
        PREPEND_PATH=""
        if prepend_path is None
        else "".join(f"{p}:" for p in prepend_path),
        SCHEDULE=schedule,
        USER=user,
        NAME=name,
        TIMEOUT=timeout,
        KILL_AFTER=kill_after,
        COMMAND=command,
        SPACE=" " if (args is not None) and (len(args) >= 1) else "",
        ARGS="" if args is None else " ".join(args),
    )


def _get_logrotate(name: str, /, *, logs_keep: int = LOGS_KEEP) -> str:
    return Template((PATH_CONFIGS / "logrotate.tmpl").read_text()).substitute(
        NAME=name, ROTATE=logs_keep
    )


def _tee_and_perms(path: PathLike, text: str, /) -> None:
    tee(path, text, sudo=True)
    chown(path, sudo=True, user="root", group="root")
    chmod(path, "u=rw,g=r,o=r", sudo=True)


__all__ = ["setup_cronjob"]
