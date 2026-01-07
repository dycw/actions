from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.logging import basic_config
from utilities.os import is_pytest

from actions.logging import LOGGER
from actions.pre_commit.click import path_argument
from actions.pre_commit.format_requirements.lib import format_requirements

if TYPE_CHECKING:
    from pathlib import Path


@path_argument
def format_requirements_sub_cmd(*, paths: tuple[Path, ...]) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    format_requirements(*paths)


__all__ = ["format_requirements_sub_cmd"]
