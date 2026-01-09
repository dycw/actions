from __future__ import annotations

import sys
from functools import partial
from typing import TYPE_CHECKING

from pydantic import TypeAdapter
from utilities.functions import max_nullable
from utilities.text import repr_str, strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.pre_commit.update_requirements.classes import (
    PipListOutdatedOutput,
    PipListOutput,
    Version1or2,
    Version2,
    Version3,
    parse_version1_or_2,
    parse_version2_or_3,
)
from actions.pre_commit.utilities import get_pyproject_dependencies, yield_toml_doc
from actions.utilities import logged_run

if TYPE_CHECKING:
    from collections.abc import MutableSet
    from pathlib import Path

    from utilities.packaging import Requirement
    from utilities.types import PathLike, StrDict

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
    versions_use = _get_versions() if versions is None else versions
    with yield_toml_doc(path, modifications=modifications) as doc:
        get_pyproject_dependencies(doc).apply(
            partial(_format_req, versions=versions_use)
        )


def _get_versions() -> VersionSet:
    json1 = logged_run(
        "uv", "pip", "list", "--format", "json", "--strict", return_=True
    )
    models1 = TypeAdapter(list[PipListOutput]).validate_json(json1)
    versions1 = {p.name: parse_version2_or_3(p.version) for p in models1}
    json2 = logged_run(
        "uv", "pip", "list", "--format", "json", "--outdated", "--strict", return_=True
    )
    models2 = TypeAdapter(list[PipListOutdatedOutput]).validate_json(json2)
    versions2 = {p.name: parse_version2_or_3(p.latest_version) for p in models2}
    out: StrDict = {}
    for key in set(versions1) | set(versions2):
        out[key] = max_nullable([versions1.get(key), versions2.get(key)])
    return out


def _format_req(requirement: Requirement, /, *, versions: VersionSet) -> Requirement:
    try:
        lower = parse_version2_or_3(requirement[">="])
    except KeyError:
        lower = None
    try:
        upper = parse_version1_or_2(requirement["<"])
    except KeyError:
        upper = None
    latest = versions.get(requirement.name)
    new_lower: Version2or3 | None = None
    new_upper: Version1or2 | None = None
    match lower, upper, latest:
        case None, None, None:
            ...
        case None, None, Version2() | Version3():
            new_lower = latest
            new_upper = latest.bump_major().major
        case Version2() | Version3(), None, None:
            new_lower = lower
        case (Version2(), None, Version2()) | (Version3(), None, Version3()):
            new_lower = max(lower, latest)
        case None, int() | Version2(), None:
            new_upper = upper
        case None, int(), Version2():
            new_upper = max(upper, latest.bump_major().major)
        case None, Version2(), Version3():
            bumped = latest.bump_minor()
            new_upper = max(upper, Version2(bumped.major, bumped.minor))
        case (
            (Version2(), int(), None)
            | (Version3(), int(), None)
            | (Version3(), Version2(), None)
        ):
            new_lower = lower
            new_upper = lower.bump_major().major
        case (
            (Version2(), int(), Version2())
            | (Version3(), int(), Version3())
            | (Version3(), Version2(), Version3())
        ):
            new_lower = max(lower, latest)
            new_upper = new_lower.bump_major().major
        case never:
            raise NotImplementedError(never)
    if new_lower is not None:
        requirement = requirement.replace(">=", str(new_lower))
    if new_upper is not None:
        requirement = requirement.replace("<", str(new_upper))
    return requirement


__all__ = ["update_requirements"]
