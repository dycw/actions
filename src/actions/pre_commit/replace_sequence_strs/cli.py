from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.pre_commit.click import path_argument
from actions.pre_commit.replace_sequence_strs.lib import replace_sequence_strs

if TYPE_CHECKING:
    from pathlib import Path


REPLACE_SEQUENCE_STRS_SUB_CMD = "replace-sequence-strs"


@path_argument
def replace_sequence_strs_sub_cmd(*, paths: tuple[Path, ...]) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - paths = %s
        """),
        replace_sequence_strs.__name__,
        __version__,
        paths,
    )
    replace_sequence_strs(*paths)


__all__ = ["REPLACE_SEQUENCE_STRS_SUB_CMD", "replace_sequence_strs_sub_cmd"]
