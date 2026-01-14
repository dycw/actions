from __future__ import annotations

from collections.abc import Callable

from tomlkit.items import AoT
from typed_settings import Secret
from utilities.packaging import Requirement
from utilities.types import StrDict

type ArrayLike = AoT | list[str] | list[StrDict]
type FuncRequirement = Callable[[Requirement], Requirement]
type SecretLike = str | Secret[str]


__all__ = ["ArrayLike", "FuncRequirement", "SecretLike"]
