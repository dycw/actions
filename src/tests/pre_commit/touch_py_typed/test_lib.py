from __future__ import annotations

from typing import TYPE_CHECKING

from actions.pre_commit.touch_py_typed.lib import _format_path

if TYPE_CHECKING:
    from pathlib import Path


class TestFormatPath:
    def test_main(self, *, tmp_path: Path) -> None:
        pyproject = tmp_path / "pyproject.toml"
        pyproject.touch()
        src = tmp_path / "src"
        src.mkdir()
        package = src / "package"
        package.mkdir()
        tests = src / "tests"
        tests.mkdir()
        _format_path(pyproject)
        assert (package / "py.typed").is_file()
