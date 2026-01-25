from __future__ import annotations

from click import option
from utilities.core import is_pytest
from utilities.logging import basic_config

from actions.logging import LOGGER
from actions.random_sleep.lib import random_sleep


@option("--min", "min_", type=int, default=0, help="Minimum duration, in seconds")
@option("--max", "max_", type=int, default=3600, help="Maximum duration, in seconds")
@option("--step", type=int, default=1, help="Step duration, in seconds")
@option("--log-freq", type=int, default=60, help="Log frequency, in seconds")
def random_sleep_sub_cmd(*, min_: int, max_: int, step: int, log_freq: int) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    random_sleep(min=min_, max=max_, step=step, log_freq=log_freq)


__all__ = ["random_sleep_sub_cmd"]
