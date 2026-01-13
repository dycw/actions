from __future__ import annotations

from typing import TYPE_CHECKING

from actions.constants import PYPROJECT_TOML
from actions.pre_commit.touch_py_typed.lib import _format_path

if TYPE_CHECKING:
    from pathlib import Path


class TestFormatPath:
    def test_main(self, *, tmp_path: Path) -> None:
        pyproject = tmp_path / PYPROJECT_TOML.name
        pyproject.touch()
        src = tmp_path / "src"
        src.mkdir()
        package = src / "package"
        package.mkdir()
        tests = src / "tests"
        tests.mkdir()
        for i in range(2):
            modifications: set[Path] = set()
            _format_path(pyproject, modifications=modifications)
            assert (package / "py.typed").is_file()
            assert len(modifications) == (1 if i == 0 else 0)
