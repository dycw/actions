from __future__ import annotations

from typing import TYPE_CHECKING, Literal, assert_never, overload

from typed_settings import EnvLoader, Secret
from utilities.subprocess import run

from actions.logging import LOGGER

if TYPE_CHECKING:
    from libcst import Module
    from utilities.types import StrStrMapping

    from actions.types import SecretLike


LOADER = EnvLoader("")


def are_modules_equal(left: Module, right: Module, /) -> bool:
    return left.code.rstrip("\n") == right.code.rstrip("\n")


def convert_list_strs(
    x: str | list[str] | tuple[str, ...] | None, /
) -> list[str] | None:
    match x:
        case None:
            return None
        case list():
            return x
        case tuple():
            return None if x == () else list(x)
        case str():
            return x.splitlines()
        case never:
            assert_never(never)


def convert_secret_str(x: SecretLike | None, /) -> Secret[str] | None:
    match x:
        case Secret():
            match x.get_secret_value():
                case None:
                    return None
                case str() as inner:
                    return None if inner == "" else Secret(inner)
                case never:
                    assert_never(never)
        case str():
            return None if x == "" else Secret(x)
        case None:
            return None
        case never:
            assert_never(never)


def convert_str(x: str | None, /) -> str | None:
    match x:
        case str():
            return None if x == "" else x
        case None:
            return None
        case never:
            assert_never(never)


@overload
def logged_run(
    cmd: SecretLike,
    /,
    *cmds_or_args: SecretLike,
    env: StrStrMapping | None = None,
    print: bool = False,
    return_: Literal[True],
) -> str: ...
@overload
def logged_run(
    cmd: SecretLike,
    /,
    *cmds_or_args: SecretLike,
    env: StrStrMapping | None = None,
    print: bool = False,
    return_: Literal[False] = False,
) -> None: ...
@overload
def logged_run(
    cmd: SecretLike,
    /,
    *cmds_or_args: SecretLike,
    env: StrStrMapping | None = None,
    print: bool = False,
    return_: bool = False,
) -> str | None: ...
def logged_run(
    cmd: SecretLike,
    /,
    *cmds_or_args: SecretLike,
    env: StrStrMapping | None = None,
    print: bool = False,  # noqa: A002
    return_: bool = False,
) -> str | None:
    cmds_and_args = [cmd, *cmds_or_args]
    LOGGER.info("Running '%s'...", " ".join(map(str, cmds_and_args)))
    unwrapped: list[str] = []
    for ca in cmds_and_args:
        match ca:
            case Secret():
                unwrapped.append(ca.get_secret_value())
            case str():
                unwrapped.append(ca)
            case never:
                assert_never(never)
    return run(*unwrapped, env=env, print=print, return_=return_, logger=LOGGER)


__all__ = [
    "LOADER",
    "are_modules_equal",
    "convert_list_strs",
    "convert_secret_str",
    "convert_str",
    "logged_run",
]
