from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.pre_commit.click import path_argument
from actions.pre_commit.touch_empty_py.lib import touch_empty_py

if TYPE_CHECKING:
    from pathlib import Path


TOUCH_EMPTY_PY_SUB_CMD = "touch-empty-py"


@path_argument
def touch_empty_py_sub_cmd(*, paths: tuple[Path, ...]) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - paths = %s
        """),
        touch_empty_py.__name__,
        __version__,
        paths,
    )
    touch_empty_py(*paths)


__all__ = ["TOUCH_EMPTY_PY_SUB_CMD", "touch_empty_py_sub_cmd"]
