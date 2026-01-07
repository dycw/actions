from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

from libcst import (
    ImportAlias,
    ImportFrom,
    Module,
    Name,
    SimpleStatementLine,
    parse_module,
)
from utilities.text import repr_str, strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.utilities import are_modules_equal

if TYPE_CHECKING:
    from utilities.types import PathLike


_MODIFICATIONS: set[Path] = set()


def touch_empty_py(*paths: PathLike) -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - paths = %s
        """),
        touch_empty_py.__name__,
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
    current = parse_module(path.read_text())
    expected = _get_formatted(path)
    if not are_modules_equal(current, expected):
        _ = path.write_text(expected.code.rstrip("\n") + "\n")
        _MODIFICATIONS.add(path)


def _get_formatted(path: PathLike, /) -> Module:
    path = Path(path)
    module = parse_module(path.read_text())
    if len(module.body) >= 1:
        return module
    line = SimpleStatementLine(
        body=[
            ImportFrom(
                module=Name("__future__"), names=[ImportAlias(name=Name("annotations"))]
            )
        ]
    )
    return module.with_changes(body=[line])


__all__ = ["touch_empty_py"]
