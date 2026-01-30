from __future__ import annotations

from click import option
from utilities.core import is_pytest, set_up_logging

from actions.random_sleep.constants import LOG_FREQ, MAX, MIN, STEP
from actions.random_sleep.lib import random_sleep


@option("--min", "min_", type=int, default=MIN, help="Minimum duration, in seconds")
@option("--max", "max_", type=int, default=MAX, help="Maximum duration, in seconds")
@option("--step", type=int, default=STEP, help="Step duration, in seconds")
@option("--log-freq", type=int, default=LOG_FREQ, help="Log frequency, in seconds")
def random_sleep_sub_cmd(*, min_: int, max_: int, step: int, log_freq: int) -> None:
    if is_pytest():
        return
    set_up_logging(__name__, root=True)
    random_sleep(min=min_, max=max_, step=step, log_freq=log_freq)


__all__ = ["random_sleep_sub_cmd"]
