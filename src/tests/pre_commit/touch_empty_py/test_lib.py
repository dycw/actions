from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import fixture
from utilities.text import strip_and_dedent

from actions.pre_commit.touch_empty_py.lib import _format_path

if TYPE_CHECKING:
    from pathlib import Path


@fixture
def input_() -> str:
    return strip_and_dedent("""
""")


@fixture
def output() -> str:
    return strip_and_dedent(
        """
from __future__ import annotations
""",
        trailing=True,
    )


class TestFormatPath:
    def test_main(self, *, tmp_path: Path, input_: str, output: str) -> None:
        path = tmp_path / "file.py"
        _ = path.write_text(input_)
        _format_path(path)
        result = path.read_text()
        assert result == output
