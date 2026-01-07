from __future__ import annotations

import json
from collections.abc import Iterator, MutableSet
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import tomlkit
from libcst import Module, parse_module
from rich.pretty import pretty_repr
from tomlkit import TOMLDocument, aot, array, document, table
from tomlkit.items import AoT, Array, Table
from utilities.functions import ensure_class
from utilities.iterables import OneEmptyError, OneNonUniqueError, one
from utilities.tempfile import TemporaryFile
from utilities.types import PathLike

from actions.constants import YAML_INSTANCE
from actions.logging import LOGGER
from actions.types import StrDict
from actions.utilities import are_texts_equal, copy_text, write_text, yaml_dump

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator, MutableSet

    from utilities.types import PathLike

    from actions.types import HasAppend, HasSetDefault, StrDict


def ensure_aot_contains(array: AoT, /, *tables: Table) -> None:
    for table_ in tables:
        if table_ not in array:
            array.append(table_)


def ensure_contains(array: HasAppend, /, *objs: Any) -> None:
    if isinstance(array, AoT):
        msg = f"Use {ensure_aot_contains.__name__!r} instead of {ensure_contains.__name__!r}"
        raise TypeError(msg)
    for obj in objs:
        if obj not in array:
            array.append(obj)


def ensure_contains_partial(
    container: HasAppend, partial: StrDict, /, *, extra: StrDict | None = None
) -> StrDict:
    try:
        return get_partial_dict(container, partial, skip_log=True)
    except OneEmptyError:
        dict_ = partial | ({} if extra is None else extra)
        container.append(dict_)
        return dict_


def ensure_not_contains(array: Array, /, *objs: Any) -> None:
    for obj in objs:
        try:
            index = next(i for i, o in enumerate(array) if o == obj)
        except StopIteration:
            pass
        else:
            del array[index]


##


def get_aot(container: HasSetDefault, key: str, /) -> AoT:
    return ensure_class(container.setdefault(key, aot()), AoT)


def get_array(container: HasSetDefault, key: str, /) -> Array:
    return ensure_class(container.setdefault(key, array()), Array)


def get_dict(container: HasSetDefault, key: str, /) -> StrDict:
    return ensure_class(container.setdefault(key, {}), dict)


def get_list(container: HasSetDefault, key: str, /) -> list[Any]:
    return ensure_class(container.setdefault(key, []), list)


def get_table(container: HasSetDefault, key: str, /) -> Table:
    return ensure_class(container.setdefault(key, table()), Table)


##


def get_partial_dict(
    iterable: Iterable[Any], dict_: StrDict, /, *, skip_log: bool = False
) -> StrDict:
    try:
        return one(i for i in iterable if is_partial_dict(dict_, i))
    except OneEmptyError:
        if not skip_log:
            LOGGER.exception(
                "Expected %s to contain %s (as a partial)",
                pretty_repr(iterable),
                pretty_repr(dict_),
            )
        raise
    except OneNonUniqueError as error:
        LOGGER.exception(
            "Expected %s to contain %s uniquely (as a partial); got %s, %s and perhaps more",
            pretty_repr(iterable),
            pretty_repr(dict_),
            pretty_repr(error.first),
            pretty_repr(error.second),
        )
        raise


def is_partial_dict(obj: Any, dict_: StrDict, /) -> bool:
    if not isinstance(obj, dict):
        return False
    results: dict[str, bool] = {}
    for key, obj_value in obj.items():
        try:
            dict_value = dict_[key]
        except KeyError:
            results[key] = False
        else:
            if isinstance(obj_value, dict) and isinstance(dict_value, dict):
                results[key] = is_partial_dict(obj_value, dict_value)
            else:
                results[key] = obj_value == dict_value
    return all(results.values())


##


@contextmanager
def yield_json_dict(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> Iterator[StrDict]:
    with yield_write_context(
        path, json.loads, dict, json.dumps, modifications=modifications
    ) as dict_:
        yield dict_


##


@contextmanager
def yield_python_file(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> Iterator[Module]:
    with yield_write_context(
        path,
        parse_module,
        lambda: Module(body=[]),
        lambda module: module.code,
        modifications=modifications,
    ) as module:
        yield module


##


@contextmanager
def yield_text_file(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> Iterator[Path]:
    path = Path(path)
    try:
        current = path.read_text()
    except FileNotFoundError:
        with TemporaryFile() as temp:
            yield temp
            copy_text(temp, path, modifications=modifications)
    else:
        with TemporaryFile(text=current) as temp:
            yield temp
            if not are_texts_equal(temp.read_text(), current):
                copy_text(temp, path, modifications=modifications)


##


@contextmanager
def yield_toml_doc(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> Iterator[TOMLDocument]:
    with yield_write_context(
        path, tomlkit.parse, document, tomlkit.dumps, modifications=modifications
    ) as doc:
        yield doc


##


@contextmanager
def yield_write_context[T](
    path: PathLike,
    loads: Callable[[str], T],
    get_default: Callable[[], T],
    dumps: Callable[[T], str],
    /,
    *,
    modifications: MutableSet[Path] | None = None,
) -> Iterator[T]:
    try:
        current = Path(path).read_text()
    except FileNotFoundError:
        yield (default := get_default())
        write_text(path, dumps(default), modifications=modifications)
    else:
        data = loads(current)
        yield data
        if not (data == loads(current)):  # noqa: SIM201
            write_text(path, dumps(data), modifications=modifications)


##


@dataclass(kw_only=True, slots=True)
class ImmutableWriteContext[T]:
    input: T
    output: T | None = None


@contextmanager
def yield_immutable_write_context[T](
    path: PathLike,
    loads: Callable[[str], T],
    get_default: Callable[[], T],
    dumps: Callable[[T], str],
    /,
    *,
    modifications: MutableSet[Path] | None = None,
) -> Iterator[ImmutableWriteContext[T]]:
    try:
        current = Path(path).read_text()
    except FileNotFoundError:
        current = None
        input_ = get_default()
    else:
        input_ = loads(current)
    yield (context := ImmutableWriteContext(input=input_))
    if (output := context.output) is None:
        msg = "Context output is missing"
        raise ValueError(msg)
    if (current is None) or (not (output == loads(current))):  # noqa: SIM201
        write_text(path, dumps(output), modifications=modifications)


##


@contextmanager
def yield_yaml_dict(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> Iterator[StrDict]:
    with yield_write_context(
        path, YAML_INSTANCE.load, dict, yaml_dump, modifications=modifications
    ) as dict_:
        yield dict_


__all__ = [
    "ensure_aot_contains",
    "ensure_contains",
    "ensure_contains_partial",
    "ensure_not_contains",
    "get_aot",
    "get_array",
    "get_dict",
    "get_list",
    "get_partial_dict",
    "get_table",
    "is_partial_dict",
    "yield_immutable_write_context",
    "yield_json_dict",
    "yield_python_file",
    "yield_text_file",
    "yield_toml_doc",
    "yield_write_context",
    "yield_yaml_dict",
]
