from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from utilities.text import strip_and_dedent

from actions import __version__
from actions.clean_dir.settings import CLEAN_DIR_SETTINGS
from actions.logging import LOGGER

if TYPE_CHECKING:
    from utilities.types import PathLike


def clean_dir(*, path: PathLike = CLEAN_DIR_SETTINGS.path) -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - path = %s
        """),
        clean_dir.__name__,
        __version__,
        path,
    )
    path = Path(path)
    if path.is_file():
        msg = f"{str(path)!r} is a file, not a directory"
        raise FileExistsError(msg)
    if not path.is_dir():
        msg = f"{str(path)!r} is a not a directory"
        raise NotADirectoryError(msg)
    for _p in path.rglob("**/*.pyc"):
        pass


__all__ = ["clean_dir"]
