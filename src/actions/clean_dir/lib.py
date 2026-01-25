from __future__ import annotations

from pathlib import Path
from shutil import rmtree
from typing import TYPE_CHECKING

from utilities.constants import PWD

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
        files = list(_yield_files(path=path))
        if len(files) >= 1:
            for f in files:
                f.unlink(missing_ok=True)
        dirs = list(_yield_dirs(path=path))
        if len(dirs) >= 1:
            for d in dirs:
                rmtree(d, ignore_errors=True)
        else:
            break
    LOGGER.info("Finished cleaning directory")


def _yield_dirs(*, path: PathLike = PWD) -> Iterator[Path]:
    for p in Path(path).rglob("**/*"):
        if p.is_dir() and (len(list(p.iterdir())) == 0):
            yield p


def _yield_files(*, path: PathLike = PWD) -> Iterator[Path]:
    path = Path(path)
    yield from path.rglob("**/*.pyc")
    yield from path.rglob("**/*.pyo")


__all__ = ["clean_dir"]
