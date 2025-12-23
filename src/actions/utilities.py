from __future__ import annotations

from typing import TYPE_CHECKING, Literal, assert_never, overload

from typed_settings import EnvLoader, Secret
from utilities.subprocess import run

from actions.logging import LOGGER

if TYPE_CHECKING:
    from actions.types import SecretLike


LOADER = EnvLoader("")


def empty_str_to_none(value: SecretLike, /) -> Secret[str] | None:
    match value:
        case Secret():
            return value
        case str():
            return None if value == "" else Secret(value)
        case None:
            return None
        case never:
            assert_never(never)


@overload
def log_run(
    cmd: SecretLike, /, *cmds: SecretLike, print: bool = False, return_: Literal[True]
) -> str: ...
@overload
def log_run(
    cmd: SecretLike,
    /,
    *cmds: SecretLike,
    print: bool = False,
    return_: Literal[False] = False,
) -> None: ...
@overload
def log_run(
    cmd: SecretLike, /, *cmds: SecretLike, print: bool = False, return_: bool = False
) -> str | None: ...
def log_run(
    cmd: SecretLike,
    /,
    *cmds: SecretLike,
    print: bool = False,  # noqa: A002
    return_: bool = False,
) -> str | None:
    all_cmds = [cmd, *cmds]
    LOGGER.info("Running '%s'...", " ".join(map(str, all_cmds)))
    unwrapped = [c if isinstance(c, str) else c.get_secret_value() for c in all_cmds]
    return run(*unwrapped, print=print, return_=return_)


__all__ = ["LOADER", "empty_str_to_none", "log_run"]
