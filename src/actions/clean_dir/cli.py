from __future__ import annotations

from typing import TYPE_CHECKING

import utilities.click
from click import command, option
from utilities.constants import PWD
from utilities.core import is_pytest, set_up_logging

from actions.clean_dir.lib import clean_dir

if TYPE_CHECKING:
    from utilities.types import PathLike


@option(
    "--path",
    type=utilities.click.Path(exist="existing dir"),
    default=PWD,
    help="The directory to clean",
)
def clean_dir_sub_cmd(*, path: PathLike) -> None:
    if is_pytest():
        return
    set_up_logging(__name__, root=True)
    clean_dir(path=path)


cli = command(clean_dir_sub_cmd)


__all__ = ["clean_dir_sub_cmd", "cli"]
