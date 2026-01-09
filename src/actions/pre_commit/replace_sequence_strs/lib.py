from __future__ import annotations

import sys
from typing import TYPE_CHECKING, override

from libcst import CSTTransformer, Name, Subscript
from libcst.matchers import Index as MIndex
from libcst.matchers import Name as MName
from libcst.matchers import Subscript as MSubscript
from libcst.matchers import SubscriptElement as MSubscriptElement
from libcst.matchers import matches
from libcst.metadata import MetadataWrapper
from utilities.text import repr_str

from actions.logging import LOGGER
from actions.pre_commit.utilities import yield_python_file
from actions.utilities import log_func_call

if TYPE_CHECKING:
    from collections.abc import MutableSet
    from pathlib import Path

    from utilities.types import PathLike


def replace_sequence_strs(*paths: PathLike) -> None:
    LOGGER.info(log_func_call(replace_sequence_strs, f"{paths=}"))
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
    with yield_python_file(path, modifications=modifications) as context:
        context.output = MetadataWrapper(context.input).module.visit(
            SequenceToListTransformer()
        )


class SequenceToListTransformer(CSTTransformer):
    @override
    def leave_Subscript(
        self, original_node: Subscript, updated_node: Subscript
    ) -> Subscript:
        _ = original_node
        if matches(
            updated_node,
            MSubscript(
                value=MName("Sequence"),
                slice=[MSubscriptElement(slice=MIndex(value=MName("str")))],
            ),
        ):
            return updated_node.with_changes(value=Name("list"))
        return updated_node


__all__ = ["replace_sequence_strs"]
