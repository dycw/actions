from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from utilities.functions import get_func_name
from utilities.iterables import one
from utilities.tabulate import func_param_desc
from utilities.text import repr_str
from utilities.throttle import throttle

from actions import __version__
from actions.constants import PYPROJECT_TOML
from actions.logging import LOGGER
from actions.pre_commit.constants import THROTTLE_DURATION
from actions.pre_commit.utilities import path_throttle_cache

if TYPE_CHECKING:
    from collections.abc import MutableSet

    from utilities.types import PathLike


def _touch_py_typed(*paths: PathLike) -> None:
    LOGGER.info(func_param_desc(touch_py_typed, __version__, f"{paths=}"))
    modifications: set[Path] = set()
    for path in paths:
        _format_path(path, modifications=modifications)
    if len(modifications) >= 1:
        LOGGER.info(
            "Exiting due to modifications: %s",
            ", ".join(map(repr_str, sorted(modifications))),
        )
        sys.exit(1)
    LOGGER.info("Finished running %r", get_func_name(touch_py_typed))


touch_py_typed = throttle(
    duration=THROTTLE_DURATION, path=path_throttle_cache(_touch_py_typed)
)(_touch_py_typed)


def _format_path(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> None:
    path = Path(path)
    if not path.is_file():
        msg = f"Expected a file; {str(path)!r} is not"
        raise FileNotFoundError(msg)
    if path.name != PYPROJECT_TOML.name:
        msg = f"Expected 'pyproject.toml'; got {str(path)!r}"
        raise TypeError(msg)
    src = path.parent / "src"
    if not src.exists():
        return
    if not src.is_dir():
        msg = f"Expected a directory; {str(src)!r} is not"
        raise NotADirectoryError(msg)
    non_tests = one(p for p in src.iterdir() if p.name != "tests")
    py_typed = non_tests / "py.typed"
    if not py_typed.exists():
        py_typed.touch()
        if modifications is not None:
            modifications.add(py_typed)


__all__ = ["touch_py_typed"]
