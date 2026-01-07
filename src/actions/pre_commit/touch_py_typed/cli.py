from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.logging import basic_config
from utilities.os import is_pytest

from actions.logging import LOGGER
from actions.pre_commit.click import path_argument
from actions.pre_commit.touch_py_typed.lib import touch_py_typed

if TYPE_CHECKING:
    from pathlib import Path


@path_argument
def touch_py_typed_sub_cmd(*, paths: tuple[Path, ...]) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    touch_py_typed(*paths)


__all__ = ["touch_py_typed_sub_cmd"]
