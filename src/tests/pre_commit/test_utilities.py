from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from libcst import parse_statement
from pytest import mark, param
from utilities.iterables import one

from actions.pre_commit.utilities import (
    ensure_contains_partial_dict,
    get_partial_dict,
    get_partial_str,
    is_partial_dict,
    is_partial_str,
    yield_immutable_write_context,
    yield_mutable_write_context,
    yield_python_file,
    yield_text_file,
)

if TYPE_CHECKING:
    from pathlib import Path

    from actions.types import StrDict


class TestEnsureContainsPartialDict:
    def test_main(self) -> None:
        url = "https://github.com/owner/repo"
        repos: list[StrDict] = []
        for _ in range(2):
            result = ensure_contains_partial_dict(
                repos,
                {"repo": url, "rev": "v6.0.0"},
                extra={"hooks": [{"id": "id1"}, {"id": "id2"}]},
            )
            assert result == {
                "repo": url,
                "rev": "v6.0.0",
                "hooks": [{"id": "id1"}, {"id": "id2"}],
            }
            expected = [result]
            assert repos == expected


class TestEnsureContainsPartialStr:
    def test_main(self) -> None:
        url = "https://github.com/owner/repo"
        dependencies: list[StrDict] = []
        for _ in range(2):
            result = ensure_contains_partial_dict(
                dependencies,
                {"repo": url, "rev": "v6.0.0"},
                extra={"hooks": [{"id": "id1"}, {"id": "id2"}]},
            )
            assert result == {
                "repo": url,
                "rev": "v6.0.0",
                "hooks": [{"id": "id1"}, {"id": "id2"}],
            }
            expected = [result]
            assert dependencies == expected


class TestGetPartialDict:
    def test_main(self) -> None:
        url = "https://github.com/owner/repo"
        repos = [
            {"repo": url, "rev": "v6.0.0", "hooks": [{"id": "id1"}, {"id": "id2"}]}
        ]
        result = get_partial_dict(repos, {"repo": url})
        assert result == one(repos)


class TestGetPartialStr:
    def test_main(self) -> None:
        dependencies = ["dycw-utilities[test]>=1.2.3, <2"]
        result = get_partial_str(dependencies, "dycw-utilities[test]")
        assert result == one(dependencies)


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


class TestIsPartialStr:
    @mark.parametrize(
        ("obj", "text", "expected"),
        [
            param(None, "a", False),
            param("a", "a", True),
            param("a", "b", False),
            param("b", "a", False),
            param("abc", "a", True),
            param("a", "abc", False),
        ],
    )
    def test_main(self, *, obj: Any, text: str, expected: bool) -> None:
        assert is_partial_str(obj, text) is expected


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
    @mark.parametrize("init", [param("{}"), param("{}\n"), param("{}\n\n")])
    def test_modified(self, *, tmp_path: Path, init: str) -> None:
        path = tmp_path / "file.json"
        _ = path.write_text(init)
        with yield_mutable_write_context(path, json.loads, dict, json.dumps) as context:
            context["a"] = 1
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
            param("\n", "import abc\n"),
            param("\n\n", "import abc\n"),
        ],
    )
    def test_modified(self, *, tmp_path: Path, init: str, expected: str) -> None:
        path = tmp_path / "file.py"
        _ = path.write_text(init)
        with yield_python_file(path) as context:
            body = [*context.input.body, parse_statement("import abc")]
            context.output = context.input.with_changes(body=body)
        assert path.read_text() == expected

    @mark.parametrize("init", [param(""), param("\n"), param("\n\n")])
    def test_unmodified(self, *, tmp_path: Path, init: str) -> None:
        path = tmp_path / "file.py"
        _ = path.write_text(init)
        with yield_python_file(path):
            ...
        assert path.read_text() == init


class TestYieldTextFile:
    @mark.parametrize("init", [param("init"), param("init\n"), param("init\n\n")])
    def test_modified(self, *, tmp_path: Path, init: str) -> None:
        path = tmp_path / "file.txt"
        _ = path.write_text(init)
        with yield_text_file(path) as context:
            context.output = context.input.replace("init", "init\npost")
        expected = "init\npost\n"
        assert path.read_text() == expected

    @mark.parametrize("init", [param("init"), param("init\n"), param("init\n\n")])
    def test_unmodified(self, *, tmp_path: Path, init: str) -> None:
        path = tmp_path / "file.txt"
        _ = path.write_text(init)
        with yield_text_file(path):
            ...
        assert path.read_text() == init
