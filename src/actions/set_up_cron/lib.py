from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Self

from utilities.constants import SYSTEM, USER, Sentinel, sentinel
from utilities.core import (
    duration_to_seconds,
    normalize_str,
    replace_non_sentinel,
    substitute,
    to_logger,
)
from utilities.subprocess import chmod, chown, tee

from actions.constants import SUDO
from actions.set_up_cron.constants import (
    KILL_AFTER,
    LOGS_KEEP,
    PATH_CONFIGS,
    SCHEDULE,
    TIMEOUT,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from utilities.types import Duration, PathLike, StrStrMapping


_LOGGER = to_logger(__name__)


def set_up_cron(
    job: Job,
    /,
    *jobs: Job,
    log_name: str | None = None,
    prepend_path: Sequence[PathLike] | None = None,
    env_vars: StrStrMapping | None = None,
    sudo: bool = False,
    logs_keep: int = LOGS_KEEP,
) -> None:
    """Set up a cronjob & logrotate."""
    _LOGGER.info("Setting up cronjob...")
    if SYSTEM != "linux":
        msg = f"System must be 'linux'; got {SYSTEM!r}"
        raise TypeError(msg)
    text = _get_crontab(
        job, *jobs, log_name=log_name, prepend_path=prepend_path, env_vars=env_vars
    )
    _tee_and_perms(f"/etc/cron.d/{name}", text, sudo=sudo)
    _tee_and_perms(
        f"/etc/logrotate.d/{name}", _get_logrotate(name, logs_keep=logs_keep), sudo=sudo
    )
    _LOGGER.info("Finished setting up cronjob")


def _get_crontab(
    job: Job,
    /,
    *jobs: Job,
    log_name: str | None = None,
    prepend_path: Sequence[PathLike] | None = None,
    env_vars: StrStrMapping | None = None,
) -> str:
    all_jobs = [job, *jobs]
    if log_name is not None:
        all_jobs = [j.replace(log=log_name) for j in all_jobs]
    text = substitute(
        (PATH_CONFIGS / "cron.tmpl"),
        PREPEND_PATH=""
        if prepend_path is None
        else "".join(f"{p}:" for p in prepend_path),
        PATH_ENV_VARS_NEW_LINE="" if env_vars is None else "\n",
        ENV_VARS=""
        if env_vars is None
        else "\n".join(f"{k}={v}" for k, v in env_vars.items()),
        JOBS="".join(j.text for j in all_jobs),
    )
    return normalize_str(text)


def _get_logrotate(name: str, /, *, logs_keep: int = LOGS_KEEP) -> str:
    return substitute(PATH_CONFIGS / "logrotate.tmpl", NAME=name, ROTATE=logs_keep)


def _tee_and_perms(path: PathLike, text: str, /, *, sudo: bool = False) -> None:
    tee(path, text, sudo=sudo)
    chown(path, sudo=sudo, user="root", group="root")
    chmod(path, "u=rw,g=r,o=r", sudo=sudo)


##


@dataclass(order=True, unsafe_hash=True, slots=True)
class Job:
    schedule: str = field(default=SCHEDULE, kw_only=True)
    user: str = field(default=USER, kw_only=True)
    name: str
    timeout: Duration = field(default=TIMEOUT, kw_only=True)
    kill_after: Duration = field(default=KILL_AFTER, kw_only=True)
    command: str
    sudo: bool = field(default=SUDO, kw_only=True)
    args: list[str] | None = field(default=None, kw_only=True)
    log: str | None = field(default=None, kw_only=True)

    def replace(
        self,
        *,
        schedule: str | Sentinel = sentinel,
        user: str | Sentinel = sentinel,
        name: str | Sentinel = sentinel,
        timeout: Duration | Sentinel = sentinel,
        kill_after: Duration | Sentinel = sentinel,
        command: str | Sentinel = sentinel,
        sudo: bool | Sentinel = sentinel,
        args: list[str] | None | Sentinel = sentinel,
        log: str | None | Sentinel = sentinel,
    ) -> Self:
        return replace_non_sentinel(
            self,
            schedule=schedule,
            user=user,
            name=name,
            timeout=timeout,
            kill_after=kill_after,
            command=command,
            sudo=sudo,
            args=args,
            log=log,
        )

    @property
    def text(self) -> str:
        return substitute(
            (PATH_CONFIGS / "job.tmpl"),
            SCHEDULE=self.schedule,
            USER=self.user,
            NAME=self.name,
            TIMEOUT=round(duration_to_seconds(self.timeout)),
            KILL_AFTER=round(duration_to_seconds(self.kill_after)),
            COMMAND=self.command,
            COMMAND_ARGS_SPACE=" "
            if (self.args is not None) and (len(self.args) >= 1)
            else "",
            SUDO="sudo" if self.sudo else "",
            SUDO_TEE_SPACE=" " if self.sudo else "",
            ARGS="" if self.args is None else " ".join(self.args),
            LOG=self.name if self.log is None else self.log,
        )


__all__ = ["Job", "set_up_cron"]
