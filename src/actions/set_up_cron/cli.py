from __future__ import annotations

from typing import TYPE_CHECKING

from click import Command, command
from utilities.click import CONTEXT_SETTINGS, ListStrs, Str, TimeDelta, argument, option
from utilities.constants import USER
from utilities.core import is_pytest, set_up_logging
from utilities.types import PathLike

from actions.constants import sudo_option
from actions.set_up_cron.constants import KILL_AFTER, LOGS_KEEP, TIMEOUT
from actions.set_up_cron.lib import set_up_cronjob

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
    @option("--prepend-path", type=ListStrs(), default=None, help="Paths to preprend")
    @option("--schedule", type=ListStrs(), default=None, help="Cron job schedule")
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
    @sudo_option
    @option("--logs-keep", type=int, default=LOGS_KEEP, help="Number of logs to keep")
    def func(
        *,
        name: str,
        command: str,
        args: tuple[str, ...],
        prepend_path: Sequence[PathLike] | None,
        schedule: str,
        user: str,
        timeout: Duration,
        kill_after: Duration,
        sudo: bool,
        logs_keep: int,
    ) -> None:
        if is_pytest():
            return
        set_up_logging(__name__, root=True)
        set_up_cronjob(
            name,
            command,
            *args,
            prepend_path=prepend_path,
            schedule=schedule,
            user=user,
            timeout=timeout,
            kill_after=kill_after,
            sudo=sudo,
            logs_keep=logs_keep,
        )

    return cli(name=name, help="Set up 'cron'", **CONTEXT_SETTINGS)(func)


cli = make_set_up_cron_cmd()


__all__ = ["SET_UP_CRON_SUB_CMD", "cli", "make_set_up_cron_cmd"]
