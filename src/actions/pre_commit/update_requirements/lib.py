from __future__ import annotations

import sys
from contextlib import suppress
from functools import partial
from typing import TYPE_CHECKING

from pydantic import TypeAdapter
from utilities.functions import max_nullable, min_nullable
from utilities.packaging import Requirement
from utilities.text import repr_str, strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.pre_commit.update_requirements.classes import (
    PipListOutdatedOutput,
    PipListOutput,
    TwoSidedVersions,
    Version1or2,
    Version2,
    Version3,
    Versions,
    parse_version1_or_2,
    parse_version2_or_3,
)
from actions.pre_commit.utilities import get_pyproject_dependencies, yield_toml_doc
from actions.utilities import logged_run

if TYPE_CHECKING:
    from collections.abc import MutableSet
    from pathlib import Path

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
    versions: VersionSet | None = None,
    modifications: MutableSet[Path] | None = None,
) -> None:
    versions_use = _get_version_set(path) if versions is None else versions
    with yield_toml_doc(path, modifications=modifications) as doc:
        get_pyproject_dependencies(doc).apply(
            partial(_format_req, versions=versions_use)
        )


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
    items: list[tuple[str, Version2or3 | None, Version1or2 | None]] = []

    def collect(requirement: Requirement, /) -> Requirement:
        try:
            lower = parse_version2_or_3(requirement[">="])
        except KeyError:
            lower = None
        try:
            upper = parse_version1_or_2(requirement["<"])
        except KeyError:
            upper = None
        items.append((requirement.name, lower, upper))
        return requirement

    with yield_toml_doc(path) as doc:
        get_pyproject_dependencies(doc).apply(collect)

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


def _format_req(requirement: Requirement, /, *, versions: VersionSet) -> Requirement:
    parts: list[str] = []
    versions_i = versions[requirement.name]
    match versions_i.pyproject_lower, versions_i.pyproject_upper, versions_i.latest:
        case None, None, None:
            ...
        case Version2() | Version3() as lower, None, None:
            parts.append(f">={lower}")
        case (Version2() as lower, None, Version2() as latest) | (
            Version3() as lower,
            None,
            Version3() as latest,
        ):
            parts.append(f">={max(lower, latest)}")
        case None, int() | Version2() as upper, None:
            parts.append(f"<{upper}")
        case None, int() as upper, Version2() as latest:
            bumped = latest.bump_major()
            parts.append(f"<{max(upper, bumped.major)}")
        case None, Version2() as upper, Version3() as latest:
            bumped = latest.bump_minor()
            parts.append(f"<{max(upper, Version2(bumped.major, bumped.minor))}")
        case (Version2() as lower, int() as upper, None) | (
            Version3() as lower,
            Version2() as upper,
            None,
        ):
            bumped = lower.bump_major()
            parts.extend([f">={lower}", f"<{bumped.major}"])
        case (Version2() as lower, int() as upper, Version2() as latest) | (
            Version3() as lower,
            Version2() as upper,
            Version3() as latest,
        ):
            new_lower = max(lower, latest)
            bumped = new_lower.bump_major()
            parts.extend([f">={new_lower}", f"<{bumped.major}"])
        case never:
            raise NotImplementedError(never)
    return Requirement.new(" ".join([requirement.name, ",".join(parts)]))


__all__ = ["update_requirements"]
