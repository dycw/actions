from __future__ import annotations

import sys
from functools import partial
from typing import TYPE_CHECKING

from ordered_set import OrderedSet
from pydantic import TypeAdapter
from utilities.functions import ensure_str, get_func_name, max_nullable
from utilities.packaging import Requirement
from utilities.tabulate import func_param_desc
from utilities.text import repr_str

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
from actions.pre_commit.update_requirements.settings import SETTINGS
from actions.pre_commit.utilities import (
    get_aot,
    get_pyproject_dependencies,
    get_set_array,
    get_set_table,
    get_table,
    yield_pyproject_toml,
    yield_toml_doc,
)
from actions.utilities import logged_run

if TYPE_CHECKING:
    from collections.abc import Iterator, MutableSet
    from pathlib import Path

    from tomlkit import TOMLDocument
    from utilities.types import PathLike, StrDict

    from actions.pre_commit.update_requirements.classes import Version2or3, VersionSet


def update_requirements(
    *paths: PathLike,
    indexes: list[str] | None = SETTINGS.indexes,
    native_tls: bool = SETTINGS.native_tls,
) -> None:
    LOGGER.info(
        func_param_desc(
            update_requirements,
            __version__,
            f"{paths=}",
            f"{indexes=}",
            f"{native_tls=}",
        )
    )
    modifications: set[Path] = set()
    for path in paths:
        _format_path(
            path, indexes=indexes, native_tls=native_tls, modifications=modifications
        )
    if len(modifications) >= 1:
        LOGGER.info(
            "Exiting due to modifications: %s",
            ", ".join(map(repr_str, sorted(modifications))),
        )
        sys.exit(1)
    LOGGER.info("Finished running %r", get_func_name(update_requirements))


def _format_path(
    path: PathLike,
    /,
    *,
    versions: VersionSet | None = None,
    indexes: list[str] | None = SETTINGS.indexes,
    native_tls: bool = SETTINGS.native_tls,
    modifications: MutableSet[Path] | None = None,
) -> None:
    versions_use = (
        _get_versions(indexes=indexes, native_tls=native_tls)
        if versions is None
        else versions
    )
    with yield_toml_doc(path, modifications=modifications) as doc:
        get_pyproject_dependencies(doc).apply(
            partial(_format_req, versions=versions_use)
        )
        _pin_cli_dependencies(doc, versions_use)


def _get_versions(
    *,
    indexes: list[str] | None = SETTINGS.indexes,
    native_tls: bool = SETTINGS.native_tls,
) -> VersionSet:
    index_args: OrderedSet[str] = OrderedSet([])
    _ = index_args.update(list(_yield_indexes()))
    if indexes is not None:
        _ = index_args.update(indexes)
    head: list[str] = ["uv", "pip", "list", "--format", "json"]
    tail: list[str] = ["--strict"]
    if len(index_args) >= 1:
        tail.extend(["--index", ",".join(index_args)])
    if native_tls:
        tail.append("--native-tls")
    json1 = logged_run(*head, *tail, return_=True)
    models1 = TypeAdapter(list[PipListOutput]).validate_json(json1)
    versions1 = {p.name: parse_version2_or_3(p.version) for p in models1}
    json2 = logged_run(*head, "--outdated", *tail, return_=True)
    models2 = TypeAdapter(list[PipListOutdatedOutput]).validate_json(json2)
    versions2 = {p.name: parse_version2_or_3(p.latest_version) for p in models2}
    out: StrDict = {}
    for key in set(versions1) | set(versions2):
        out[key] = max_nullable([versions1.get(key), versions2.get(key)])
    return out


def _yield_indexes() -> Iterator[str]:
    try:
        with yield_pyproject_toml() as doc:
            try:
                tool = get_table(doc, "tool")
            except KeyError:
                return
            try:
                uv = get_table(tool, "uv")
            except KeyError:
                return
            try:
                indexes = get_aot(uv, "index")
            except KeyError:
                return
            else:
                for index in indexes:
                    yield ensure_str(index["url"])
    except FileNotFoundError:
        return


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


def _pin_cli_dependencies(doc: TOMLDocument, versions: VersionSet, /) -> None:
    try:
        project = get_table(doc, "project")
    except KeyError:
        return
    try:
        _ = get_table(project, "scripts")
    except KeyError:
        return
    dependencies = get_set_array(project, "dependencies")
    opt_dependencies = get_set_table(project, "optional-dependencies")
    cli = get_set_array(opt_dependencies, "cli")
    cli.clear()
    for dep in dependencies:
        Requirement(dep).replace()
        a


__all__ = ["update_requirements"]
