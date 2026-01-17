from __future__ import annotations

import sys
from contextlib import contextmanager, suppress
from hashlib import blake2b
from itertools import product
from pathlib import Path
from re import MULTILINE, escape, search, sub
from shlex import join
from string import Template
from subprocess import CalledProcessError
from typing import TYPE_CHECKING, Literal, assert_never

import tomlkit
from tomlkit import TOMLDocument, table
from tomlkit.exceptions import NonExistentKey
from utilities.functions import get_func_name
from utilities.inflect import counted_noun
from utilities.re import extract_groups
from utilities.subprocess import ripgrep
from utilities.tabulate import func_param_desc
from utilities.text import repr_str, strip_and_dedent
from utilities.throttle import throttle
from utilities.version import ParseVersionError, Version, parse_version

from actions import __version__
from actions.constants import (
    ACTIONS_URL,
    BUMPVERSION_TOML,
    COVERAGERC_TOML,
    ENVRC,
    GITEA_PULL_REQUEST_YAML,
    GITEA_PUSH_YAML,
    GITHUB,
    GITHUB_PULL_REQUEST_YAML,
    GITHUB_PUSH_YAML,
    GITIGNORE,
    MAX_PYTHON_VERSION,
    PRE_COMMIT_CONFIG_YAML,
    PYPROJECT_TOML,
    PYRIGHTCONFIG_JSON,
    PYTEST_TOML,
    README_MD,
    RUFF_TOML,
    YAML_INSTANCE,
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
from actions.pre_commit.conformalize_repo.constants import (
    CONFORMALIZE_REPO_SUB_CMD,
    DOCKERFMT_URL,
    PATH_CONFIGS,
    PRE_COMMIT_HOOKS_URL,
    RUFF_URL,
    SHELLCHECK_URL,
    SHFMT_URL,
    TAPLO_URL,
    UV_URL,
)
from actions.pre_commit.conformalize_repo.settings import SETTINGS
from actions.pre_commit.constants import THROTTLE_DURATION
from actions.pre_commit.format_requirements.constants import FORMAT_REQUIREMENTS_SUB_CMD
from actions.pre_commit.replace_sequence_strs.constants import (
    REPLACE_SEQUENCE_STRS_SUB_CMD,
)
from actions.pre_commit.touch_empty_py.constants import TOUCH_EMPTY_PY_SUB_CMD
from actions.pre_commit.touch_py_typed.constants import TOUCH_PY_TYPED_SUB_CMD
from actions.pre_commit.update_requirements.constants import UPDATE_REQUIREMENTS_SUB_CMD
from actions.pre_commit.utilities import (
    ensure_contains,
    ensure_contains_partial_dict,
    ensure_contains_partial_str,
    ensure_not_contains,
    get_set_aot,
    get_set_array,
    get_set_dict,
    get_set_list_dicts,
    get_set_list_strs,
    get_set_table,
    path_throttle_cache,
    yield_json_dict,
    yield_pyproject_toml,
    yield_text_file,
    yield_toml_doc,
    yield_yaml_dict,
)
from actions.utilities import logged_run

if TYPE_CHECKING:
    from collections.abc import Iterator, MutableSet

    from tomlkit.items import Table
    from typed_settings import Secret
    from utilities.types import PathLike, StrDict


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
    envrc: bool = SETTINGS.envrc,
    envrc__uv: bool = SETTINGS.envrc__uv,
    gitignore: bool = SETTINGS.gitignore,
    package_name: str | None = SETTINGS.package_name,
    pre_commit__dockerfmt: bool = SETTINGS.pre_commit__dockerfmt,
    pre_commit__prettier: bool = SETTINGS.pre_commit__prettier,
    pre_commit__python: bool = SETTINGS.pre_commit__python,
    pre_commit__ruff: bool = SETTINGS.pre_commit__ruff,
    pre_commit__shell: bool = SETTINGS.pre_commit__shell,
    pre_commit__taplo: bool = SETTINGS.pre_commit__taplo,
    pre_commit__uv: bool = SETTINGS.pre_commit__uv,
    pyproject: bool = SETTINGS.pyproject,
    pyproject__project__optional_dependencies__scripts: bool = SETTINGS.pyproject__project__optional_dependencies__scripts,
    pyright: bool = SETTINGS.pyright,
    pytest: bool = SETTINGS.pytest,
    pytest__asyncio: bool = SETTINGS.pytest__asyncio,
    pytest__ignore_warnings: bool = SETTINGS.pytest__ignore_warnings,
    pytest__timeout: int | None = SETTINGS.pytest__timeout,
    python_package_name: str | None = SETTINGS.python_package_name,
    python_version: str = SETTINGS.python_version,
    readme: bool = SETTINGS.readme,
    repo_name: str | None = SETTINGS.repo_name,
    ruff: bool = SETTINGS.ruff,
    run_version_bump: bool = SETTINGS.run_version_bump,
    script: str | None = SETTINGS.script,
    uv__indexes: list[tuple[str, str]] = SETTINGS.uv__indexes,
    uv__native_tls: bool = SETTINGS.uv__native_tls,
) -> None:
    LOGGER.info(
        func_param_desc(
            conformalize_repo,
            __version__,
            f"{ci__certificates=}",
            f"{ci__gitea=}",
            f"{ci__token_checkout=}",
            f"{ci__token_github=}",
            f"{ci__pull_request__pre_commit=}",
            f"{ci__pull_request__pre_commit__submodules=}",
            f"{ci__pull_request__pyright=}",
            f"{ci__pull_request__pytest__macos=}",
            f"{ci__pull_request__pytest__ubuntu=}",
            f"{ci__pull_request__pytest__windows=}",
            f"{ci__pull_request__pytest__all_versions=}",
            f"{ci__pull_request__pytest__sops_age_key=}",
            f"{ci__pull_request__ruff=}",
            f"{ci__push__publish__github=}",
            f"{ci__push__publish__primary=}",
            f"{ci__push__publish__primary__job_name=}",
            f"{ci__push__publish__primary__username=}",
            f"{ci__push__publish__primary__password=}",
            f"{ci__push__publish__primary__publish_url=}",
            f"{ci__push__publish__secondary=}",
            f"{ci__push__publish__secondary__job_name=}",
            f"{ci__push__publish__secondary__username=}",
            f"{ci__push__publish__secondary__password=}",
            f"{ci__push__publish__secondary__publish_url=}",
            f"{ci__push__tag=}",
            f"{ci__push__tag__all=}",
            f"{coverage=}",
            f"{description=}",
            f"{envrc=}",
            f"{envrc__uv=}",
            f"{gitignore=}",
            f"{package_name=}",
            f"{pre_commit__dockerfmt=}",
            f"{pre_commit__prettier=}",
            f"{pre_commit__python=}",
            f"{pre_commit__ruff=}",
            f"{pre_commit__shell=}",
            f"{pre_commit__taplo=}",
            f"{pre_commit__uv=}",
            f"{pyproject=}",
            f"{pyproject__project__optional_dependencies__scripts=}",
            f"{pyright=}",
            f"{pytest=}",
            f"{pytest__asyncio=}",
            f"{pytest__ignore_warnings=}",
            f"{pytest__timeout=}",
            f"{python_package_name=}",
            f"{python_version=}",
            f"{readme=}",
            f"{repo_name=}",
            f"{ruff=}",
            f"{run_version_bump=}",
            f"{script=}",
            f"{uv__indexes=}",
            f"{uv__native_tls=}",
        )
    )
    modifications: set[Path] = set()
    add_bumpversion_toml(
        modifications=modifications,
        pyproject=pyproject,
        package_name=package_name,
        python_package_name=python_package_name,
    )
    check_versions()
    run_pre_commit_update(modifications=modifications)
    run_ripgrep_and_replace(modifications=modifications, version=python_version)
    update_action_file_extensions(modifications=modifications)
    update_action_versions(modifications=modifications)
    add_pre_commit_config_yaml(
        modifications=modifications,
        dockerfmt=pre_commit__dockerfmt,
        prettier=pre_commit__prettier,
        python=pre_commit__python,
        ruff=pre_commit__ruff,
        shell=pre_commit__shell,
        taplo=pre_commit__taplo,
        uv=pre_commit__uv,
        script=script,
        uv__indexes=uv__indexes,
        uv__native_tls=uv__native_tls,
    )
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
            ruff=ruff,
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
    if envrc or envrc__uv:
        add_envrc(
            modifications=modifications,
            uv=envrc__uv,
            uv__native_tls=uv__native_tls,
            python_version=python_version,
            script=script,
        )
    if gitignore:
        add_gitignore(modifications=modifications)
    if pyproject:
        add_pyproject_toml(
            modifications=modifications,
            python_version=python_version,
            description=description,
            package_name=package_name,
            readme=readme,
            optional_dependencies__scripts=pyproject__project__optional_dependencies__scripts,
            python_package_name=python_package_name,
            uv__indexes=uv__indexes,
        )
    if pyright:
        add_pyrightconfig_json(
            modifications=modifications, python_version=python_version, script=script
        )
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
    if ruff:
        add_ruff_toml(modifications=modifications, python_version=python_version)
    if run_version_bump:
        run_bump_my_version(modifications=modifications)
    if len(modifications) >= 1:
        LOGGER.info(
            "Exiting due to %s: %s",
            counted_noun(modifications, "modification"),
            ", ".join(map(repr_str, sorted(modifications))),
        )
        sys.exit(1)
    LOGGER.info("Finished running %r", get_func_name(conformalize_repo))


##


def add_bumpversion_toml(
    *,
    modifications: MutableSet[Path] | None = None,
    pyproject: bool = SETTINGS.pyproject,
    package_name: str | None = SETTINGS.package_name,
    python_package_name: str | None = SETTINGS.python_package_name,
) -> None:
    with yield_bumpversion_toml(modifications=modifications) as doc:
        tool = get_set_table(doc, "tool")
        bumpversion = get_set_table(tool, "bumpversion")
        if pyproject:
            files = get_set_aot(bumpversion, "files")
            ensure_contains(
                files,
                _add_bumpversion_toml_file(PYPROJECT_TOML, 'version = "${version}"'),
            )
    if (
        python_package_name_use := get_python_package_name(
            package_name=package_name, python_package_name=python_package_name
        )
    ) is not None:
        files = get_set_aot(bumpversion, "files")
        ensure_contains(
            files,
            _add_bumpversion_toml_file(
                f"src/{python_package_name_use}/__init__.py",
                '__version__ = "${version}"',
            ),
        )


def _add_bumpversion_toml_file(path: PathLike, template: str, /) -> Table:
    tab = table()
    tab["filename"] = str(path)
    tab["search"] = Template(template).substitute(version="{current_version}")
    tab["replace"] = Template(template).substitute(version="{new_version}")
    return tab


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


def add_envrc(
    *,
    modifications: MutableSet[Path] | None = None,
    uv: bool = SETTINGS.envrc__uv,
    uv__native_tls: bool = SETTINGS.uv__native_tls,
    python_version: str = SETTINGS.python_version,
    script: str | None = SETTINGS.script,
) -> None:
    with yield_text_file(ENVRC, modifications=modifications) as context:
        shebang = strip_and_dedent("""
            #!/usr/bin/env sh
            # shellcheck source=/dev/null
        """)
        if search(escape(shebang), context.output, flags=MULTILINE) is None:
            context.output += f"\n\n{shebang}"

        echo = strip_and_dedent("""
            # echo
            echo_date() { echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >&2; }
        """)
        if search(escape(echo), context.output, flags=MULTILINE) is None:
            context.output += f"\n\n{echo}"

        if uv:
            uv_text = _add_envrc_uv_text(
                native_tls=uv__native_tls, python_version=python_version, script=script
            )
            if search(escape(uv_text), context.output, flags=MULTILINE) is None:
                context.output += f"\n\n{uv_text}"


def _add_envrc_uv_text(
    *,
    native_tls: bool = SETTINGS.uv__native_tls,
    python_version: str = SETTINGS.python_version,
    script: str | None = SETTINGS.script,
) -> str:
    lines: list[str] = [
        strip_and_dedent("""
            # uv
            export UV_MANAGED_PYTHON='true'
        """)
    ]
    if native_tls:
        lines.append("export UV_NATIVE_TLS='true'")
    lines.append(
        strip_and_dedent(f"""
            export UV_PRERELEASE='disallow'
            export UV_PYTHON='{python_version}'
            export UV_RESOLUTION='highest'
            export UV_VENV_CLEAR=1
            if ! command -v uv >/dev/null 2>&1; then
            \techo_date "ERROR: 'uv' not found" && exit 1
            fi
            activate='.venv/bin/activate'
            if [ -f $activate ]; then
            \t. $activate
            else
            \tuv venv
            fi
        """)
    )
    args: list[str] = ["uv", "sync"]
    if script is None:
        args.extend(["--all-extras", "--all-groups"])
    args.extend(["--active", "--locked"])
    if script is not None:
        args.extend(["--script", script])
    lines.append(join(args))
    return "\n".join(lines)


##


def add_gitignore(*, modifications: MutableSet[Path] | None = None) -> None:
    with yield_text_file(GITIGNORE, modifications=modifications) as context:
        text = (PATH_CONFIGS / "gitignore").read_text()
        if search(escape(text), context.output, flags=MULTILINE) is None:
            context.output += f"\n\n{text}"


##


def add_pre_commit_config_yaml(
    *,
    modifications: MutableSet[Path] | None = None,
    dockerfmt: bool = SETTINGS.pre_commit__dockerfmt,
    prettier: bool = SETTINGS.pre_commit__prettier,
    python: bool = SETTINGS.pre_commit__python,
    ruff: bool = SETTINGS.pre_commit__ruff,
    shell: bool = SETTINGS.pre_commit__shell,
    taplo: bool = SETTINGS.pre_commit__taplo,
    uv: bool = SETTINGS.pre_commit__uv,
    script: str | None = SETTINGS.script,
    uv__indexes: list[tuple[str, str]] = SETTINGS.uv__indexes,
    uv__native_tls: bool = SETTINGS.uv__native_tls,
) -> None:
    with yield_yaml_dict(PRE_COMMIT_CONFIG_YAML, modifications=modifications) as dict_:
        _add_pre_commit_config_repo(dict_, ACTIONS_URL, CONFORMALIZE_REPO_SUB_CMD)
        _add_pre_commit_config_repo(
            dict_, PRE_COMMIT_HOOKS_URL, "check-executables-have-shebangs"
        )
        _add_pre_commit_config_repo(dict_, PRE_COMMIT_HOOKS_URL, "check-merge-conflict")
        _add_pre_commit_config_repo(dict_, PRE_COMMIT_HOOKS_URL, "check-symlinks")
        _add_pre_commit_config_repo(dict_, PRE_COMMIT_HOOKS_URL, "destroyed-symlinks")
        _add_pre_commit_config_repo(dict_, PRE_COMMIT_HOOKS_URL, "detect-private-key")
        _add_pre_commit_config_repo(dict_, PRE_COMMIT_HOOKS_URL, "end-of-file-fixer")
        _add_pre_commit_config_repo(
            dict_, PRE_COMMIT_HOOKS_URL, "mixed-line-ending", args=("add", ["--fix=lf"])
        )
        _add_pre_commit_config_repo(dict_, PRE_COMMIT_HOOKS_URL, "no-commit-to-branch")
        _add_pre_commit_config_repo(
            dict_,
            PRE_COMMIT_HOOKS_URL,
            "pretty-format-json",
            args=("add", ["--autofix"]),
        )
        _add_pre_commit_config_repo(dict_, PRE_COMMIT_HOOKS_URL, "no-commit-to-branch")
        _add_pre_commit_config_repo(dict_, PRE_COMMIT_HOOKS_URL, "trailing-whitespace")
        if dockerfmt:
            _add_pre_commit_config_repo(
                dict_,
                DOCKERFMT_URL,
                "dockerfmt",
                args=("add", ["--newline", "--write"]),
            )
        if prettier:
            _add_pre_commit_config_repo(
                dict_,
                "local",
                "prettier",
                name="prettier",
                entry="npx prettier --write",
                language="system",
                types_or=["markdown", "yaml"],
            )
        if python:
            _add_pre_commit_config_repo(dict_, ACTIONS_URL, FORMAT_REQUIREMENTS_SUB_CMD)
            _add_pre_commit_config_repo(
                dict_, ACTIONS_URL, REPLACE_SEQUENCE_STRS_SUB_CMD
            )
            _add_pre_commit_config_repo(dict_, ACTIONS_URL, TOUCH_EMPTY_PY_SUB_CMD)
            _add_pre_commit_config_repo(dict_, ACTIONS_URL, TOUCH_PY_TYPED_SUB_CMD)
            args: list[str] = []
            if len(uv__indexes) >= 1:
                args.extend(["--index", ",".join(v for _, v in uv__indexes)])
            if uv__native_tls:
                args.append("--native-tls")
            _add_pre_commit_config_repo(
                dict_,
                ACTIONS_URL,
                UPDATE_REQUIREMENTS_SUB_CMD,
                args=("add", args) if len(args) >= 1 else None,
            )
        if ruff:
            _add_pre_commit_config_repo(
                dict_, RUFF_URL, "ruff-check", args=("add", ["--fix"])
            )
            _add_pre_commit_config_repo(dict_, RUFF_URL, "ruff-format")
        if shell:
            _add_pre_commit_config_repo(dict_, SHFMT_URL, "shfmt")
            _add_pre_commit_config_repo(dict_, SHELLCHECK_URL, "shellcheck")
        if taplo:
            _add_pre_commit_config_repo(
                dict_,
                TAPLO_URL,
                "taplo-format",
                args=(
                    "exact",
                    [
                        "--option",
                        "indent_tables=true",
                        "--option",
                        "indent_entries=true",
                        "--option",
                        "reorder_keys=true",
                    ],
                ),
            )
        if uv:
            args: list[str] = [
                "--upgrade",
                "--resolution",
                "highest",
                "--prerelease",
                "disallow",
            ]
            if script is not None:
                args.extend(["--script", script])
            _add_pre_commit_config_repo(
                dict_,
                UV_URL,
                "uv-lock",
                files=None if script is None else rf"^{escape(script)}$",
                args=("add", args),
            )


def _add_pre_commit_config_repo(
    pre_commit_dict: StrDict,
    url: str,
    id_: str,
    /,
    *,
    name: str | None = None,
    entry: str | None = None,
    language: str | None = None,
    files: str | None = None,
    types_or: list[str] | None = None,
    args: tuple[Literal["add", "exact"], list[str]] | None = None,
) -> None:
    repos_list = get_set_list_dicts(pre_commit_dict, "repos")
    repo_dict = ensure_contains_partial_dict(
        repos_list, {"repo": url}, extra={} if url == "local" else {"rev": "master"}
    )
    hooks_list = get_set_list_dicts(repo_dict, "hooks")
    hook_dict = ensure_contains_partial_dict(hooks_list, {"id": id_})
    if name is not None:
        hook_dict["name"] = name
    if entry is not None:
        hook_dict["entry"] = entry
    if language is not None:
        hook_dict["language"] = language
    if files is not None:
        hook_dict["files"] = files
    if types_or is not None:
        hook_dict["types_or"] = types_or
    if args is not None:
        match args:
            case "add", list() as args_i:
                hook_args = get_set_list_strs(hook_dict, "args")
                ensure_contains(hook_args, *args_i)
            case "exact", list() as args_i:
                hook_dict["args"] = args_i
            case never:
                assert_never(never)


##


def add_pyproject_toml(
    *,
    modifications: MutableSet[Path] | None = None,
    python_version: str = SETTINGS.python_version,
    description: str | None = SETTINGS.description,
    package_name: str | None = SETTINGS.package_name,
    readme: bool = SETTINGS.readme,
    optional_dependencies__scripts: bool = SETTINGS.pyproject__project__optional_dependencies__scripts,
    python_package_name: str | None = SETTINGS.python_package_name,
    uv__indexes: list[tuple[str, str]] = SETTINGS.uv__indexes,
) -> None:
    with yield_pyproject_toml(modifications=modifications) as doc:
        build_system = get_set_table(doc, "build-system")
        build_system["build-backend"] = "uv_build"
        build_system["requires"] = ["uv_build"]
        project = get_set_table(doc, "project")
        project["requires-python"] = f">= {python_version}"
        if description is not None:
            project["description"] = description
        if package_name is not None:
            project["name"] = package_name
        if readme:
            project["readme"] = "README.md"
        project.setdefault("version", "0.1.0")
        dependency_groups = get_set_table(doc, "dependency-groups")
        dev = get_set_array(dependency_groups, "dev")
        _ = ensure_contains_partial_str(dev, "dycw-utilities[test]")
        _ = ensure_contains_partial_str(dev, "pyright")
        _ = ensure_contains_partial_str(dev, "rich")
        if optional_dependencies__scripts:
            optional_dependencies = get_set_table(project, "optional-dependencies")
            scripts = get_set_array(optional_dependencies, "scripts")
            _ = ensure_contains_partial_str(scripts, "click")
        if python_package_name is not None:
            uv = get_tool_uv(doc)
            build_backend = get_set_table(uv, "build-backend")
            build_backend["module-name"] = get_python_package_name(
                package_name=package_name, python_package_name=python_package_name
            )
            build_backend["module-root"] = "src"
        if len(uv__indexes) >= 1:
            uv = get_tool_uv(doc)
            indexes = get_set_aot(uv, "index")
            for name, url in uv__indexes:
                index = table()
                index["explicit"] = True
                index["name"] = name
                index["url"] = url
                ensure_contains(indexes, index)


##


def add_pyrightconfig_json(
    *,
    modifications: MutableSet[Path] | None = None,
    python_version: str = SETTINGS.python_version,
    script: str | None = SETTINGS.script,
) -> None:
    with yield_json_dict(PYRIGHTCONFIG_JSON, modifications=modifications) as dict_:
        dict_["deprecateTypingAliases"] = True
        dict_["enableReachabilityAnalysis"] = False
        include = get_set_list_strs(dict_, "include")
        ensure_contains(include, "src" if script is None else script)
        dict_["pythonVersion"] = python_version
        dict_["reportCallInDefaultInitializer"] = True
        dict_["reportImplicitOverride"] = True
        dict_["reportImplicitStringConcatenation"] = True
        dict_["reportImportCycles"] = True
        dict_["reportMissingSuperCall"] = True
        dict_["reportMissingTypeArgument"] = False
        dict_["reportMissingTypeStubs"] = False
        dict_["reportPrivateImportUsage"] = False
        dict_["reportPrivateUsage"] = False
        dict_["reportPropertyTypeMismatch"] = True
        dict_["reportUninitializedInstanceVariable"] = True
        dict_["reportUnknownArgumentType"] = False
        dict_["reportUnknownMemberType"] = False
        dict_["reportUnknownParameterType"] = False
        dict_["reportUnknownVariableType"] = False
        dict_["reportUnnecessaryComparison"] = False
        dict_["reportUnnecessaryTypeIgnoreComment"] = True
        dict_["reportUnusedCallResult"] = True
        dict_["reportUnusedImport"] = False
        dict_["reportUnusedVariable"] = False
        dict_["typeCheckingMode"] = "strict"


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


def add_ruff_toml(
    *,
    modifications: MutableSet[Path] | None = None,
    python_version: str = SETTINGS.python_version,
) -> None:
    with yield_toml_doc(RUFF_TOML, modifications=modifications) as doc:
        doc["target-version"] = f"py{python_version.replace('.', '')}"
        doc["unsafe-fixes"] = True
        fmt = get_set_table(doc, "format")
        fmt["preview"] = True
        fmt["skip-magic-trailing-comma"] = True
        lint = get_set_table(doc, "lint")
        lint["explicit-preview-rules"] = True
        fixable = get_set_array(lint, "fixable")
        ensure_contains(fixable, "ALL")
        ignore = get_set_array(lint, "ignore")
        ensure_contains(
            ignore,
            "ANN401",  # any-type
            "ASYNC109",  # async-function-with-timeout
            "C901",  # complex-structure
            "CPY",  # flake8-copyright
            "D",  # pydocstyle
            "E501",  # line-too-long
            "PD",  # pandas-vet
            "PERF203",  # try-except-in-loop
            "PLC0415",  # import-outside-top-level
            "PLE1205",  # logging-too-many-args
            "PLR0904",  # too-many-public-methods
            "PLR0911",  # too-many-return-statements
            "PLR0912",  # too-many-branches
            "PLR0913",  # too-many-arguments
            "PLR0915",  # too-many-statements
            "PLR2004",  # magic-value-comparison
            "PT012",  # pytest-raises-with-multiple-statements
            "PT013",  # pytest-incorrect-pytest-import
            "PYI041",  # redundant-numeric-union
            "S202",  # tarfile-unsafe-members
            "S310",  # suspicious-url-open-usage
            "S311",  # suspicious-non-cryptographic-random-usage
            "S602",  # subprocess-popen-with-shell-equals-true
            "S603",  # subprocess-without-shell-equals-true
            "S607",  # start-process-with-partial-path
            # preview
            "S101",  # assert
            # formatter
            "W191",  # tab-indentation
            "E111",  # indentation-with-invalid-multiple
            "E114",  # indentation-with-invalid-multiple-comment
            "E117",  # over-indented
            "COM812",  # missing-trailing-comma
            "COM819",  # prohibited-trailing-comma
            "ISC001",  # single-line-implicit-string-concatenation
            "ISC002",  # multi-line-implicit-string-concatenation
        )
        lint["preview"] = True
        select = get_set_array(lint, "select")
        selected_rules = [
            "RUF022",  # unsorted-dunder-all
            "RUF029",  # unused-async
        ]
        ensure_contains(select, "ALL", *selected_rules)
        extend_per_file_ignores = get_set_table(lint, "extend-per-file-ignores")
        test_py = get_set_array(extend_per_file_ignores, "test_*.py")
        test_py_rules = [
            "S101",  # assert
            "SLF001",  # private-member-access
        ]
        ensure_contains(test_py, *test_py_rules)
        ensure_not_contains(ignore, *selected_rules, *test_py_rules)
        bugbear = get_set_table(lint, "flake8-bugbear")
        extend_immutable_calls = get_set_array(bugbear, "extend-immutable-calls")
        ensure_contains(extend_immutable_calls, "typing.cast")
        tidy_imports = get_set_table(lint, "flake8-tidy-imports")
        tidy_imports["ban-relative-imports"] = "all"
        isort = get_set_table(lint, "isort")
        req_imps = get_set_array(isort, "required-imports")
        ensure_contains(req_imps, "from __future__ import annotations")
        isort["split-on-trailing-comma"] = False


##


def check_versions() -> None:
    version = get_version_from_bumpversion_toml()
    try:
        set_version(version)
    except CalledProcessError:
        msg = f"Inconsistent versions; should be {version}"
        raise ValueError(msg) from None


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


def get_version_from_bumpversion_toml(
    *, obj: TOMLDocument | str | None = None
) -> Version:
    match obj:
        case TOMLDocument() as doc:
            tool = get_set_table(doc, "tool")
            bumpversion = get_set_table(tool, "bumpversion")
            return parse_version(str(bumpversion["current_version"]))
        case str() as text:
            return get_version_from_bumpversion_toml(obj=tomlkit.parse(text))
        case None:
            with yield_bumpversion_toml() as doc:
                return get_version_from_bumpversion_toml(obj=doc)
        case never:
            assert_never(never)


def get_version_from_git_show() -> Version:
    text = logged_run("git", "show", f"origin/master:{BUMPVERSION_TOML}", return_=True)
    return get_version_from_bumpversion_toml(obj=text.rstrip("\n"))


def get_version_from_git_tag() -> Version:
    text = logged_run("git", "tag", "--points-at", "origin/master", return_=True)
    for line in text.splitlines():
        with suppress(ParseVersionError):
            return parse_version(line)
    msg = "No valid version from 'git tag'"
    raise ValueError(msg)


##


def run_bump_my_version(*, modifications: MutableSet[Path] | None = None) -> None:
    def run_set_version(version: Version, /) -> None:
        LOGGER.info("Setting version to %s...", version)
        set_version(version)
        if modifications is not None:
            modifications.add(BUMPVERSION_TOML)

    try:
        prev = get_version_from_git_tag()
    except (CalledProcessError, ValueError):
        try:
            prev = get_version_from_git_show()
        except (CalledProcessError, ParseVersionError, NonExistentKey):
            run_set_version(Version(0, 1, 0))
            return
    current = get_version_from_bumpversion_toml()
    patched = prev.bump_patch()
    if current not in {patched, prev.bump_minor(), prev.bump_major()}:
        run_set_version(patched)


##


def _run_pre_commit_update(*, modifications: MutableSet[Path] | None = None) -> None:
    current = PRE_COMMIT_CONFIG_YAML.read_text()
    logged_run("pre-commit", "autoupdate", print=True)
    if (modifications is not None) and (PRE_COMMIT_CONFIG_YAML.read_text() != current):
        modifications.add(PRE_COMMIT_CONFIG_YAML)


run_pre_commit_update = throttle(
    duration=THROTTLE_DURATION, path=path_throttle_cache(_run_pre_commit_update)
)(_run_pre_commit_update)


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


def set_version(version: Version, /) -> None:
    logged_run(
        "bump-my-version",
        "replace",
        "--new-version",
        str(version),
        str(BUMPVERSION_TOML),
    )


##


def update_action_file_extensions(
    *, modifications: MutableSet[Path] | None = None
) -> None:
    try:
        paths = list(Path(".github").rglob("**/*.yml"))
    except FileNotFoundError:
        return
    for path in paths:
        new = path.with_suffix(".yaml")
        LOGGER.info("Renaming '%s' -> '%s'...", path, new)
        _ = path.rename(new)
        if modifications is not None:
            modifications.add(path)


##


def update_action_versions(*, modifications: MutableSet[Path] | None = None) -> None:
    try:
        paths = list(GITHUB.rglob("**/*.yaml"))
    except FileNotFoundError:
        return
    versions = {
        "actions/checkout": "v6",
        "actions/setup-python": "v6",
        "astral-sh/ruff-action": "v3",
        "astral-sh/setup-uv": "v7",
    }
    for path, (action, version) in product(paths, versions.items()):
        text = sub(
            rf"^(\s*- uses: {action})@.+$",
            rf"\1@{version}",
            path.read_text(),
            flags=MULTILINE,
        )
        with yield_yaml_dict(path, modifications=modifications) as dict_:
            dict_.clear()
            dict_.update(YAML_INSTANCE.load(text))


##


@contextmanager
def yield_bumpversion_toml(
    *, modifications: MutableSet[Path] | None = None
) -> Iterator[TOMLDocument]:
    with yield_toml_doc(BUMPVERSION_TOML, modifications=modifications) as doc:
        tool = get_set_table(doc, "tool")
        bumpversion = get_set_table(tool, "bumpversion")
        bumpversion["allow_dirty"] = True
        bumpversion.setdefault("current_version", str(Version(0, 1, 0)))
        yield doc


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
    "add_bumpversion_toml",
    "add_ci_pull_request_yaml",
    "add_ci_push_yaml",
    "add_coveragerc_toml",
    "add_envrc",
    "add_gitignore",
    "add_pre_commit_config_yaml",
    "add_pyproject_toml",
    "add_pyrightconfig_json",
    "add_pytest_toml",
    "add_readme_md",
    "add_ruff_toml",
    "check_versions",
    "get_cron_job",
    "get_python_package_name",
    "get_tool_uv",
    "get_version_from_bumpversion_toml",
    "get_version_from_git_show",
    "get_version_from_git_tag",
    "run_bump_my_version",
    "run_pre_commit_update",
    "run_ripgrep_and_replace",
    "set_version",
    "update_action_file_extensions",
    "update_action_versions",
    "yield_bumpversion_toml",
    "yield_python_versions",
]
