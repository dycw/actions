from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from tomlkit.items import Array, Table
from typed_settings import Secret
from utilities.packaging import Requirement
from utilities.types import StrDict

if TYPE_CHECKING:
    from tomlkit.container import Container


type FuncRequirement = Callable[[Requirement], Requirement]
type HasAppend = Array | list[Any]
type HasSetDefault = Container | StrDict | Table
type SecretLike = str | Secret[str]


__all__ = ["FuncRequirement", "HasAppend", "HasSetDefault", "SecretLike"]
