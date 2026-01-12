from __future__ import annotations

from pathlib import Path
from shutil import rmtree
from typing import TYPE_CHECKING

from utilities.functions import get_func_name
from utilities.tabulate import func_param_desc

from actions import __version__
from actions.clean_dir.settings import SETTINGS
from actions.logging import LOGGER

if TYPE_CHECKING:
    from collections.abc import Iterator

    from utilities.types import PathLike


def clean_dir(*, dir_: PathLike = SETTINGS.dir) -> None:
    """Clean a directory."""
    LOGGER.info(func_param_desc(clean_dir, __version__, f"{dir_=}"))
    dir_ = Path(dir_)
    if not dir_.is_dir():
        msg = f"{str(dir_)!r} is a not a directory"
        raise NotADirectoryError(msg)
    while True:
        files = list(_yield_files(dir_=dir_))
        if len(files) >= 1:
            for f in files:
                f.unlink(missing_ok=True)
        dirs = list(_yield_dirs(dir_=dir_))
        if len(dirs) >= 1:
            for d in dirs:
                rmtree(d, ignore_errors=True)
        else:
            break
    LOGGER.info("Finished running %r", get_func_name(clean_dir))


def _yield_dirs(*, dir_: PathLike = SETTINGS.dir) -> Iterator[Path]:
    for path in Path(dir_).rglob("**/*"):
        if path.is_dir() and (len(list(path.iterdir())) == 0):
            yield path


def _yield_files(*, dir_: PathLike = SETTINGS.dir) -> Iterator[Path]:
    dir_ = Path(dir_)
    yield from dir_.rglob("**/*.pyc")
    yield from dir_.rglob("**/*.pyo")


__all__ = ["clean_dir"]
