from __future__ import annotations

from io import StringIO
from pathlib import Path
from textwrap import indent
from typing import TYPE_CHECKING, Any, Literal, assert_never, overload

from tabulate import tabulate
from typed_settings import EnvLoader, Secret
from utilities.atomicwrites import writer
from utilities.functions import get_func_name
from utilities.subprocess import run
from utilities.text import split_str, strip_and_dedent

from actions import __version__
from actions.constants import YAML_INSTANCE
from actions.logging import LOGGER

if TYPE_CHECKING:
    from collections.abc import Callable, MutableSet

    from utilities.types import PathLike, StrStrMapping

    from actions.types import SecretLike


LOADER = EnvLoader("")


def are_equal_modulo_new_line(x: str, y: str, /) -> bool:
    return ensure_new_line(x) == ensure_new_line(y)


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
    return text.strip("\n") + "\n"


def log_func_call(func: Callable[..., Any], /, *variables: str) -> str:
    name = get_func_name(func)
    table = tabulate(
        list(map(split_f_str_equals, variables)), tablefmt="rounded_outline"
    )
    indented = indent(table, "  ")
    return strip_and_dedent(
        f"""
        Running {name!r} (version {__version__}) with settings:
        {indented}
        """
    )


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


def split_f_str_equals(text: str, /) -> tuple[str, str]:
    """Split an `f`-string with `=`."""
    return split_str(text, separator="=", n=2)


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
    "are_equal_modulo_new_line",
    "convert_list_strs",
    "convert_secret_str",
    "convert_str",
    "copy_text",
    "ensure_new_line",
    "logged_run",
    "split_f_str_equals",
    "write_text",
    "yaml_dump",
]
