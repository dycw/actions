from __future__ import annotations

import sys
from typing import TYPE_CHECKING, Any, override

from packaging._tokenizer import ParserSyntaxError
from packaging.requirements import InvalidRequirement, Requirement, _parse_requirement
from packaging.specifiers import Specifier, SpecifierSet
from tomlkit import string
from utilities.functions import ensure_str
from utilities.text import repr_str, strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.pre_commit.utilities import (
    ensure_contains,
    get_pyproject_dependencies,
    yield_toml_doc,
)

if TYPE_CHECKING:
    from collections.abc import Iterator, MutableSet
    from pathlib import Path

    from tomlkit.items import Array
    from utilities.types import PathLike


def format_requirements(*paths: PathLike) -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - paths = %s
        """),
        format_requirements.__name__,
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
        if (deps := project_deps.dependencies) is not None:
            _format_array(deps)
        if (opt_depedencies := project_deps.opt_dependencies) is not None:
            for array in opt_depedencies.values():
                _format_array(array)
        if (dep_grps := project_deps.dep_groups) is not None:
            for array in dep_grps.values():
                _format_array(array)


def _format_array(dependencies: Array, /) -> None:
    formatted = list(map(_format_item, dependencies))
    dependencies.clear()
    ensure_contains(dependencies, *formatted)


def _format_item(item: Any, /) -> Any:
    return string(str(_CustomRequirement(ensure_str(item))))


class _CustomRequirement(Requirement):
    @override
    def __init__(self, requirement_string: str) -> None:
        super().__init__(requirement_string)
        try:
            parsed = _parse_requirement(requirement_string)
        except ParserSyntaxError as e:
            raise InvalidRequirement(str(e)) from e
        self.specifier = _CustomSpecifierSet(parsed.specifier)

    @override
    def _iter_parts(self, name: str) -> Iterator[str]:
        yield name
        if self.extras:
            formatted_extras = ",".join(sorted(self.extras))
            yield f"[{formatted_extras}]"
        if self.specifier:
            yield f" {self.specifier}"
        if self.url:
            yield f"@ {self.url}"
            if self.marker:
                yield " "
        if self.marker:
            yield f"; {self.marker}"


class _CustomSpecifierSet(SpecifierSet):
    @override
    def __str__(self) -> str:
        specs = sorted(self._specs, key=self._key)
        return ", ".join(map(str, specs))

    def _key(self, spec: Specifier, /) -> int:
        return [">=", "<"].index(spec.operator)


__all__ = ["format_requirements"]
