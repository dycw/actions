from __future__ import annotations

from math import ceil, floor
from random import choice
from time import sleep

from utilities.core import get_now
from whenever import TimeDelta, ZonedDateTime

from actions.logging import LOGGER
from actions.random_sleep.constants import LOG_FREQ, MAX, MIN, STEP
from actions.random_sleep.settings import SETTINGS


def random_sleep(
    *,
    min: int = MIN,  # noqa: A002
    max: int = MAX,  # noqa: A002
    step: int = STEP,
    log_freq: int = LOG_FREQ,
) -> None:
    LOGGER.info("Sleeping...")
    start = get_now()
    duration = TimeDelta(seconds=choice(range(min, max, step)))
    LOGGER.info("Sleeping for %s...", duration)
    end = (start + duration).round(mode="ceil")
    while (now := get_now()) < end:
        _intermediate(start, now, end, log_freq=log_freq)
    LOGGER.info("Finished sleeping")


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
