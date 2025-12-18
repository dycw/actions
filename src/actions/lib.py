from __future__ import annotations

from template_action import __version__
from template_action.logging import LOGGER
from template_action.settings import SETTINGS


def template_action(*, flag: bool = SETTINGS.flag) -> None:
    LOGGER.info(
        """\
Running version %s with settings:
 - flag = %s
 """,
        __version__,
        flag,
    )


__all__ = ["template_action"]
