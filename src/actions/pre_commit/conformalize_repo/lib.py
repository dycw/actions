from __future__ import annotations

import sys
from hashlib import blake2b
from re import MULTILINE, escape, search, sub
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
    README_MD,
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
    ci__certificates: bool = SETTINGS.ci__certificates,
    ci__gitea: bool = SETTINGS.ci__gitea,
    ci__token_checkout: Secret[str] | None = SETTINGS.ci__token_checkout,
    ci__token_github: Secret[str] | None = SETTINGS.ci__token_github,
    ci__pull_request__pre_commit: bool = SETTINGS.ci__pull_request__pre_commit,
    ci__pull_request__pre_commit__submodules: str
    | None = SETTINGS.ci__pull_request__pre_commit__submodules,
    ci__pull_request__pyright: bool = SETTINGS.ci__pull_request__pyright,
    ci__pull_request__pytest__macos: bool = SETTINGS.ci__pull_request__pytest__macos,
    ci__pull_request__pytest__ubuntu: bool = SETTINGS.ci__pull_request__pytest__ubuntu,
    ci__pull_request__pytest__windows: bool = SETTINGS.ci__pull_request__pytest__windows,
    ci__pull_request__pytest__all_versions: bool = SETTINGS.ci__pull_request__pytest__all_versions,
    ci__pull_request__pytest__sops_age_key: Secret[str]
    | None = SETTINGS.ci__pull_request__pytest__sops_age_key,
    ci__pull_request__ruff: bool = SETTINGS.ci__pull_request__ruff,
    ci__push__publish__github: bool = SETTINGS.ci__push__publish__github,
    ci__push__publish__primary: bool = SETTINGS.ci__push__publish__primary,
    ci__push__publish__primary__job_name: str = SETTINGS.ci__push__publish__primary__job_name,
    ci__push__publish__primary__username: str
    | None = SETTINGS.ci__push__publish__primary__username,
    ci__push__publish__primary__password: Secret[str]
    | None = SETTINGS.ci__push__publish__primary__password,
    ci__push__publish__primary__publish_url: str
    | None = SETTINGS.ci__push__publish__primary__publish_url,
    ci__push__publish__secondary: bool = SETTINGS.ci__push__publish__secondary,
    ci__push__publish__secondary__job_name: str = SETTINGS.ci__push__publish__secondary__job_name,
    ci__push__publish__secondary__username: str
    | None = SETTINGS.ci__push__publish__secondary__username,
    ci__push__publish__secondary__password: Secret[str]
    | None = SETTINGS.ci__push__publish__secondary__password,
    ci__push__publish__secondary__publish_url: str
    | None = SETTINGS.ci__push__publish__secondary__publish_url,
    ci__push__tag: bool = SETTINGS.ci__push__tag,
    ci__push__tag__all: bool = SETTINGS.ci__push__tag__all,
    coverage: bool = SETTINGS.coverage,
    description: str | None = SETTINGS.description,
    package_name: str | None = SETTINGS.package_name,
    pytest: bool = SETTINGS.pytest,
    pytest__asyncio: bool = SETTINGS.pytest__asyncio,
    pytest__ignore_warnings: bool = SETTINGS.pytest__ignore_warnings,
    pytest__timeout: int | None = SETTINGS.pytest__timeout,
    python_package_name: str | None = SETTINGS.python_package_name,
    python_version: str = SETTINGS.python_version,
    readme: bool = SETTINGS.readme,
    repo_name: str | None = SETTINGS.repo_name,
    script: str | None = SETTINGS.script,
    uv__native_tls: bool = SETTINGS.uv__native_tls,
) -> None:
    modifications: set[Path] = set()
    run_ripgrep_and_replace(modifications=modifications, version=python_version)
    if (
        ci__pull_request__pre_commit
        or ci__pull_request__pyright
        or ci__pull_request__pytest__macos
        or ci__pull_request__pytest__ubuntu
        or ci__pull_request__pytest__windows
        or ci__pull_request__ruff
    ):
        add_ci_pull_request_yaml(
            gitea=ci__gitea,
            modifications=modifications,
            certificates=ci__certificates,
            pre_commit=ci__pull_request__pre_commit,
            pre_commit__submodules=ci__pull_request__pre_commit__submodules,
            pyright=ci__pull_request__pyright,
            pytest__macos=ci__pull_request__pytest__macos,
            pytest__ubuntu=ci__pull_request__pytest__ubuntu,
            pytest__windows=ci__pull_request__pytest__windows,
            pytest__all_versions=ci__pull_request__pytest__all_versions,
            pytest__sops_age_key=ci__pull_request__pytest__sops_age_key,
            pytest__timeout=pytest__timeout,
            python_version=python_version,
            repo_name=repo_name,
            script=script,
            token_checkout=ci__token_checkout,
            token_github=ci__token_github,
            uv__native_tls=uv__native_tls,
        )
    if (
        ci__push__publish__github
        or ci__push__publish__primary
        or (ci__push__publish__primary__username is not None)
        or (ci__push__publish__primary__password is not None)
        or (ci__push__publish__primary__publish_url is not None)
        or ci__push__publish__secondary
        or (ci__push__publish__secondary__username is not None)
        or (ci__push__publish__secondary__password is not None)
        or (ci__push__publish__secondary__publish_url is not None)
        or ci__push__tag
        or ci__push__tag__all
    ):
        add_ci_push_yaml(
            gitea=ci__gitea,
            modifications=modifications,
            certificates=ci__certificates,
            publish__github=ci__push__publish__github,
            publish__primary=ci__push__publish__primary,
            publish__primary__job_name=ci__push__publish__primary__job_name,
            publish__primary__username=ci__push__publish__primary__username,
            publish__primary__password=ci__push__publish__primary__password,
            publish__primary__publish_url=ci__push__publish__primary__publish_url,
            publish__secondary=ci__push__publish__secondary,
            publish__secondary__job_name=ci__push__publish__secondary__job_name,
            publish__secondary__username=ci__push__publish__secondary__username,
            publish__secondary__password=ci__push__publish__secondary__password,
            publish__secondary__publish_url=ci__push__publish__secondary__publish_url,
            tag=ci__push__tag,
            tag__all=ci__push__tag__all,
            token_checkout=ci__token_checkout,
            token_github=ci__token_github,
            uv__native_tls=uv__native_tls,
        )
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
            script=script,
        )
    if readme:
        add_readme_md(
            modifications=modifications, name=repo_name, description=description
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


def add_ci_pull_request_yaml(
    *,
    gitea: bool = SETTINGS.ci__gitea,
    modifications: MutableSet[Path] | None = None,
    certificates: bool = SETTINGS.ci__certificates,
    pre_commit: bool = SETTINGS.ci__pull_request__pre_commit,
    pre_commit__submodules: str
    | None = SETTINGS.ci__pull_request__pre_commit__submodules,
    pyright: bool = SETTINGS.ci__pull_request__pyright,
    pytest__macos: bool = SETTINGS.ci__pull_request__pytest__macos,
    pytest__ubuntu: bool = SETTINGS.ci__pull_request__pytest__ubuntu,
    pytest__windows: bool = SETTINGS.ci__pull_request__pytest__windows,
    pytest__all_versions: bool = SETTINGS.ci__pull_request__pytest__all_versions,
    pytest__sops_age_key: Secret[str]
    | None = SETTINGS.ci__pull_request__pytest__sops_age_key,
    pytest__timeout: int | None = SETTINGS.pytest__timeout,
    python_version: str = SETTINGS.python_version,
    repo_name: str | None = SETTINGS.repo_name,
    ruff: bool = SETTINGS.ci__pull_request__ruff,
    script: str | None = SETTINGS.script,
    token_checkout: Secret[str] | None = SETTINGS.ci__token_checkout,
    token_github: Secret[str] | None = SETTINGS.ci__token_github,
    uv__native_tls: bool = SETTINGS.uv__native_tls,
) -> None:
    path = GITEA_PULL_REQUEST_YAML if gitea else GITHUB_PULL_REQUEST_YAML
    with yield_yaml_dict(path, modifications=modifications) as dict_:
        dict_["name"] = "pull-request"
        on = get_set_dict(dict_, "on")
        pull_request = get_set_dict(on, "pull_request")
        branches = get_set_list_strs(pull_request, "branches")
        ensure_contains(branches, "master")
        schedule = get_set_list_dicts(on, "schedule")
        ensure_contains(schedule, {"cron": get_cron_job(repo_name=repo_name)})
        jobs = get_set_dict(dict_, "jobs")
        if pre_commit:
            pre_commit_dict = get_set_dict(jobs, "pre-commit")
            pre_commit_dict["runs-on"] = "ubuntu-latest"
            steps = get_set_list_dicts(pre_commit_dict, "steps")
            if certificates:
                ensure_contains(steps, update_ca_certificates_dict("pre-commit"))
            ensure_contains(
                steps,
                action_run_hooks_dict(
                    token_checkout=token_checkout,
                    token_github=token_github,
                    submodules=pre_commit__submodules,
                    repos=["dycw/actions", "pre-commit/pre-commit-hooks"],
                    gitea=gitea,
                ),
            )
        if pyright:
            pyright_dict = get_set_dict(jobs, "pyright")
            pyright_dict["runs-on"] = "ubuntu-latest"
            steps = get_set_list_dicts(pyright_dict, "steps")
            if certificates:
                ensure_contains(steps, update_ca_certificates_dict("pyright"))
            ensure_contains(
                steps,
                action_pyright_dict(
                    token_checkout=token_checkout,
                    token_github=token_github,
                    python_version=python_version,
                    with_requirements=script,
                    native_tls=uv__native_tls,
                ),
            )
        if pytest__macos or pytest__ubuntu or pytest__windows:
            pytest_dict = get_set_dict(jobs, "pytest")
            env = get_set_dict(pytest_dict, "env")
            env["CI"] = "1"
            pytest_dict["name"] = (
                "pytest (${{matrix.os}}, ${{matrix.python-version}}, ${{matrix.resolution}})"
            )
            pytest_dict["runs-on"] = "${{matrix.os}}"
            steps = get_set_list_dicts(pytest_dict, "steps")
            if certificates:
                ensure_contains(steps, update_ca_certificates_dict("pytest"))
            ensure_contains(
                steps,
                action_pytest_dict(
                    token_checkout=token_checkout,
                    token_github=token_github,
                    python_version="${{matrix.python-version}}",
                    sops_age_key=pytest__sops_age_key,
                    resolution="${{matrix.resolution}}",
                    native_tls=uv__native_tls,
                    with_requirements=script,
                ),
            )
            strategy_dict = get_set_dict(pytest_dict, "strategy")
            strategy_dict["fail-fast"] = False
            matrix = get_set_dict(strategy_dict, "matrix")
            os = get_set_list_strs(matrix, "os")
            if pytest__macos:
                ensure_contains(os, "macos-latest")
            if pytest__ubuntu:
                ensure_contains(os, "ubuntu-latest")
            if pytest__windows:
                ensure_contains(os, "windows-latest")
            python_version_dict = get_set_list_strs(matrix, "python-version")
            if pytest__all_versions:
                ensure_contains(
                    python_version_dict, *yield_python_versions(python_version)
                )
            else:
                ensure_contains(python_version_dict, python_version)
            resolution = get_set_list_strs(matrix, "resolution")
            ensure_contains(resolution, "highest", "lowest-direct")
            if pytest__timeout is not None:
                pytest_dict["timeout-minutes"] = max(round(pytest__timeout / 60), 1)
        if ruff:
            ruff_dict = get_set_dict(jobs, "ruff")
            ruff_dict["runs-on"] = "ubuntu-latest"
            steps = get_set_list_dicts(ruff_dict, "steps")
            if certificates:
                ensure_contains(steps, update_ca_certificates_dict("steps"))
            ensure_contains(
                steps,
                action_ruff_dict(
                    token_checkout=token_checkout, token_github=token_github
                ),
            )


##


def add_ci_push_yaml(
    *,
    gitea: bool = SETTINGS.ci__gitea,
    modifications: MutableSet[Path] | None = None,
    certificates: bool = SETTINGS.ci__certificates,
    publish__github: bool = SETTINGS.ci__push__publish__github,
    publish__primary: bool = SETTINGS.ci__push__publish__primary,
    publish__primary__job_name: str = SETTINGS.ci__push__publish__primary__job_name,
    publish__primary__username: str
    | None = SETTINGS.ci__push__publish__primary__username,
    publish__primary__password: Secret[str]
    | None = SETTINGS.ci__push__publish__primary__password,
    publish__primary__publish_url: str
    | None = SETTINGS.ci__push__publish__primary__publish_url,
    publish__secondary: bool = SETTINGS.ci__push__publish__secondary,
    publish__secondary__job_name: str = SETTINGS.ci__push__publish__secondary__job_name,
    publish__secondary__username: str
    | None = SETTINGS.ci__push__publish__secondary__username,
    publish__secondary__password: Secret[str]
    | None = SETTINGS.ci__push__publish__secondary__password,
    publish__secondary__publish_url: str
    | None = SETTINGS.ci__push__publish__secondary__publish_url,
    tag: bool = SETTINGS.ci__push__tag,
    tag__all: bool = SETTINGS.ci__push__tag__all,
    token_checkout: Secret[str] | None = SETTINGS.ci__token_checkout,
    token_github: Secret[str] | None = SETTINGS.ci__token_github,
    uv__native_tls: bool = SETTINGS.uv__native_tls,
) -> None:
    path = GITEA_PUSH_YAML if gitea else GITHUB_PUSH_YAML
    with yield_yaml_dict(path, modifications=modifications) as dict_:
        dict_["name"] = "push"
        on = get_set_dict(dict_, "on")
        push = get_set_dict(on, "push")
        branches = get_set_list_strs(push, "branches")
        ensure_contains(branches, "master")
        jobs = get_set_dict(dict_, "jobs")
        if publish__github:
            _add_ci_push_yaml_publish_dict(
                jobs,
                "github",
                github=True,
                token_checkout=token_checkout,
                token_github=token_github,
            )
        if publish__primary:
            _add_ci_push_yaml_publish_dict(
                jobs,
                publish__primary__job_name,
                certificates=certificates,
                token_checkout=token_checkout,
                token_github=token_github,
                username=publish__primary__username,
                password=publish__primary__password,
                publish_url=publish__primary__publish_url,
                uv__native_tls=uv__native_tls,
            )
        if publish__secondary:
            _add_ci_push_yaml_publish_dict(
                jobs,
                publish__secondary__job_name,
                certificates=certificates,
                token_checkout=token_checkout,
                token_github=token_github,
                username=publish__secondary__username,
                password=publish__secondary__password,
                publish_url=publish__secondary__publish_url,
                uv__native_tls=uv__native_tls,
            )
        if tag:
            tag_dict = get_set_dict(jobs, "tag")
            tag_dict["runs-on"] = "ubuntu-latest"
            steps = get_set_list_dicts(tag_dict, "steps")
            if certificates:
                ensure_contains(steps, update_ca_certificates_dict("tag"))
            ensure_contains(
                steps,
                action_tag_commit_dict(
                    major_minor=tag__all, major=tag__all, latest=tag__all
                ),
            )


def _add_ci_push_yaml_publish_dict(
    jobs: StrDict,
    name: str,
    /,
    *,
    github: bool = False,
    certificates: bool = SETTINGS.ci__certificates,
    token_checkout: Secret[str] | None = SETTINGS.ci__token_checkout,
    token_github: Secret[str] | None = SETTINGS.ci__token_github,
    username: str | None = None,
    password: Secret[str] | None = None,
    publish_url: str | None = None,
    uv__native_tls: bool = SETTINGS.uv__native_tls,
) -> None:
    publish_name = f"publish-{name}"
    publish_dict = get_set_dict(jobs, publish_name)
    if github:
        environment = get_set_dict(publish_dict, "environment")
        environment["name"] = "pypi"
        permissions = get_set_dict(publish_dict, "permissions")
        permissions["id-token"] = "write"
    publish_dict["runs-on"] = "ubuntu-latest"
    steps = get_set_list_dicts(publish_dict, "steps")
    if certificates:
        ensure_contains(steps, update_ca_certificates_dict(publish_name))
    ensure_contains(
        steps,
        action_publish_package_dict(
            token_checkout=token_checkout,
            token_github=token_github,
            username=username,
            password=password,
            publish_url=publish_url,
            native_tls=uv__native_tls,
        ),
    )


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
    script: str | None = SETTINGS.script,
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
        ensure_contains(testpaths, "src/tests" if script is None else "tests")
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


def add_readme_md(
    *,
    modifications: MutableSet[Path] | None = None,
    name: str | None = SETTINGS.package_name,
    description: str | None = SETTINGS.description,
) -> None:
    with yield_text_file(README_MD, modifications=modifications) as context:
        lines: list[str] = []
        if name is not None:
            lines.append(f"# `{name}`")
        if description is not None:
            lines.append(description)
        text = "\n\n".join(lines)
        if search(escape(text), context.output, flags=MULTILINE) is None:
            context.output += f"\n\n{text}"


##


def get_cron_job(*, repo_name: str | None = SETTINGS.repo_name) -> str:
    if repo_name is None:
        minute = hour = 0
    else:
        digest = blake2b(repo_name.encode(), digest_size=8).digest()
        value = int.from_bytes(digest, "big")
        minute = value % 60
        hour = (value // 60) % 24
    return f"{minute} {hour} * * *"


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


def get_tool_uv(doc: TOMLDocument, /) -> Table:
    tool = get_set_table(doc, "tool")
    return get_set_table(tool, "uv")


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


def yield_python_versions(
    version: str, /, *, max_: str = MAX_PYTHON_VERSION
) -> Iterator[str]:
    major, minor = _yield_python_version_tuple(version)
    max_major, max_minor = _yield_python_version_tuple(max_)
    if major != max_major:
        msg = f"Major versions must be equal; got {major} and {max_major}"
        raise ValueError(msg)
    if minor > max_minor:
        msg = f"Minor version must be at most {max_minor}; got {minor}"
        raise ValueError(msg)
    for i in range(minor, max_minor + 1):
        yield f"{major}.{i}"


def _yield_python_version_tuple(version: str, /) -> tuple[int, int]:
    major, minor = extract_groups(r"^(\d+)\.(\d+)$", version)
    return int(major), int(minor)


##


__all__ = [
    "add_ci_pull_request_yaml",
    "add_ci_push_yaml",
    "add_coveragerc_toml",
    "add_pytest_toml",
    "add_readme_md",
    "get_cron_job",
    "get_python_package_name",
    "get_tool_uv",
    "run_ripgrep_and_replace",
    "yield_python_versions",
]
