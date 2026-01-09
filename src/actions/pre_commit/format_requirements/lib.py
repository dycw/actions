from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from utilities.text import repr_str

from actions.logging import LOGGER
from actions.pre_commit.utilities import get_pyproject_dependencies, yield_toml_doc
from actions.utilities import log_func_call

if TYPE_CHECKING:
    from collections.abc import MutableSet
    from pathlib import Path

    from utilities.packaging import Requirement
    from utilities.types import PathLike


def format_requirements(*paths: PathLike) -> None:
    LOGGER.info(log_func_call(format_requirements, f"{paths=}"))
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
        get_pyproject_dependencies(doc).apply(_format_req)


def _format_req(requirement: Requirement, /) -> Requirement:
    return requirement


__all__ = ["format_requirements"]
