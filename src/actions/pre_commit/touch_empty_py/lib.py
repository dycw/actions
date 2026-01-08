from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from libcst import parse_statement
from utilities.text import repr_str, strip_and_dedent
from utilities.throttle import throttle
from utilities.whenever import HOUR

from actions import __version__
from actions.constants import PATH_THROTTLE_CACHE
from actions.logging import LOGGER
from actions.pre_commit.utilities import yield_python_file

if TYPE_CHECKING:
    from collections.abc import MutableSet
    from pathlib import Path

    from utilities.types import PathLike


def _touch_empty_py(*paths: PathLike) -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - paths = %s
        """),
        touch_empty_py.__name__,
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


touch_empty_py = throttle(
    delta=12 * HOUR, path=PATH_THROTTLE_CACHE / _touch_empty_py.__name__
)(_touch_empty_py)


def _format_path(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> None:
    with yield_python_file(path, modifications=modifications) as context:
        if len(context.input.body) >= 1:
            return
        body = [
            *context.input.body,
            parse_statement("from __future__ import annotations"),
        ]
        context.output = context.input.with_changes(body=body)


__all__ = ["touch_empty_py"]
