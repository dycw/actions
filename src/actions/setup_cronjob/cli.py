from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.click import ListStrs, Str, argument, flag, option
from utilities.constants import USER
from utilities.core import is_pytest, set_up_logging

from actions.setup_cronjob.constants import KILL_AFTER, LOGS_KEEP, TIMEOUT
from actions.setup_cronjob.lib import setup_cronjob

if TYPE_CHECKING:
    from collections.abc import Sequence

    from utilities.types import PathLike


@argument("name", type=str)
@argument("command", type=str)
@argument("args", nargs=-1, type=str)
@option("--prepend-path", type=ListStrs(), default=None, help="Paths to preprend")
@option("--schedule", type=ListStrs(), default=None, help="Cron job schedule")
@option("--user", type=Str(), default=USER, help="Cron job user")
@option(
    "--timeout", type=int, default=TIMEOUT, help="Seconds until timing-out the cron job"
)
@option(
    "--kill-after",
    type=int,
    default=KILL_AFTER,
    help="Seconds until killing the cron job (after timeout)",
)
@flag("--sudo", default=False, help="Run as 'sudo'")
@option("--logs-keep", type=int, default=LOGS_KEEP, help="Number of logs to keep")
def setup_cronjob_sub_cmd(
    *,
    name: str,
    command: str,
    args: tuple[str, ...],
    prepend_path: Sequence[PathLike] | None,
    schedule: str,
    user: str,
    timeout: int,
    kill_after: int,
    sudo: bool,
    logs_keep: int,
) -> None:
    if is_pytest():
        return
    set_up_logging(__name__, root=True)
    setup_cronjob(
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


__all__ = ["setup_cronjob_sub_cmd"]
