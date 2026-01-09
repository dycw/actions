from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from libcst import parse_statement
from utilities.text import repr_str
from utilities.throttle import throttle

from actions.logging import LOGGER
from actions.pre_commit.constants import THROTTLE_DELTA
from actions.pre_commit.utilities import path_throttle_cache, yield_python_file
from actions.utilities import log_func_call

if TYPE_CHECKING:
    from collections.abc import MutableSet
    from pathlib import Path

    from utilities.types import PathLike


def _touch_empty_py(*paths: PathLike) -> None:
    LOGGER.info(log_func_call(touch_empty_py, f"{paths=}"))
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
    delta=THROTTLE_DELTA, path=path_throttle_cache(_touch_empty_py)
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
