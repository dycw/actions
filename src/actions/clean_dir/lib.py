from __future__ import annotations

from pathlib import Path
from shutil import rmtree
from typing import TYPE_CHECKING

from utilities.constants import PWD

from actions.clean_dir.settings import SETTINGS
from actions.logging import LOGGER

if TYPE_CHECKING:
    from collections.abc import Iterator

    from utilities.types import PathLike


def clean_dir(*, path: PathLike = PWD) -> None:
    """Clean a directory."""
    LOGGER.info("Cleaning directory...")
    path = Path(path)
    if not path.is_dir():
        msg = f"{str(path)!r} is a not a directory"
        raise NotADirectoryError(msg)
    while True:
        files = list(_yield_files(dir_=path))
        if len(files) >= 1:
            for f in files:
                f.unlink(missing_ok=True)
        dirs = list(_yield_dirs(dir_=path))
        if len(dirs) >= 1:
            for d in dirs:
                rmtree(d, ignore_errors=True)
        else:
            break
    LOGGER.info("Finished cleaning directory")


def _yield_dirs(*, dir_: PathLike = SETTINGS.dir) -> Iterator[Path]:
    for path in Path(dir_).rglob("**/*"):
        if path.is_dir() and (len(list(path.iterdir())) == 0):
            yield path


def _yield_files(*, dir_: PathLike = SETTINGS.dir) -> Iterator[Path]:
    dir_ = Path(dir_)
    yield from dir_.rglob("**/*.pyc")
    yield from dir_.rglob("**/*.pyo")


__all__ = ["clean_dir"]
