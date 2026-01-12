from __future__ import annotations

from math import ceil, floor
from random import choice
from time import sleep

from utilities.functions import get_func_name
from utilities.tabulate import func_param_desc
from utilities.whenever import get_now
from whenever import TimeDelta, ZonedDateTime

from actions import __version__
from actions.logging import LOGGER
from actions.random_sleep.settings import SETTINGS


def random_sleep(
    *,
    min: int = SETTINGS.min,  # noqa: A002
    max: int = SETTINGS.max,  # noqa: A002
    step: int = SETTINGS.step,
    log_freq: int = SETTINGS.log_freq,
) -> None:
    LOGGER.info(
        func_param_desc(
            random_sleep, __version__, f"{min=}", f"{max=}", f"{step=}", f"{log_freq=}"
        )
    )
    start = get_now()
    delta = TimeDelta(seconds=choice(range(min, max, step)))
    LOGGER.info("Sleeping for %s...", delta)
    end = (start + delta).round(mode="ceil")
    while (now := get_now()) < end:
        _intermediate(start, now, end, log_freq=log_freq)
    LOGGER.info("Finished running %r", get_func_name(random_sleep))


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
