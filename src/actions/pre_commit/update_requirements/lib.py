from __future__ import annotations

import sys
from contextlib import suppress
from typing import TYPE_CHECKING

from packaging.requirements import Requirement
from pydantic import TypeAdapter
from utilities.functions import ensure_str, max_nullable, min_nullable
from utilities.packaging import Requirement
from utilities.text import repr_str, strip_and_dedent
from utilities.version import ParseVersionError
from utilities.version import parse_version as parse_version3

from actions import __version__
from actions.logging import LOGGER
from actions.pre_commit.update_requirements.classes import (
    PipListOutdatedOutput,
    PipListOutput,
    TwoSidedVersions,
    Versions,
    parse_version2,
    parse_version2_or_3,
)
from actions.pre_commit.utilities import get_pyproject_dependencies, yield_toml_doc
from actions.utilities import logged_run

if TYPE_CHECKING:
    from collections.abc import Iterator, MutableSet
    from pathlib import Path

    from tomlkit.items import Array
    from utilities.types import PathLike

    from actions.pre_commit.update_requirements.classes import Version2or3, VersionSet


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
    path: PathLike,
    /,
    *,
    versions: dict[str, VersionSet] | None = None,
    modifications: MutableSet[Path] | None = None,
) -> None:
    # assert 0, _get_pyproject_versions(path)
    versions_use = _get_version_set(path) if versions is None else versions
    with yield_toml_doc(path, modifications=modifications) as doc:
        assert 0, versions_use
        get_pyproject_dependencies(doc)
        assert 0, _get_version_set()
        modifications.add(py_typed)


def _get_version_set(path: PathLike, /) -> VersionSet:
    out: dict[str, Versions] = {}
    for key, (lower, upper) in _get_pyproject_versions(path).items():
        versions = out.get(key, Versions())
        versions.pyproject_lower = lower
        versions.pyproject_upper = upper
        out[key] = versions
    for key, value in _get_pip_list_versions().items():
        with suppress(KeyError):
            versions = out[key]
            versions.current = value
    for key, value in _get_pip_list_outdated_versions().items():
        with suppress(KeyError):
            versions = out[key]
            versions.latest = value
            out[key] = versions
    return out


def _get_pyproject_versions(path: PathLike, /) -> dict[str, TwoSidedVersions]:
    items: list[tuple[str, Version2or3 | None, Version2or3 | None]] = []
    with yield_toml_doc(path) as doc:
        project_deps = get_pyproject_dependencies(doc)
        if (deps := project_deps.dependencies) is not None:
            items.extend(_get_pyproject_versions_yield_array(deps))
        if (opt_depedencies := project_deps.opt_dependencies) is not None:
            for array in opt_depedencies.values():
                items.extend(_get_pyproject_versions_yield_array(array))
        if (dep_grps := project_deps.dep_groups) is not None:
            for array in dep_grps.values():
                items.extend(_get_pyproject_versions_yield_array(array))
    out: dict[str, TwoSidedVersions] = {}
    for key, lower, upper in items:
        try:
            curr_lower, curr_upper = out[key]
        except KeyError:
            out[key] = (lower, upper)
        else:
            out[key] = (
                max_nullable([curr_lower, lower], default=None),
                min_nullable([curr_upper, upper], default=None),
            )
    return out


def _get_pyproject_versions_yield_array(
    array: Array, /
) -> Iterator[tuple[str, Version2or3 | None, Version2or3 | None]]:
    for item in array:
        req = Requirement.new(ensure_str(item))
        try:
            lower = parse_version2_or_3(req[">="])
        except KeyError:
            lower = None
        try:
            upper = parse_version2_or_3(req["<"])
        except KeyError:
            upper = None
        yield req.name, lower, upper


def _get_pip_list_versions() -> dict[str, Version2or3]:
    json = logged_run("uv", "pip", "list", "--format", "json", "--strict", return_=True)
    packages = TypeAdapter(list[PipListOutput]).validate_json(json)
    return {p.name: parse_version2_or_3(p.version) for p in packages}


def _get_pip_list_outdated_versions() -> dict[str, Version2or3]:
    json = logged_run(
        "uv", "pip", "list", "--format", "json", "--outdated", "--strict", return_=True
    )
    packages = TypeAdapter(list[PipListOutdatedOutput]).validate_json(json)
    return {p.name: parse_version2_or_3(p.version) for p in packages}


__all__ = ["update_requirements"]
