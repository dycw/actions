from __future__ import annotations

from typing import TYPE_CHECKING

from click import Command, command
from utilities.click import CONTEXT_SETTINGS, Path, option
from utilities.constants import PWD
from utilities.core import is_pytest, set_up_logging

from actions.clean_dir.lib import clean_dir

if TYPE_CHECKING:
    from collections.abc import Callable

    from utilities.types import PathLike


CLEAN_DIR_SUB_CMD = "clean-dir"


def make_clean_dir_cmd(
    *, cli: Callable[..., Command] = command, name: str | None = None
) -> Command:
    @option(
        "--path",
        type=Path(exist="existing dir"),
        default=PWD,
        help="The directory to clean",
    )
    def func(*, path: PathLike) -> None:
        if is_pytest():
            return
        set_up_logging(__name__, root=True)
        clean_dir(path=path)

    return cli(name=name, help="Clean a directory", **CONTEXT_SETTINGS)(func)


cli = make_clean_dir_cmd()


__all__ = ["CLEAN_DIR_SUB_CMD", "cli", "make_clean_dir_cmd"]
