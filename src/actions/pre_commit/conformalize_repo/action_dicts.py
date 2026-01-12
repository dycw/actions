from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ruamel.yaml.scalarstring import LiteralScalarString
from typed_settings import Secret

from actions.pre_commit.conformalize_repo.settings import SETTINGS
from actions.publish_package.constants import PUBLISH_PACKAGE_DOCSTRING
from actions.run_hooks.constants import RUN_HOOKS_DOCSTRING
from actions.tag_commit.constants import TAG_COMMIT_DOCSTRING

if TYPE_CHECKING:
    from utilities.types import StrDict


def action_publish_package_dict(
    *,
    token_checkout: Secret[str] | None = SETTINGS.ci__token_checkout,
    token_github: Secret[str] | None = SETTINGS.ci__token_github,
    username: str | None = SETTINGS.ci__push__publish__primary__username,
    password: Secret[str] | None = SETTINGS.ci__push__publish__primary__password,
    publish_url: Secret[str] | None = SETTINGS.ci__push__publish__primary__publish_url,
    trusted_publishing: bool = False,
    native_tls: bool = SETTINGS.uv__native_tls,
) -> StrDict:
    out: StrDict = {
        "name": PUBLISH_PACKAGE_DOCSTRING,
        "uses": "dycw/action-publish-package@latest",
    }
    with_: StrDict = {}
    _add_token_checkout(with_, token=token_checkout)
    _add_token_github(with_, token=token_github)
    _add_item(with_, "username", value=username)
    _add_item(with_, "password", value=password)
    _add_item(with_, "publish-url", value=publish_url)
    _add_boolean(with_, "trusted-publishing", value=trusted_publishing)
    _add_native_tls(with_, native_tls=native_tls)
    _add_with_dict(out, with_)
    return out


def action_pyright_dict(
    *,
    token_checkout: Secret[str] | None = SETTINGS.ci__token_checkout,
    token_github: Secret[str] | None = SETTINGS.ci__token_github,
    python_version: str | None = None,
    resolution: str | None = None,
    prerelease: str | None = None,
    native_tls: bool = SETTINGS.uv__native_tls,
    with_requirements: str | None = None,
) -> StrDict:
    out: StrDict = {"name": "Run 'pyright'", "uses": "dycw/action-pyright@latest"}
    with_: StrDict = {}
    _add_token_checkout(with_, token=token_checkout)
    _add_token_github(with_, token=token_github)
    _add_python_version(with_, python_version=python_version)
    _add_resolution(with_, resolution=resolution)
    _add_prerelease(with_, prerelease=prerelease)
    _add_native_tls(with_, native_tls=native_tls)
    _add_with_requirements(with_, with_requirements=with_requirements)
    _add_with_dict(out, with_)
    return out


def action_pytest_dict(
    *,
    token_checkout: Secret[str] | None = SETTINGS.ci__token_checkout,
    token_github: Secret[str] | None = SETTINGS.ci__token_github,
    python_version: str | None = None,
    sops_age_key: Secret[str] | None = None,
    resolution: str | None = None,
    prerelease: str | None = None,
    native_tls: bool = SETTINGS.uv__native_tls,
    with_requirements: str | None = None,
) -> StrDict:
    out: StrDict = {"name": "Run 'pytest'", "uses": "dycw/action-pytest@latest"}
    with_: StrDict = {}
    _add_token_checkout(with_, token=token_checkout)
    _add_token_github(with_, token=token_github)
    _add_python_version(with_, python_version=python_version)
    _add_item(with_, "sops-age-key", value=sops_age_key)
    _add_resolution(with_, resolution=resolution)
    _add_prerelease(with_, prerelease=prerelease)
    _add_native_tls(with_, native_tls=native_tls)
    _add_with_requirements(with_, with_requirements=with_requirements)
    _add_with_dict(out, with_)
    return out


def action_ruff_dict(
    *,
    token_checkout: Secret[str] | None = SETTINGS.ci__token_checkout,
    token_github: Secret[str] | None = SETTINGS.ci__token_github,
) -> StrDict:
    out: StrDict = {"name": "Run 'ruff'", "uses": "dycw/action-ruff@latest"}
    with_: StrDict = {}
    _add_token_checkout(with_, token=token_checkout)
    _add_token_github(with_, token=token_github)
    _add_with_dict(out, with_)
    return out


def action_run_hooks_dict(
    *,
    token_checkout: Secret[str] | None = SETTINGS.ci__token_checkout,
    token_github: Secret[str] | None = SETTINGS.ci__token_github,
    submodules: str | None = SETTINGS.ci__pull_request__pre_commit__submodules,
    repos: list[str] | None = None,
    hooks: list[str] | None = None,
    hooks_exclude: list[str] | None = None,
    sleep: int | None = None,
    gitea: bool = SETTINGS.ci__gitea,
) -> StrDict:
    out: StrDict = {
        "if": f"{_runner(gitea=gitea)}.event_name == 'pull_request'",
        "name": RUN_HOOKS_DOCSTRING,
        "uses": "dycw/action-run-hooks@latest",
    }
    with_: StrDict = {}
    _add_token_checkout(with_, token=token_checkout)
    _add_token_github(with_, token=token_github)
    _add_item(with_, "submodules", value=submodules)
    _add_yaml_str(with_, "repos", values=repos)
    _add_yaml_str(with_, "hooks", values=hooks)
    _add_yaml_str(with_, "hooks-exclude", values=hooks_exclude)
    _add_item(with_, "hooks", value=hooks)
    _add_item(with_, "sleep", value=sleep)
    _add_with_dict(out, with_)
    return out


def action_tag_commit_dict(
    *,
    token_checkout: Secret[str] | None = SETTINGS.ci__token_checkout,
    token_github: Secret[str] | None = SETTINGS.ci__token_github,
    user_name: str | None = None,
    user_email: str | None = None,
    major_minor: bool = False,
    major: bool = False,
    latest: bool = False,
) -> StrDict:
    out: StrDict = {
        "name": TAG_COMMIT_DOCSTRING,
        "uses": "dycw/action-tag-commit@latest",
    }
    with_: StrDict = {}
    _add_token_checkout(with_, token=token_checkout)
    _add_token_github(with_, token=token_github)
    _add_item(with_, "user-name", value=user_name)
    _add_item(with_, "user-email", value=user_email)
    _add_boolean(with_, "major-minor", value=major_minor)
    _add_boolean(with_, "major", value=major)
    _add_boolean(with_, "latest", value=latest)
    _add_with_dict(out, with_)
    return out


def update_ca_certificates_dict(desc: str, /) -> StrDict:
    return {
        "name": f"Update CA certificates ({desc})",
        "run": "sudo update-ca-certificates",
    }


##


def _add_boolean(dict_: StrDict, key: str, /, *, value: bool = False) -> None:
    if value:
        dict_[key] = value


def _add_item(dict_: StrDict, key: str, /, *, value: Any | None = None) -> None:
    match value:
        case None:
            ...
        case Secret():
            _add_item(dict_, key, value=value.get_secret_value())
        case _:
            dict_[key] = value


def _add_native_tls(
    dict_: StrDict, /, *, native_tls: bool = SETTINGS.uv__native_tls
) -> None:
    _add_boolean(dict_, "native-tls", value=native_tls)


def _add_python_version(
    dict_: StrDict, /, *, python_version: str | None = None
) -> None:
    _add_item(dict_, "python-version", value=python_version)


def _add_prerelease(dict_: StrDict, /, *, prerelease: str | None = None) -> None:
    _add_item(dict_, "prerelease", value=prerelease)


def _add_resolution(dict_: StrDict, /, *, resolution: str | None = None) -> None:
    _add_item(dict_, "resolution", value=resolution)


def _add_token_checkout(
    dict_: StrDict, /, *, token: Secret[str] | None = SETTINGS.ci__token_checkout
) -> None:
    _add_item(dict_, "token-checkout", value=token)


def _add_token_github(
    dict_: StrDict, /, *, token: Secret[str] | None = SETTINGS.ci__token_github
) -> None:
    _add_item(dict_, "token-github", value=token)


def _add_with_dict(dict_: StrDict, with_: StrDict, /) -> None:
    if len(with_) >= 1:
        dict_["with"] = with_


def _add_with_requirements(
    dict_: StrDict, /, *, with_requirements: str | None = None
) -> None:
    _add_item(dict_, "with-requirements", value=with_requirements)


def _add_yaml_str(
    dict_: StrDict, key: str, /, *, values: list[str] | None = None
) -> None:
    if values is not None:
        dict_[key] = LiteralScalarString("\n".join(values))


def _runner(*, gitea: bool = False) -> str:
    return "gitea" if gitea else "github"


__all__ = [
    "action_publish_package_dict",
    "action_pyright_dict",
    "action_pytest_dict",
    "action_ruff_dict",
    "action_run_hooks_dict",
    "action_tag_commit_dict",
    "update_ca_certificates_dict",
]
