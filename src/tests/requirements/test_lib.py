from __future__ import annotations

from pathlib import Path

from actions.requirements.lib import _get_formatted


class TestGetFormatted:
    def test_main(self) -> None:
        root = Path(__file__).parent
        result = _get_formatted(root.joinpath("in.toml"))
        expected = root.joinpath("out.toml").read_text()
        assert result == expected
