from __future__ import annotations

from typing import Any

from typed_settings import Secret

type SecretLike = str | Secret[str]
type StrDict = dict[str, Any]


__all__ = ["SecretLike", "StrDict"]
