from __future__ import annotations

from actions import __version__
from actions.logging import LOGGER
from actions.settings import SETTINGS


def run_action(*, flag: bool = SETTINGS.flag) -> None:
    LOGGER.info(
        """\
Running version %s with settings:
 - flag = %s
 """,
        __version__,
        flag,
    )


__all__ = ["run_action"]
