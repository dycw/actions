from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING, override

from libcst import CSTTransformer, Module, Name, Subscript, parse_module
from libcst.matchers import Index as MIndex
from libcst.matchers import Name as MName
from libcst.matchers import Subscript as MSubscript
from libcst.matchers import SubscriptElement as MSubscriptElement
from libcst.matchers import matches
from libcst.metadata import MetadataWrapper
from utilities.text import repr_str, strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.utilities import are_modules_equal, write_text

if TYPE_CHECKING:
    from utilities.types import PathLike


_MODIFICATIONS: set[Path] = set()


def replace_sequence_strs(*paths: PathLike) -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - paths = %s
        """),
        replace_sequence_strs.__name__,
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
    if path.suffix != ".py":
        msg = f"Expected a Python file; got {str(path)!r}"
        raise TypeError(msg)
    current = parse_module(path.read_text())
    expected = _get_formatted(path)
    if not are_modules_equal(current, expected):
        write_text(path, expected.code, modifications=_MODIFICATIONS)


def _get_formatted(path: PathLike, /) -> Module:
    path = Path(path)
    wrapper = MetadataWrapper(parse_module(path.read_text()))
    return wrapper.module.visit(SequenceToListTransformer())


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
