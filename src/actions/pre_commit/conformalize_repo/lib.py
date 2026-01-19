from __future__ import annotations

import sys
from hashlib import blake2b
from re import MULTILINE, sub
from typing import TYPE_CHECKING

from utilities.functions import get_func_name
from utilities.inflect import counted_noun
from utilities.re import extract_groups
from utilities.subprocess import ripgrep
from utilities.text import repr_str

from actions.constants import (
    COVERAGERC_TOML,
    GITEA_PULL_REQUEST_YAML,
    GITEA_PUSH_YAML,
    GITHUB_PULL_REQUEST_YAML,
    GITHUB_PUSH_YAML,
    MAX_PYTHON_VERSION,
    PYTEST_TOML,
)
from actions.logging import LOGGER
from actions.pre_commit.conformalize_repo.action_dicts import (
    action_publish_package_dict,
    action_pyright_dict,
    action_pytest_dict,
    action_ruff_dict,
    action_run_hooks_dict,
    action_tag_commit_dict,
    update_ca_certificates_dict,
)
from actions.pre_commit.conformalize_repo.settings import SETTINGS
from actions.pre_commit.utilities import (
    ensure_contains,
    get_set_array,
    get_set_dict,
    get_set_list_dicts,
    get_set_list_strs,
    get_set_table,
    yield_text_file,
    yield_toml_doc,
    yield_yaml_dict,
)

if TYPE_CHECKING:
    from collections.abc import Iterator, MutableSet
    from pathlib import Path

    from tomlkit import TOMLDocument
    from tomlkit.items import Table
    from typed_settings import Secret
    from utilities.types import StrDict


def conformalize_repo(
    *,
    coverage: bool = SETTINGS.coverage,
    package_name: str | None = SETTINGS.package_name,
    pytest: bool = SETTINGS.pytest,
    pytest__asyncio: bool = SETTINGS.pytest__asyncio,
    pytest__ignore_warnings: bool = SETTINGS.pytest__ignore_warnings,
    pytest__timeout: int | None = SETTINGS.pytest__timeout,
    python_package_name: str | None = SETTINGS.python_package_name,
    python_version: str = SETTINGS.python_version,
) -> None:
    modifications: set[Path] = set()
    run_ripgrep_and_replace(modifications=modifications, version=python_version)
    if coverage:
        add_coveragerc_toml(modifications=modifications)
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


def add_coveragerc_toml(*, modifications: MutableSet[Path] | None = None) -> None:
    with yield_toml_doc(COVERAGERC_TOML, modifications=modifications) as doc:
        html = get_set_table(doc, "html")
        html["directory"] = ".coverage/html"
        report = get_set_table(doc, "report")
        exclude_also = get_set_array(report, "exclude_also")
        ensure_contains(exclude_also, "@overload", "if TYPE_CHECKING:")
        report["fail_under"] = 100.0
        report["skip_covered"] = True
        report["skip_empty"] = True
        run = get_set_table(doc, "run")
        run["branch"] = True
        run["data_file"] = ".coverage/data"
        run["parallel"] = True


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


def run_ripgrep_and_replace(
    *,
    version: str = SETTINGS.python_version,
    modifications: MutableSet[Path] | None = None,
) -> None:
    result = ripgrep(
        "--files-with-matches",
        "--pcre2",
        "--type=py",
        rf'# requires-python = ">=(?!{version})\d+\.\d+"',
    )
    if result is None:
        return
    for path in result.splitlines():
        with yield_text_file(path, modifications=modifications) as context:
            context.output = sub(
                r'# requires-python = ">=\d+\.\d+"',
                rf'# requires-python = ">={version}"',
                context.input,
                flags=MULTILINE,
            )


##


__all__ = [
    "add_coveragerc_toml",
    "add_pytest_toml",
    "get_python_package_name",
    "run_ripgrep_and_replace",
]
