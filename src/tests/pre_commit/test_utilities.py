from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from pytest import mark, param, raises
from utilities.iterables import one

from actions.pre_commit.utilities import (
    get_partial_dict,
    is_partial_dict,
    yield_immutable_write_context,
    yield_mutable_write_context,
)

if TYPE_CHECKING:
    from pathlib import Path

    from actions.types import StrDict


class TestGetPartialDict:
    def test_main(self) -> None:
        url = "https://github.com/owner/repo"
        repos_list = [
            {"repo": url, "rev": "v6.0.0", "hooks": [{"id": "id1"}, {"id": "id2"}]}
        ]
        result = get_partial_dict(repos_list, {"repo": url})
        assert result == one(repos_list)


class TestIsPartialDict:
    @mark.parametrize(
        ("obj", "dict_", "expected"),
        [
            param(None, {}, False),
            param({}, {}, True),
            param({}, {"a": 1}, True),
            param({"a": 1}, {}, False),
            param({"a": 1}, {"a": 1}, True),
            param({"a": 1}, {"a": 2}, False),
            param({"a": 1, "b": 2}, {"a": 1}, False),
            param({"a": 1}, {"a": 1, "b": 2}, True),
            param({"a": 1, "b": 2}, {"a": 1, "b": 2}, True),
            param({"a": 1, "b": 2}, {"a": 1, "b": 3}, False),
            param({"a": 1, "b": {}}, {"a": 1, "b": {}}, True),
            param({"a": 1, "b": {"c": 2}}, {"a": 1, "b": {}}, False),
            param({"a": 1, "b": {}}, {"a": 1, "b": {"c": 2}}, True),
            param({"a": 1, "b": {"c": 2}}, {"a": 1, "b": {"c": 2}}, True),
            param({"a": 1, "b": {"c": 2}}, {"a": 1, "b": {"c": 3}}, False),
        ],
    )
    def test_main(self, *, obj: Any, dict_: StrDict, expected: bool) -> None:
        assert is_partial_dict(obj, dict_) is expected


class TestYieldImmutableWriteContext:
    @mark.parametrize("init", [param("init"), param("init\n"), param("init\n\n")])
    def test_modified(self, *, tmp_path: Path, init: str) -> None:
        path = tmp_path / "file.txt"
        _ = path.write_text(init)
        with yield_immutable_write_context(path, str, lambda: "", str) as context:
            context.output = context.input.replace("init", "init\npost")
        expected = "init\npost\n"
        assert path.read_text() == expected

    @mark.parametrize("init", [param("init"), param("init\n"), param("init\n\n")])
    def test_unmodified(self, *, tmp_path: Path, init: str) -> None:
        path = tmp_path / "file.txt"
        _ = path.write_text(init)
        with yield_immutable_write_context(path, str, lambda: "", str):
            ...
        assert path.read_text() == init


class TestYieldMutableWriteContext:
    @mark.parametrize("leading", [param(""), param("\n"), param("\n\n")])
    @mark.parametrize("trailing", [param(""), param("\n"), param("\n\n")])
    def test_modified(self, *, tmp_path: Path, leading: str, trailing: str) -> None:
        path = tmp_path / "file.json"
        _ = path.write_text(leading + json.dumps({"a": 1}) + trailing)
        with yield_mutable_write_context(path, json.loads, dict, json.dumps) as temp:
            temp["b"] = 2
        expected = '{"a": 1, "b": 2}\n'
        assert path.read_text() == expected

    @mark.parametrize("leading", [param(""), param("\n"), param("\n\n")])
    @mark.parametrize("trailing", [param(""), param("\n"), param("\n\n")])
    def test_unmodified(self, *, tmp_path: Path, leading: str, trailing: str) -> None:
        path = tmp_path / "file.json"
        initial = leading + json.dumps({"a": 1}) + trailing
        _ = path.write_text(initial)
        with yield_mutable_write_context(path, json.loads, dict, json.dumps):
            ...
        assert path.read_text() == initial
