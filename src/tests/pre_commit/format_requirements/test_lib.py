from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import fixture
from tomlkit import loads

from actions.pre_commit.format_requirements.lib import _format_path, _get_formatted

if TYPE_CHECKING:
    from pathlib import Path


@fixture
def root(*, tests_pre_commit: Path) -> Path:
    return tests_pre_commit / "format_requirements"


class TestFormatPath:
    def test_main(self, *, root: Path, tmp_path: Path) -> None:
        path = tmp_path / "file.toml"
        _ = path.write_text((root / "in.toml").read_text())
        _format_path(path)
        result = path.read_text()
        expected = root.joinpath("out.toml").read_text()
        assert result == expected


class TestGetFormatted:
    def test_main(self, *, root: Path) -> None:
        result = _get_formatted(root.joinpath("in.toml"))
        expected = loads(root.joinpath("out.toml").read_text())
        assert result == expected
