from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from utilities.iterables import one
from utilities.text import repr_str, strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.pre_commit.utilities import get_pyproject_dependencies, yield_toml_doc

if TYPE_CHECKING:
    from collections.abc import MutableSet
    from pathlib import Path

    from utilities.types import PathLike


def update_requirements(*paths: PathLike) -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - paths = %s
        """),
        update_requirements.__name__,
        __version__,
        paths,
    )
    modifications: set[Path] = set()
    for path in paths:
        _format_path(path, modifications=modifications)
    if len(modifications) >= 1:
        LOGGER.info(
            "Exiting due to modifications: %s",
            ", ".join(map(repr_str, sorted(modifications))),
        )
        sys.exit(1)


def _format_path(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> None:
    with yield_toml_doc(path, modifications=modifications) as doc:
        project_deps = get_pyproject_dependencies(doc)
    if not path.is_file():
        msg = f"Expected a file; {str(path)!r} is not"
        raise FileNotFoundError(msg)
    if path.name != "pyproject.toml":
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


__all__ = ["update_requirements"]
