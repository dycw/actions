from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING, Any, Literal, overload

from utilities.core import to_logger
from utilities.pydantic import extract_secret
from utilities.subprocess import run

from actions.constants import YAML_INSTANCE
from actions.logging import LOGGER

if TYPE_CHECKING:
    from utilities.types import SecretLike, StrStrMapping


_LOGGER = to_logger(__name__)


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
    _LOGGER.info("Running '%s'...", " ".join(map(str, cmds_and_args)))
    unwrapped: list[str] = list(map(extract_secret, cmds_and_args))
    return run(*unwrapped, env=env, print=print, return_=return_, logger=LOGGER)


##


def yaml_dump(obj: Any, /) -> str:
    stream = StringIO()
    YAML_INSTANCE.dump(obj, stream)
    return stream.getvalue()


##


__all__ = ["logged_run", "yaml_dump"]
