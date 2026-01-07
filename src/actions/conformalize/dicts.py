from __future__ import annotations

from typing import TYPE_CHECKING, Any

import actions.publish_package.doc
import actions.random_sleep.doc
import actions.run_hooks.doc
import actions.tag_commit.doc
from actions.conformalize.defaults import GITHUB_TOKEN, PRERELEASE, RESOLUTION

if TYPE_CHECKING:
    from actions.types import StrDict


def run_action_pre_commit_dict(
    *,
    token: str = GITHUB_TOKEN,
    submodules: str | None = None,
    repos: Any | None = None,
    hooks: Any | None = None,
    sleep: int = 1,
) -> StrDict:
    dict_: StrDict = {"token": token}
    _add_item(dict_, "submodules", value=submodules)
    _add_item(dict_, "repos", value=repos)
    _add_item(dict_, "hooks", value=hooks)
    dict_["sleep"] = sleep
    return {
        "name": actions.run_hooks.doc.DOCSTRING,
        "uses": "dycw/action-run-hooks@latest",
        "with": dict_,
    }


def run_action_publish_dict(
    *,
    token: str = GITHUB_TOKEN,
    username: str | None = None,
    password: str | None = None,
    publish_url: str | None = None,
    trusted_publishing: bool = False,
    native_tls: bool = False,
) -> StrDict:
    dict_: StrDict = {"token": token}
    _add_item(dict_, "username", value=username)
    _add_item(dict_, "password", value=password)
    _add_item(dict_, "publish-url", value=publish_url)
    _add_boolean(dict_, "trusted-publishing", value=trusted_publishing)
    _add_native_tls(dict_, native_tls=native_tls)
    return {
        "name": actions.publish_package.doc.DOCSTRING,
        "uses": "dycw/action-publish-package@latest",
        "with": dict_,
    }


def run_action_pyright_dict(
    *,
    token_checkout: str = GITHUB_TOKEN,
    token_uv: str = GITHUB_TOKEN,
    python_version: str | None = None,
    resolution: str = RESOLUTION,
    prerelease: str = PRERELEASE,
    native_tls: bool = False,
    with_requirements: str | None = None,
) -> StrDict:
    dict_: StrDict = {"token-checkout": token_checkout, "token-uv": token_uv}
    _add_python_version(dict_, python_version=python_version)
    dict_["resolution"] = resolution
    dict_["prerelease"] = prerelease
    _add_native_tls(dict_, native_tls=native_tls)
    _add_with_requirements(dict_, with_requirements=with_requirements)
    return {
        "name": "Run 'pyright'",
        "uses": "dycw/action-pyright@latest",
        "with": dict_,
    }


def run_action_pytest_dict(
    *,
    token_checkout: str = GITHUB_TOKEN,
    token_uv: str = GITHUB_TOKEN,
    python_version: str | None = None,
    sops_age_key: str | None = None,
    token_sops: str = GITHUB_TOKEN,
    token_age: str = GITHUB_TOKEN,
    resolution: str = RESOLUTION,
    prerelease: str = PRERELEASE,
    native_tls: bool = False,
    with_requirements: str | None = None,
) -> StrDict:
    dict_: StrDict = {"token-checkout": token_checkout, "token-uv": token_uv}
    _add_python_version(dict_, python_version=python_version)
    _add_item(dict_, "sops-age-key", value=sops_age_key)
    dict_["token-sops"] = token_sops
    dict_["token-age"] = token_age
    dict_["resolution"] = resolution
    dict_["prerelease"] = prerelease
    _add_native_tls(dict_, native_tls=native_tls)
    _add_with_requirements(dict_, with_requirements=with_requirements)
    return {"name": "Run 'pytest'", "uses": "dycw/action-pytest@latest", "with": dict_}


def run_action_random_sleep_dict(
    *,
    token_checkout: str = GITHUB_TOKEN,
    token_uv: str = GITHUB_TOKEN,
    min: int = 0,  # noqa: A002
    max: int = 3600,  # noqa: A002
    step: int = 1,
    log_freq: int = 1,
) -> StrDict:
    dict_: StrDict = {
        "token-checkout": token_checkout,
        "token-uv": token_uv,
        "min": min,
        "max": max,
        "step": step,
        "log-freq": log_freq,
    }
    return {
        "name": actions.random_sleep.doc.DOCSTRING,
        "uses": "dycw/action-random-sleep@latest",
        "with": dict_,
    }


def run_action_ruff_dict(
    *, token_checkout: str = GITHUB_TOKEN, token_ruff: str = GITHUB_TOKEN
) -> StrDict:
    dict_: StrDict = {"token-checkout": token_checkout, "token-ruff": token_ruff}
    return {"name": "Run 'ruff'", "uses": "dycw/action-ruff@latest", "with": dict_}


def run_action_tag_dict(
    *,
    token_checkout: str = GITHUB_TOKEN,
    token_uv: str = GITHUB_TOKEN,
    user_name: str = "github-actions-bot",
    user_email: str = "noreply@github.com",
    major_minor: bool = False,
    major: bool = False,
    latest: bool = False,
) -> StrDict:
    dict_: StrDict = {
        "token-checkout": token_checkout,
        "token-uv": token_uv,
        "user-name": user_name,
        "user-email": user_email,
    }
    _add_boolean(dict_, "major-minor", value=major_minor)
    _add_boolean(dict_, "major", value=major)
    _add_boolean(dict_, "latest", value=latest)
    return {
        "name": actions.tag_commit.doc.DOCSTRING,
        "uses": "dycw/action-tag-commit@latest",
        "with": dict_,
    }


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


def _add_with_requirements(
    dict_: StrDict, /, *, with_requirements: str | None = None
) -> None:
    _add_item(dict_, "with-requirements", value=with_requirements)


__all__ = [
    "run_action_pre_commit_dict",
    "run_action_publish_dict",
    "run_action_pyright_dict",
    "run_action_pytest_dict",
    "run_action_random_sleep_dict",
    "run_action_ruff_dict",
    "run_action_tag_dict",
]
