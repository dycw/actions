from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import fixture
from tomlkit import loads

from actions.format_requirements.lib import _format_path, _get_formatted

if TYPE_CHECKING:
    from pathlib import Path


@fixture
def path_tests_i(*, path_tests: Path) -> Path:
    return path_tests / "requirements"


class TestFormatPath:
    def test_main(self, *, path_tests_i: Path, tmp_path: Path) -> None:
        path = tmp_path / "file.toml"
        _ = path.write_text((path_tests_i / "in.toml").read_text())
        _format_path(path)
        result = loads(path.read_text())
        expected = loads(path_tests_i.joinpath("out.toml").read_text())
        assert result == expected


class TestGetFormatted:
    def test_main(self, *, path_tests_i: Path) -> None:
        result = _get_formatted(path_tests_i.joinpath("in.toml"))
        expected = loads(path_tests_i.joinpath("out.toml").read_text())
        assert result == expected
