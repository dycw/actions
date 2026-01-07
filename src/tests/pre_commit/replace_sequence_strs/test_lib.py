from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import fixture
from utilities.text import strip_and_dedent

from actions.pre_commit.replace_sequence_strs.lib import _format_path

if TYPE_CHECKING:
    from pathlib import Path


@fixture
def input_() -> str:
    return strip_and_dedent("""
from collections.abc import Sequence

x: Sequence[str]
""")


@fixture
def output() -> str:
    return strip_and_dedent(
        """
from collections.abc import Sequence

x: list[str]
""",
        trailing=True,
    )


class TestFormatPath:
    def test_main(self, *, tmp_path: Path, input_: str, output: str) -> None:
        path = tmp_path / "file.py"
        _ = path.write_text(input_)
        for i in range(2):
            modifications: set[Path] = set()
            _format_path(path, modifications=modifications)
            result = path.read_text()
            assert result == output
            assert len(modifications) == (1 if i == 0 else 0)
