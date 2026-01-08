from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import fixture
from utilities.text import strip_and_dedent

from actions.pre_commit.update_requirements.lib import _format_path

if TYPE_CHECKING:
    from pathlib import Path


@fixture
def input_() -> str:
    return strip_and_dedent("""
[project]
  dependencies = [
    "unbounded",
    "lower-unchanged >=1.2.3",
    "lower-changed >=1.2.3",
    "upper-unchanged <1.3",
    "upper-changed <1.3",
    "lower-and-upper-unchanged >=1.2.3, <1.3",
    "lower-and-upper-changed1 >=1.2.3, <1.3",
    "lower-and-upper-changed2 >=1.2.3, <9.9",
  ]
""")


@fixture
def output() -> str:
    return strip_and_dedent(
        """
[project]
  dependencies = ["unbounded", "lower1 >=1.2.3", "lower2 >=1.2.3", "upper1 <1.3", "upper2 <1.3", "lower-and-upper1 >=1.2.3, <1.3", "lower-and-upper2 >=1.2.3, <1.3", "lower-and-upper3 >=1.2.3, <1.3", "with-extra[extra1]", "with-extra[extra2] >=1.2.3", "with-extra[extra3] >=1.2.3"]
""",
        trailing=True,
    )


class TestFormatPath:
    def test_main(self, *, tmp_path: Path, input_: str, output: str) -> None:
        path = tmp_path / "file.toml"
        _ = path.write_text(input_)
        for i in range(2):
            modifications: set[Path] = set()
            _format_path(path, modifications=modifications)
            result = path.read_text()
            assert result == output
            assert len(modifications) == (1 if i == 0 else 0)
