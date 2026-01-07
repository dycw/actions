from __future__ import annotations

from typing import TYPE_CHECKING

from libcst import parse_module
from pytest import fixture

from actions.pre_commit.replace_sequence_strs.lib import _format_path, _get_formatted
from actions.utilities import are_modules_equal

if TYPE_CHECKING:
    from pathlib import Path


@fixture
def root(*, tests_pre_commit: Path) -> Path:
    return tests_pre_commit / "replace_sequence_strs"


class TestFormatPath:
    def test_main(self, *, root: Path, tmp_path: Path) -> None:
        path = tmp_path / "file.py"
        _ = path.write_text((root / "in_.py").read_text())
        _format_path(path)
        result = parse_module(path.read_text())
        expected = parse_module(root.joinpath("out.py").read_text())
        assert are_modules_equal(result, expected)


class TestGetFormatted:
    def test_main(self, *, root: Path) -> None:
        result = _get_formatted(root.joinpath("in_.py"))
        expected = parse_module(root.joinpath("out.py").read_text())
        assert are_modules_equal(result, expected)
