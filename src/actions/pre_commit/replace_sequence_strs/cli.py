from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.logging import basic_config
from utilities.os import is_pytest

from actions.logging import LOGGER
from actions.pre_commit.click import path_argument
from actions.pre_commit.replace_sequence_strs.lib import replace_sequence_strs

if TYPE_CHECKING:
    from pathlib import Path


@path_argument
def replace_sequence_strs_sub_cmd(*, paths: tuple[Path, ...]) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    replace_sequence_strs(*paths)


__all__ = ["replace_sequence_strs_sub_cmd"]
