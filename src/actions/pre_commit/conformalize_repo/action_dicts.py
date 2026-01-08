from __future__ import annotations

from typing import TYPE_CHECKING, Any

from actions.publish_package.constants import PUBLISH_PACKAGE_DOCSTRING
from actions.random_sleep.constants import RANDOM_SLEEP_DOCSTRING
from actions.run_hooks.constants import RUN_HOOKS_DOCSTRING
from actions.tag_commit.constants import TAG_COMMIT_DOCSTRING

if TYPE_CHECKING:
    from actions.types import StrDict


def run_action_pre_commit_dict(
    *,
    token: str | None = None,
    submodules: str | None = None,
    repos: Any | None = None,
    hooks: Any | None = None,
    sleep: int = 1,
    gitea: bool = False,
) -> StrDict:
    dict_: StrDict = {}
    _add_token(dict_, token=token)
    _add_item(dict_, "submodules", value=submodules)
    _add_item(dict_, "repos", value=repos)
    _add_item(dict_, "hooks", value=hooks)
    dict_["sleep"] = sleep
    return {
        "if": f"{_runner(gitea=gitea)}.event_name == 'pull_request'",
        "name": RUN_HOOKS_DOCSTRING,
        "uses": "dycw/action-run-hooks@latest",
        "with": dict_,
    }


def run_action_publish_dict(
    *,
    token: str | None = None,
    username: str | None = None,
    password: str | None = None,
    publish_url: str | None = None,
    trusted_publishing: bool = False,
    native_tls: bool = False,
) -> StrDict:
    dict_: StrDict = {}
    _add_token(dict_, token=token)
    _add_item(dict_, "username", value=username)
    _add_item(dict_, "password", value=password)
    _add_item(dict_, "publish-url", value=publish_url)
    _add_boolean(dict_, "trusted-publishing", value=trusted_publishing)
    _add_native_tls(dict_, native_tls=native_tls)
    return {
        "name": PUBLISH_PACKAGE_DOCSTRING,
        "uses": "dycw/action-publish-package@latest",
        "with": dict_,
    }


def run_action_pyright_dict(
    *,
    token: str | None = None,
    python_version: str | None = None,
    resolution: str | None = None,
    prerelease: str | None = None,
    native_tls: bool = False,
    with_requirements: str | None = None,
) -> StrDict:
    dict_: StrDict = {}
    _add_token(dict_, token=token)
    _add_python_version(dict_, python_version=python_version)
    _add_resolution(dict_, resolution=resolution)
    _add_prerelease(dict_, prerelease=prerelease)
    _add_native_tls(dict_, native_tls=native_tls)
    _add_with_requirements(dict_, with_requirements=with_requirements)
    return {
        "name": "Run 'pyright'",
        "uses": "dycw/action-pyright@latest",
        "with": dict_,
    }


def run_action_pytest_dict(
    *,
    token: str | None = None,
    python_version: str | None = None,
    sops_age_key: str | None = None,
    resolution: str | None = None,
    prerelease: str | None = None,
    native_tls: bool = False,
    with_requirements: str | None = None,
) -> StrDict:
    dict_: StrDict = {}
    _add_token(dict_, token=token)
    _add_python_version(dict_, python_version=python_version)
    _add_item(dict_, "sops-age-key", value=sops_age_key)
    _add_resolution(dict_, resolution=resolution)
    _add_prerelease(dict_, prerelease=prerelease)
    _add_native_tls(dict_, native_tls=native_tls)
    _add_with_requirements(dict_, with_requirements=with_requirements)
    return {"name": "Run 'pytest'", "uses": "dycw/action-pytest@latest", "with": dict_}


def run_action_random_sleep_dict(
    *,
    token: str | None = None,
    min: int = 0,  # noqa: A002
    max: int = 3600,  # noqa: A002
    step: int = 1,
    log_freq: int = 1,
) -> StrDict:
    dict_: StrDict = {}
    _add_token(dict_, token=token)
    dict_["min"] = min
    dict_["max"] = max
    dict_["step"] = step
    dict_["log-freq"] = log_freq
    return {
        "name": RANDOM_SLEEP_DOCSTRING,
        "uses": "dycw/action-random-sleep@latest",
        "with": dict_,
    }


def run_action_ruff_dict(*, token: str | None = None) -> StrDict:
    dict_: StrDict = {}
    _add_token(dict_, token=token)
    return {"name": "Run 'ruff'", "uses": "dycw/action-ruff@latest", "with": dict_}


def run_action_tag_dict(
    *,
    token: str | None = None,
    user_name: str | None = None,
    user_email: str | None = None,
    major_minor: bool = False,
    major: bool = False,
    latest: bool = False,
) -> StrDict:
    dict_: StrDict = {}
    _add_token(dict_, token=token)
    _add_item(dict_, "user-name", value=user_name)
    _add_item(dict_, "user-email", value=user_email)
    _add_boolean(dict_, "major-minor", value=major_minor)
    _add_boolean(dict_, "major", value=major)
    _add_boolean(dict_, "latest", value=latest)
    return {
        "name": TAG_COMMIT_DOCSTRING,
        "uses": "dycw/action-tag-commit@latest",
        "with": dict_,
    }


##


def _add_boolean(dict_: StrDict, key: str, /, *, value: bool = False) -> None:
    if value:
        dict_[key] = value


def _add_item(dict_: StrDict, key: str, /, *, value: Any | None = None) -> None:
    if value is not None:
        dict_[key] = value


def _add_native_tls(dict_: StrDict, /, *, native_tls: bool = False) -> None:
    _add_boolean(dict_, "native-tls", value=native_tls)


def _add_python_version(
    dict_: StrDict, /, *, python_version: str | None = None
) -> None:
    _add_item(dict_, "python-version", value=python_version)


def _add_prerelease(dict_: StrDict, /, *, prerelease: str | None = None) -> None:
    _add_item(dict_, "prerelease", value=prerelease)


def _add_resolution(dict_: StrDict, /, *, resolution: str | None = None) -> None:
    _add_item(dict_, "resolution", value=resolution)


def _add_token(dict_: StrDict, /, *, token: str | None = None) -> None:
    _add_item(dict_, "token", value=token)


def _add_with_requirements(
    dict_: StrDict, /, *, with_requirements: str | None = None
) -> None:
    _add_item(dict_, "with-requirements", value=with_requirements)


def _runner(*, gitea: bool = False) -> str:
    return "gitea" if gitea else "github"


__all__ = [
    "run_action_pre_commit_dict",
    "run_action_publish_dict",
    "run_action_pyright_dict",
    "run_action_pytest_dict",
    "run_action_random_sleep_dict",
    "run_action_ruff_dict",
    "run_action_tag_dict",
]
