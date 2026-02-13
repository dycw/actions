from __future__ import annotations

from typing import TYPE_CHECKING

from click import Command, command
from utilities.click import CONTEXT_SETTINGS, option
from utilities.core import is_pytest, set_up_logging

from actions import __version__
from actions.random_sleep.constants import LOG_FREQ, MAX, MIN, STEP
from actions.random_sleep.lib import random_sleep

if TYPE_CHECKING:
    from collections.abc import Callable

RANDOM_SLEEP_SUB_CMD = "random-sleep"


def make_random_sleep_cmd(
    *, cli: Callable[..., Command] = command, name: str | None = None
) -> Command:
    @option("--min", "min_", type=int, default=MIN, help="Minimum duration, in seconds")
    @option("--max", "max_", type=int, default=MAX, help="Maximum duration, in seconds")
    @option("--step", type=int, default=STEP, help="Step duration, in seconds")
    @option("--log-freq", type=int, default=LOG_FREQ, help="Log frequency, in seconds")
    def func(*, min_: int, max_: int, step: int, log_freq: int) -> None:
        if is_pytest():
            return
        set_up_logging(__name__, root=True, log_version=__version__)
        random_sleep(min=min_, max=max_, step=step, log_freq=log_freq)

    return cli(name=name, help="Random sleep with logging", **CONTEXT_SETTINGS)(func)


cli = make_random_sleep_cmd()


__all__ = ["RANDOM_SLEEP_SUB_CMD", "cli", "make_random_sleep_cmd"]
