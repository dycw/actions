from __future__ import annotations

from typing import TYPE_CHECKING

from actions.conformalize.defaults import GITHUB_TOKEN, PRERELEASE, RESOLUTION

if TYPE_CHECKING:
    from actions.types import StrDict


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


def _add_item(dict_: StrDict, key: str, /, *, value: str | None = None) -> None:
    if value is not None:
        dict_[key] = value


def _add_native_tls(dict_: StrDict, /, *, native_tls: bool = False) -> None:
    if native_tls:
        dict_["native-tls"] = native_tls


def _add_python_version(
    dict_: StrDict, /, *, python_version: str | None = None
) -> None:
    _add_item(dict_, "python-version", value=python_version)


def _add_with_requirements(
    dict_: StrDict, /, *, with_requirements: str | None = None
) -> None:
    _add_item(dict_, "with-requirements", value=with_requirements)


__all__ = ["run_action_pyright_dict"]
