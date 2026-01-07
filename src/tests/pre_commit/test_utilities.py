from __future__ import annotations

import json
from typing import TYPE_CHECKING

from pytest import mark, param

from actions.pre_commit.utilities import yield_write_context

if TYPE_CHECKING:
    from pathlib import Path


class TestYieldWriteContext:
    @mark.parametrize("leading", [param(""), param("\n"), param("\n\n")])
    @mark.parametrize("trailing", [param(""), param("\n"), param("\n\n")])
    def test_modified(self, *, tmp_path: Path, leading: str, trailing: str) -> None:
        path = tmp_path / "file.json"
        _ = path.write_text(leading + json.dumps({"a": 1}) + trailing)
        with yield_write_context(path, json.loads, dict, json.dumps) as temp:
            temp["b"] = 2
        expected = '{"a": 1, "b": 2}\n'
        assert path.read_text() == expected

    @mark.parametrize("leading", [param(""), param("\n"), param("\n\n")])
    @mark.parametrize("trailing", [param(""), param("\n"), param("\n\n")])
    def test_unmodified(self, *, tmp_path: Path, leading: str, trailing: str) -> None:
        path = tmp_path / "file.json"
        initial = leading + json.dumps({"a": 1}) + trailing
        _ = path.write_text(initial)
        with yield_write_context(path, json.loads, dict, json.dumps):
            ...
        assert path.read_text() == initial
