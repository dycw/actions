from __future__ import annotations

from math import ceil, floor
from random import choice
from time import sleep

from utilities.whenever import get_now
from whenever import TimeDelta, ZonedDateTime

from actions.logging import LOGGER
from actions.random_sleep.settings import SETTINGS
from actions.utilities import log_func_call


def random_sleep(
    *,
    min_: int = SETTINGS.min,
    max_: int = SETTINGS.max,
    step: int = SETTINGS.step,
    log_freq: int = SETTINGS.log_freq,
) -> None:
    variables = [f"{min_=}", f"{max_=}", f"{step=}", f"{log_freq=}"]
    LOGGER.info(log_func_call(random_sleep, *variables))
    start = get_now()
    delta = TimeDelta(seconds=choice(range(min_, max_, step)))
    LOGGER.info("Sleeping for %s...", delta)
    end = (start + delta).round(mode="ceil")
    while (now := get_now()) < end:
        _intermediate(start, now, end, log_freq=log_freq)
    LOGGER.info("Finished sleeping for %s", delta)


def _intermediate(
    start: ZonedDateTime,
    now: ZonedDateTime,
    end: ZonedDateTime,
    /,
    *,
    log_freq: int = SETTINGS.log_freq,
) -> None:
    elapsed = TimeDelta(seconds=floor((now - start).in_seconds()))
    remaining = TimeDelta(seconds=ceil((end - now).in_seconds()))
    this_sleep = min(remaining, TimeDelta(seconds=log_freq))
    LOGGER.info(
        "Sleeping for %s... (elapsed = %s, remaining = %s)",
        this_sleep,
        elapsed,
        remaining,
    )
    sleep(round(this_sleep.in_seconds()))


__all__ = ["random_sleep"]
