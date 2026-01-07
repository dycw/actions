from __future__ import annotations

from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, Any, Literal, assert_never, overload

from typed_settings import EnvLoader, Secret
from utilities.atomicwrites import writer
from utilities.subprocess import run

from actions.constants import YAML_INSTANCE
from actions.logging import LOGGER

if TYPE_CHECKING:
    from collections.abc import MutableSet

    from libcst import Module
    from tomlkit import TOMLDocument
    from utilities.types import PathLike, StrStrMapping

    from actions.types import SecretLike


LOADER = EnvLoader("")


def are_docs_unequal(left: TOMLDocument, right: TOMLDocument, /) -> bool:
    return not (left == right)  # noqa: SIM201


def are_modules_equal(left: Module, right: Module, /) -> bool:
    return are_texts_equal(left.code, right.code)


def are_texts_equal(left: str, right: str, /) -> bool:
    return ensure_new_line(left) == ensure_new_line(right)


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


def copy_text(
    src: PathLike, dest: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> None:
    LOGGER.info("Copying '%s' -> '%s'...", str(src), str(dest))
    text = Path(src).read_text()
    write_text(dest, text, modifications=modifications)


def ensure_new_line(text: str, /) -> str:
    return text.rstrip("\n") + "\n"


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


def write_text(
    path: PathLike, text: str, /, *, modifications: MutableSet[Path] | None = None
) -> None:
    LOGGER.info("Writing '%s'...", str(path))
    with writer(path, overwrite=True) as temp:
        _ = temp.write_text(ensure_new_line(text))
    if modifications is not None:
        modifications.add(Path(path))


def yaml_dump(obj: Any, /) -> str:
    stream = StringIO()
    YAML_INSTANCE.dump(obj, stream)
    return stream.getvalue()


##


__all__ = [
    "LOADER",
    "are_docs_unequal",
    "are_modules_equal",
    "are_texts_equal",
    "convert_list_strs",
    "convert_secret_str",
    "convert_str",
    "copy_text",
    "ensure_new_line",
    "logged_run",
    "write_text",
    "yaml_dump",
]
