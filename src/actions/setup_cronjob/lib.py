from __future__ import annotations

from string import Template
from typing import TYPE_CHECKING

from utilities.functions import get_func_name
from utilities.platform import SYSTEM
from utilities.subprocess import chmod, chown, tee
from utilities.tabulate import func_param_desc

from actions import __version__
from actions.logging import LOGGER
from actions.setup_cronjob.constants import PATH_CONFIGS
from actions.setup_cronjob.settings import SETTINGS

if TYPE_CHECKING:
    from collections.abc import Sequence

    from utilities.types import PathLike


def setup_cronjob(
    *,
    name: str = SETTINGS.name,
    prepend_path: Sequence[PathLike] | None = SETTINGS.prepend_path,
    schedule: str = SETTINGS.schedule,
    user: str = SETTINGS.user,
    timeout: int = SETTINGS.timeout,
    kill_after: int = SETTINGS.kill_after,
    command: PathLike = SETTINGS.command,
    args: list[str] | None = SETTINGS.args,
    logs_keep: int = SETTINGS.logs_keep,
) -> None:
    """Set up a cronjob & logrotate."""
    LOGGER.info(
        func_param_desc(
            setup_cronjob,
            __version__,
            f"{name=}",
            f"{prepend_path=}",
            f"{schedule=}",
            f"{user=}",
            f"{timeout=}",
            f"{kill_after=}",
            f"{command=}",
            f"{args=}",
            f"{logs_keep=}",
        )
    )
    if SYSTEM != "linux":
        msg = f"System must be 'linux'; got {SYSTEM!r}"
        raise TypeError(msg)
    _tee_and_perms(
        f"/etc/cron.d/{name}",
        _get_crontab(
            prepend_path=prepend_path,
            schedule=schedule,
            user=user,
            name=name,
            timeout=timeout,
            kill_after=kill_after,
            command=command,
            args=args,
        ),
    )
    _tee_and_perms(
        f"/etc/logrotate.d/{name}", _get_logrotate(name=name, logs_keep=logs_keep)
    )
    LOGGER.info("Finished running %r", get_func_name(setup_cronjob))


def _get_crontab(
    *,
    prepend_path: Sequence[PathLike] | None = SETTINGS.prepend_path,
    schedule: str = SETTINGS.schedule,
    user: str = SETTINGS.user,
    name: str = SETTINGS.name,
    timeout: int = SETTINGS.timeout,
    kill_after: int = SETTINGS.kill_after,
    command: PathLike | None = SETTINGS.command,
    args: list[str] | None = SETTINGS.args,
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


def _get_logrotate(
    *, name: str = SETTINGS.name, logs_keep: int = SETTINGS.logs_keep
) -> str:
    return Template((PATH_CONFIGS / "logrotate.tmpl").read_text()).substitute(
        NAME=name, ROTATE=logs_keep
    )


def _tee_and_perms(path: PathLike, text: str, /) -> None:
    tee(path, text, sudo=True)
    chown(path, sudo=True, user="root", group="root")
    chmod(path, "u=rw,g=r,o=r", sudo=True)


__all__ = ["setup_cronjob"]
