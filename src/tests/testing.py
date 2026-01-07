from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.text import strip_and_dedent

if TYPE_CHECKING:
    from libcst import Module


def check_modules_equal(left: Module, right: Module, /) -> None:
    left_text = left.code.rstrip("\n")
    right_text = right.code.rstrip("\n")
    if left_text != right_text:
        msg = strip_and_dedent(f"""
Modules must be equal; got:

==== LEFT =====================================================================
{left_text}
==== RIGHT ====================================================================
{right_text}
""")
        raise ValueError(msg)
