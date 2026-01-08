from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from tomlkit.items import Array, Table
from typed_settings import Secret
from utilities.packaging import Requirement

if TYPE_CHECKING:
    from tomlkit.container import Container


type FuncRequirement = Callable[[Requirement], Requirement]
type HasAppend = Array | list[Any]
type HasSetDefault = Container | StrDict | Table
type SecretLike = str | Secret[str]
type StrDict = dict[str, Any]


__all__ = ["FuncRequirement", "HasAppend", "HasSetDefault", "SecretLike", "StrDict"]
