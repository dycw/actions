from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.logging import basic_config
from utilities.os import is_pytest

from actions.logging import LOGGER
from actions.pre_commit.click import path_argument
from actions.update_requirements.lib import update_requirements

if TYPE_CHECKING:
    from pathlib import Path


@path_argument
def update_requirements_sub_cmd(*, paths: tuple[Path, ...]) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    update_requirements(*paths)


__all__ = ["update_requirements_sub_cmd"]
