from __future__ import annotations

from typing import TYPE_CHECKING

from click import Command, command
from utilities.click import (
    CONTEXT_SETTINGS,
    ListStrs,
    Str,
    TimeDelta,
    argument,
    flag,
    option,
)
from utilities.constants import USER
from utilities.core import is_pytest, set_up_logging
from utilities.types import PathLike

from actions import __version__
from actions.set_up_cron.constants import KILL_AFTER, LOGS_KEEP, SCHEDULE, TIMEOUT
from actions.set_up_cron.lib import Job, set_up_cron

if TYPE_CHECKING:
    from collections.abc import Callable, Sequence

    from utilities.types import Duration, PathLike


SET_UP_CRON_SUB_CMD: str = "set-up-cron"


def make_set_up_cron_cmd(
    *, cli: Callable[..., Command] = command, name: str | None = None
) -> Command:
    @argument("name", type=Str())
    @argument("command", type=Str())
    @argument("args", nargs=-1, type=Str())
    @option("--schedule", type=Str(), default=SCHEDULE, help="Cron job schedule")
    @option("--user", type=Str(), default=USER, help="Cron job user")
    @option(
        "--timeout",
        type=TimeDelta(),
        default=TIMEOUT,
        help="Duration until timing-out the cron job",
    )
    @option(
        "--kill-after",
        type=TimeDelta(),
        default=KILL_AFTER,
        help="Duration until killing the cron job (after timeout)",
    )
    @flag("--sudo-job", default=False, help="Run job as 'sudo'")
    @option("--prepend-path", type=ListStrs(), default=None, help="Paths to preprend")
    @flag("--sudo-cron", default=False, help="Run cron as 'sudo'")
    @option("--logs-keep", type=int, default=LOGS_KEEP, help="Number of logs to keep")
    def func(
        *,
        name: str,
        command: str,
        args: tuple[str, ...],
        schedule: str,
        user: str,
        timeout: Duration,
        kill_after: Duration,
        sudo_job: bool,
        prepend_path: Sequence[PathLike] | None,
        sudo_cron: bool,
        logs_keep: int,
    ) -> None:
        if is_pytest():
            return
        set_up_logging(__name__, root=True, log_version=__version__)
        job = Job(
            name,
            command,
            schedule=schedule,
            user=user,
            timeout=timeout,
            kill_after=kill_after,
            sudo=sudo_job,
            args=list(args) if len(args) >= 1 else None,
        )
        set_up_cron(
            job,
            cron_name=name,
            prepend_path=prepend_path,
            sudo=sudo_cron,
            logs_keep=logs_keep,
        )

    return cli(name=name, help="Set up 'cron'", **CONTEXT_SETTINGS)(func)


cli = make_set_up_cron_cmd()


__all__ = ["SET_UP_CRON_SUB_CMD", "cli", "make_set_up_cron_cmd"]
