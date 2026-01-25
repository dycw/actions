from __future__ import annotations

from typing import TYPE_CHECKING

import utilities.click
from click import option
from utilities.constants import PWD
from utilities.core import is_pytest
from utilities.logging import basic_config

from actions.clean_dir.lib import clean_dir
from actions.logging import LOGGER

if TYPE_CHECKING:
    from utilities.types import PathLike


@option(
    "--path", type=utilities.click.Path(), default=PWD, help="The directory to clean"
)
def clean_dir_sub_cmd(*, path: PathLike) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    clean_dir(path=path)


__all__ = ["clean_dir_sub_cmd"]
