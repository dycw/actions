from __future__ import annotations

import json
from collections.abc import Iterator, MutableSet
from contextlib import contextmanager, suppress
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, assert_never, overload

import tomlkit
from libcst import Module, parse_module
from rich.pretty import pretty_repr
from tomlkit import TOMLDocument, aot, array, document, string, table
from tomlkit.items import AoT, Array, Table
from utilities.functions import ensure_class, ensure_str, get_func_name
from utilities.iterables import OneEmptyError, OneNonUniqueError, one
from utilities.packaging import Requirement
from utilities.types import PathLike, StrDict
from utilities.typing import is_str_dict

from actions.constants import PATH_CACHE, PYPROJECT_TOML, YAML_INSTANCE
from actions.logging import LOGGER
from actions.utilities import are_equal_modulo_new_line, write_text, yaml_dump

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable, Iterator, MutableSet

    from utilities.types import PathLike, StrDict

    from actions.types import ArrayLike, ContainerLike, FuncRequirement


##


@overload
def ensure_contains(container: AoT, /, *objs: Table) -> None: ...
@overload
def ensure_contains(container: list[str], /, *objs: str) -> None: ...
@overload
def ensure_contains(container: list[StrDict], /, *objs: StrDict) -> None: ...
def ensure_contains(container: ArrayLike, /, *objs: Any) -> None:
    for obj in objs:
        if obj not in container:
            container.append(obj)


def ensure_contains_partial_dict(
    container: list[StrDict], partial: StrDict, /, *, extra: StrDict | None = None
) -> StrDict:
    try:
        return get_partial_dict(container, partial, skip_log=True)
    except OneEmptyError:
        dict_ = partial | ({} if extra is None else extra)
        container.append(dict_)
        return dict_


def ensure_contains_partial_str(list_: Array | list[str], text: str, /) -> str:
    try:
        return get_partial_str(list_, text, skip_log=True)
    except OneEmptyError:
        list_.append(text)
        return text


@overload
def ensure_not_contains(container: AoT, /, *objs: Table) -> None: ...
@overload
def ensure_not_contains(container: list[str], /, *objs: str) -> None: ...
@overload
def ensure_not_contains(container: list[StrDict], /, *objs: StrDict) -> None: ...
def ensure_not_contains(container: ArrayLike, /, *objs: Any) -> None:
    for obj in objs:
        try:
            index = next(i for i, o in enumerate(container) if o == obj)
        except StopIteration:
            pass
        else:
            del container[index]


##


def get_aot(container: ContainerLike, key: str, /) -> AoT:
    return ensure_class(container[key], AoT)


def get_array(container: ContainerLike, key: str, /) -> Array:
    return ensure_class(container[key], Array)


def get_dict(dict_: StrDict, key: str, /) -> StrDict:
    if is_str_dict(value := dict_[key]):
        return value
    raise TypeError(value)


def get_list_dicts(dict_: StrDict, key: str, /) -> list[StrDict]:
    list_ = ensure_class(dict_[key], list)
    for i in list_:
        if not is_str_dict(i):
            raise TypeError(i)
    return list_


def get_list_strs(dict_: StrDict, key: str, /) -> list[str]:
    list_ = ensure_class(dict_[key], list)
    for i in list_:
        if not isinstance(i, str):
            raise TypeError(i)
    return list_


def get_table(container: ContainerLike, key: str, /) -> Table:
    return ensure_class(container[key], Table)


##


def get_set_aot(container: ContainerLike, key: str, /) -> AoT:
    try:
        return get_aot(container, key)
    except KeyError:
        value = container[key] = aot()
        return value


def get_set_array(container: ContainerLike, key: str, /) -> Array:
    try:
        return get_array(container, key)
    except KeyError:
        value = container[key] = array()
        return value


def get_set_dict(dict_: StrDict, key: str, /) -> StrDict:
    try:
        return get_dict(dict_, key)
    except KeyError:
        value = dict_[key] = {}
        return value


def get_set_list_dicts(dict_: StrDict, key: str, /) -> list[StrDict]:
    try:
        return get_list_dicts(dict_, key)
    except KeyError:
        value = dict_[key] = []
        return value


def get_set_list_strs(dict_: StrDict, key: str, /) -> list[str]:
    try:
        return get_list_strs(dict_, key)
    except KeyError:
        value = dict_[key] = []
        return value


def get_set_table(container: ContainerLike, key: str, /) -> Table:
    try:
        return get_table(container, key)
    except KeyError:
        value = container[key] = table()
        return value


##


def get_partial_dict(
    iterable: Iterable[StrDict], dict_: StrDict, /, *, skip_log: bool = False
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


def get_partial_str(
    iterable: Iterable[Any], text: str, /, *, skip_log: bool = False
) -> str:
    try:
        return one(i for i in iterable if is_partial_str(i, text))
    except OneEmptyError:
        if not skip_log:
            LOGGER.exception(
                "Expected %s to contain %s (as a partial)",
                pretty_repr(iterable),
                pretty_repr(text),
            )
        raise
    except OneNonUniqueError as error:
        LOGGER.exception(
            "Expected %s to contain %s uniquely (as a partial); got %s, %s and perhaps more",
            pretty_repr(iterable),
            pretty_repr(text),
            pretty_repr(error.first),
            pretty_repr(error.second),
        )
        raise


def is_partial_str(obj: Any, text: str, /) -> bool:
    return isinstance(obj, str) and (text in obj)


##


def get_pyproject_dependencies(doc: TOMLDocument, /) -> PyProjectDependencies:
    out = PyProjectDependencies()
    try:
        project = get_table(doc, "project")
    except KeyError:
        pass
    else:
        with suppress(KeyError):
            out.dependencies = get_array(project, "dependencies")
        try:
            opt_dependencies = get_table(project, "optional-dependencies")
        except KeyError:
            pass
        else:
            out.opt_dependencies = {}
            for key in opt_dependencies:
                out.opt_dependencies[ensure_str(key)] = get_array(opt_dependencies, key)
    try:
        dep_grps = get_table(doc, "dependency-groups")
    except KeyError:
        pass
    else:
        out.dep_groups = {}
        for key in dep_grps:
            out.dep_groups[ensure_str(key)] = get_array(dep_grps, key)
    return out


@dataclass(kw_only=True, slots=True)
class PyProjectDependencies:
    dependencies: Array | None = None
    opt_dependencies: dict[str, Array] | None = None
    dep_groups: dict[str, Array] | None = None

    def apply(self, func: FuncRequirement, /) -> None:
        if (deps := self.dependencies) is not None:
            self._apply_to_array(deps, func)
        if (opt_depedencies := self.opt_dependencies) is not None:
            for deps in opt_depedencies.values():
                self._apply_to_array(deps, func)
        if (dep_grps := self.dep_groups) is not None:
            for deps in dep_grps.values():
                self._apply_to_array(deps, func)

    def _apply_to_array(self, array: Array, func: FuncRequirement, /) -> None:
        strs = list(map(ensure_str, array))
        reqs = list(map(Requirement, strs))
        results = list(map(func, reqs))
        new_strs = list(map(str, results))
        strings = list(map(string, new_strs))
        array.clear()
        ensure_contains(array, *strings)


##


def path_throttle_cache(func: Callable[..., Any]) -> Path:
    func_name = get_func_name(func)
    cwd_name = Path.cwd().name
    return PATH_CACHE / "throttle" / f"{func_name}--{cwd_name}"


##


@dataclass(kw_only=True, slots=True)
class WriteContext[T]:
    input: T
    output: T


@contextmanager
def yield_immutable_write_context[T](
    path: PathLike,
    loads: Callable[[str], T],
    get_default: Callable[[], T],
    dumps: Callable[[T], str],
    /,
    *,
    modifications: MutableSet[Path] | None = None,
) -> Iterator[WriteContext[T]]:
    try:
        current = Path(path).read_text()
    except FileNotFoundError:
        current = None
        input_ = get_default()
        output = get_default()
    else:
        input_ = loads(current)
        output = loads(current)
    yield (context := WriteContext(input=input_, output=output))
    if current is None:
        write_text(path, dumps(context.output), modifications=modifications)
    else:
        match context.output, loads(current):
            case Module() as output_module, Module() as current_module:
                if not are_equal_modulo_new_line(
                    output_module.code, current_module.code
                ):
                    write_text(path, dumps(output_module), modifications=modifications)
            case TOMLDocument() as output_doc, TOMLDocument() as current_doc:
                if not (output_doc == current_doc):  # noqa: SIM201
                    write_text(path, dumps(output_doc), modifications=modifications)
            case str() as output_text, str() as current_text:
                if not are_equal_modulo_new_line(output_text, current_text):
                    write_text(path, dumps(output_text), modifications=modifications)
            case output_obj, current_obj:
                if output_obj != current_obj:
                    write_text(path, dumps(output_obj), modifications=modifications)
            case never:
                assert_never(never)


##


@contextmanager
def yield_json_dict(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> Iterator[StrDict]:
    with yield_mutable_write_context(
        path, json.loads, dict, json.dumps, modifications=modifications
    ) as dict_:
        yield dict_


##


@contextmanager
def yield_pyproject_toml(
    *, modifications: MutableSet[Path] | None = None
) -> Iterator[TOMLDocument]:
    with yield_toml_doc(PYPROJECT_TOML, modifications=modifications) as doc:
        yield doc


##


@contextmanager
def yield_mutable_write_context[T](
    path: PathLike,
    loads: Callable[[str], T],
    get_default: Callable[[], T],
    dumps: Callable[[T], str],
    /,
    *,
    modifications: MutableSet[Path] | None = None,
) -> Iterator[T]:
    with yield_immutable_write_context(
        path, loads, get_default, dumps, modifications=modifications
    ) as context:
        yield context.output


##


@contextmanager
def yield_python_file(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> Iterator[WriteContext[Module]]:
    with yield_immutable_write_context(
        path,
        parse_module,
        lambda: Module(body=[]),
        lambda module: module.code,
        modifications=modifications,
    ) as context:
        yield context


##


@contextmanager
def yield_text_file(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> Iterator[WriteContext[str]]:
    with yield_immutable_write_context(
        path, str, lambda: "", str, modifications=modifications
    ) as context:
        yield context


##


@contextmanager
def yield_toml_doc(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> Iterator[TOMLDocument]:
    with yield_mutable_write_context(
        path, tomlkit.parse, document, tomlkit.dumps, modifications=modifications
    ) as doc:
        yield doc


##


@contextmanager
def yield_yaml_dict(
    path: PathLike, /, *, modifications: MutableSet[Path] | None = None
) -> Iterator[StrDict]:
    with yield_mutable_write_context(
        path, YAML_INSTANCE.load, dict, yaml_dump, modifications=modifications
    ) as dict_:
        yield dict_


__all__ = [
    "PyProjectDependencies",
    "WriteContext",
    "ensure_contains",
    "ensure_contains_partial_dict",
    "ensure_contains_partial_str",
    "ensure_not_contains",
    "get_aot",
    "get_array",
    "get_dict",
    "get_list_dicts",
    "get_list_strs",
    "get_partial_dict",
    "get_partial_str",
    "get_pyproject_dependencies",
    "get_set_aot",
    "get_set_array",
    "get_set_dict",
    "get_set_list_dicts",
    "get_set_list_strs",
    "get_set_table",
    "get_table",
    "is_partial_dict",
    "is_partial_str",
    "path_throttle_cache",
    "yield_immutable_write_context",
    "yield_json_dict",
    "yield_mutable_write_context",
    "yield_pyproject_toml",
    "yield_python_file",
    "yield_text_file",
    "yield_toml_doc",
    "yield_yaml_dict",
]
