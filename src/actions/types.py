from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tomlkit.items import Array, Table
from typed_settings import Secret

if TYPE_CHECKING:
    from tomlkit.container import Container


type HasAppend = Array | list[Any]
type HasSetDefault = Container | StrDict | Table
type SecretLike = str | Secret[str]
type StrDict = dict[str, Any]


__all__ = ["HasAppend", "HasSetDefault", "SecretLike", "StrDict"]
