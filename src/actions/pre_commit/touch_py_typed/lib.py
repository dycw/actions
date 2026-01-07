from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from utilities.iterables import one
from utilities.text import repr_str, strip_and_dedent

from actions import __version__
from actions.logging import LOGGER

if TYPE_CHECKING:
    from utilities.types import PathLike


_MODIFICATIONS: set[Path] = set()


def touch_py_typed(*paths: PathLike) -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - paths = %s
        """),
        touch_py_typed.__name__,
        __version__,
        paths,
    )
    for path in paths:
        _format_path(path)
    if len(_MODIFICATIONS) >= 1:
        LOGGER.info(
            "Exiting due to modifications: %s",
            ", ".join(map(repr_str, sorted(_MODIFICATIONS))),
        )
        sys.exit(1)


def _format_path(path: PathLike, /) -> None:
    path = Path(path)
    if not path.is_file():
        msg = f"Expected a file; {str(path)!r} is not"
        raise FileNotFoundError(msg)
    if path.name != "pyproject.toml":
        msg = f"Expected 'pyproject.toml'; got {str(path)!r}"
        raise TypeError(msg)
    src = path / "src"
    if not src.exists():
        return
    if not src.is_dir():
        msg = f"Expected a directory; {str(src)!r} is not"
        raise NotADirectoryError(msg)
    non_tests = one(p for p in src.iterdir() if p.name != "tests")
    py_typed = non_tests / "py.typed"
    if not py_typed.exists():
        py_typed.touch()
        _MODIFICATIONS.add(py_typed)


__all__ = ["touch_py_typed"]
