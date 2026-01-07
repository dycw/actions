from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from libcst import SimpleStatementLine, parse_statement
from pytest import mark, param, raises
from utilities.iterables import one

from actions.pre_commit.utilities import (
    get_partial_dict,
    is_partial_dict,
    yield_immutable_write_context,
    yield_mutable_write_context,
    yield_python_file,
    yield_text_file,
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


class TestYieldWriteContext:
    @mark.parametrize("init", [param("init"), param("init\n"), param("init\n\n")])
    def test_modified(self, *, tmp_path: Path, init: str) -> None:
        path = tmp_path / "file.txt"
        _ = path.write_text(init)
        with yield_immutable_write_context(path, str, lambda: "", str) as temp:
            temp.output = temp.input.replace("init", "init\npost")
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
    @mark.parametrize("init", [param("{}"), param("{}\n"), param("{}\n\n")])
    def test_modified(self, *, tmp_path: Path, init: str) -> None:
        path = tmp_path / "file.json"
        _ = path.write_text(init)
        with yield_mutable_write_context(path, json.loads, dict, json.dumps) as temp:
            temp["a"] = 1
        expected = '{"a": 1}\n'
        assert path.read_text() == expected

    @mark.parametrize("init", [param("{}"), param("{}\n"), param("{}\n\n")])
    def test_unmodified(self, *, tmp_path: Path, init: str) -> None:
        path = tmp_path / "file.json"
        _ = path.write_text(init)
        with yield_mutable_write_context(path, json.loads, dict, json.dumps):
            ...
        assert path.read_text() == init


class TestYieldPythonFile:
    @mark.parametrize(
        ("init", "expected"),
        [
            param("", "import abc\n"),
            param("\n", "\nimport abc\n"),
            param("\n\n", "\n\nimport abc\n"),
            param("\n\n\n", "\n\n\nimport abc\n"),
        ],
    )
    def test_modified(self, *, tmp_path: Path, init: str, expected: str) -> None:
        path = tmp_path / "file.py"
        _ = path.write_text(init)
        with yield_python_file(path) as temp:
            body = [*temp.input.body, parse_statement("import abc")]
            temp.output = temp.input.with_changes(body=body)
        assert path.read_text() == expected

    @mark.parametrize(
        ("init", "expected"),
        [
            param("", "\n"),
            param("\n", "\n"),
            param("\n\n", "\n"),
            param("\n\n\n", "\n"),
        ],
    )
    def test_unmodified(self, *, tmp_path: Path, init: str, expected: str) -> None:
        path = tmp_path / "file.py"
        _ = path.write_text(init)
        with yield_python_file(path):
            ...
        assert path.read_text() == expected


class TestYieldTextFile:
    @mark.parametrize("init", [param("init"), param("init\n"), param("init\n\n")])
    def test_modified(self, *, tmp_path: Path, init: str) -> None:
        path = tmp_path / "file.txt"
        _ = path.write_text(init)
        with yield_text_file(path) as temp:
            temp.output = temp.input.replace("init", "init\npost")
        expected = "init\npost\n"
        assert path.read_text() == expected

    @mark.parametrize("init", [param("init"), param("init\n"), param("init\n\n")])
    def test_unmodified(self, *, tmp_path: Path, init: str) -> None:
        path = tmp_path / "file.txt"
        _ = path.write_text(init)
        with yield_text_file(path):
            ...
        assert path.read_text() == init
