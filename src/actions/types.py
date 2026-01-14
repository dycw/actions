from __future__ import annotations

from collections.abc import Callable

from tomlkit import TOMLDocument
from tomlkit.items import AoT, Table
from typed_settings import Secret
from utilities.packaging import Requirement
from utilities.types import StrDict

type ArrayLike = AoT | list[str] | list[StrDict]
type FuncRequirement = Callable[[Requirement], Requirement]
type SecretLike = str | Secret[str]
type TableLike = TOMLDocument | Table


__all__ = ["ArrayLike", "FuncRequirement", "SecretLike", "TableLike"]
