from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from utilities.functions import get_func_name
from utilities.inflect import counted_noun
from utilities.text import repr_str

from actions.constants import COVERAGERC_TOML, PYTEST_TOML
from actions.logging import LOGGER
from actions.pre_commit.conformalize_repo.settings import SETTINGS
from actions.pre_commit.utilities import (
    ensure_contains,
    get_set_array,
    get_set_table,
    yield_toml_doc,
)

if TYPE_CHECKING:
    from collections.abc import MutableSet
    from pathlib import Path


def conformalize_repo(
    *,
    package_name: str | None = SETTINGS.package_name,
    pytest: bool = SETTINGS.pytest,
    pytest__asyncio: bool = SETTINGS.pytest__asyncio,
    pytest__ignore_warnings: bool = SETTINGS.pytest__ignore_warnings,
    pytest__timeout: int | None = SETTINGS.pytest__timeout,
    python_package_name: str | None = SETTINGS.python_package_name,
) -> None:
    modifications: set[Path] = set()
    if (
        pytest
        or pytest__asyncio
        or pytest__ignore_warnings
        or (pytest__timeout is not None)
    ):
        add_pytest_toml(
            modifications=modifications,
            asyncio=pytest__asyncio,
            ignore_warnings=pytest__ignore_warnings,
            timeout=pytest__timeout,
            coverage=coverage,
            package_name=package_name,
            python_package_name=python_package_name,
        )
    if len(modifications) >= 1:
        LOGGER.info(
            "Exiting due to %s: %s",
            counted_noun(modifications, "modification"),
            ", ".join(map(repr_str, sorted(modifications))),
        )
        sys.exit(1)
    LOGGER.info("Finished running %r", get_func_name(conformalize_repo))


##


def add_pytest_toml(
    *,
    modifications: MutableSet[Path] | None = None,
    asyncio: bool = SETTINGS.pytest__asyncio,
    ignore_warnings: bool = SETTINGS.pytest__ignore_warnings,
    timeout: int | None = SETTINGS.pytest__timeout,
    coverage: bool = SETTINGS.coverage,
    package_name: str | None = SETTINGS.package_name,
    python_package_name: str | None = SETTINGS.python_package_name,
) -> None:
    with yield_toml_doc(PYTEST_TOML, modifications=modifications) as doc:
        pytest = get_set_table(doc, "pytest")
        addopts = get_set_array(pytest, "addopts")
        ensure_contains(
            addopts,
            "-ra",
            "-vv",
            "--color=auto",
            "--durations=10",
            "--durations-min=10",
        )
        if coverage and (
            (
                python_package_name_use := get_python_package_name(
                    package_name=package_name, python_package_name=python_package_name
                )
            )
            is not None
        ):
            ensure_contains(
                addopts,
                f"--cov={python_package_name_use}",
                f"--cov-config={COVERAGERC_TOML}",
                "--cov-report=html",
            )
        pytest["collect_imported_tests"] = False
        pytest["empty_parameter_set_mark"] = "fail_at_collect"
        filterwarnings = get_set_array(pytest, "filterwarnings")
        ensure_contains(filterwarnings, "error")
        pytest["minversion"] = "9.0"
        pytest["strict"] = True
        testpaths = get_set_array(pytest, "testpaths")
        ensure_contains(testpaths, "src/tests")
        pytest["xfail_strict"] = True
        if asyncio:
            pytest["asyncio_default_fixture_loop_scope"] = "function"
            pytest["asyncio_mode"] = "auto"
        if ignore_warnings:
            filterwarnings = get_set_array(pytest, "filterwarnings")
            ensure_contains(
                filterwarnings,
                "ignore::DeprecationWarning",
                "ignore::ResourceWarning",
                "ignore::RuntimeWarning",
            )
        if timeout is not None:
            pytest["timeout"] = str(timeout)


##


def get_python_package_name(
    *,
    package_name: str | None = SETTINGS.package_name,
    python_package_name: str | None = SETTINGS.python_package_name,
) -> str | None:
    if python_package_name is not None:
        return python_package_name
    if package_name is not None:
        return package_name.replace("-", "_")
    return None


##


__all__ = ["add_coveragerc_toml", "add_pytest_toml", "get_python_package_name"]
