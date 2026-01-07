from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from pytest import mark, param, raises
from utilities.iterables import one
from utilities.text import strip_and_dedent

from actions.pre_commit.conformalize_repo.lib import (
    _add_envrc_uv_text,
    get_partial_dict,
    is_partial_dict,
    yield_python_versions,
    yield_write_context,
)

if TYPE_CHECKING:
    from pathlib import Path

    from actions.types import StrDict


class TestAddEnvrcUvText:
    def test_main(self) -> None:
        result = _add_envrc_uv_text()
        expected = strip_and_dedent("""
            # uv
            export UV_MANAGED_PYTHON='true'
            export UV_PRERELEASE='disallow'
            export UV_PYTHON='3.14'
            if ! command -v uv >/dev/null 2>&1; then
                echo_date "ERROR: 'uv' not found" && exit 1
            fi
            activate='.venv/bin/activate'
            if [ -f $activate ]; then
                . $activate
            else
                uv venv
            fi
            uv sync --all-extras --all-groups --active --locked
        """)
        assert result == expected


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


class TestYieldPythonVersions:
    @mark.parametrize(
        ("version", "expected"),
        [
            param("3.12", ["3.12", "3.13", "3.14"]),
            param("3.13", ["3.13", "3.14"]),
            param("3.14", ["3.14"]),
        ],
    )
    def test_main(self, *, version: str, expected: list[str]) -> None:
        assert list(yield_python_versions(version)) == expected

    def test_error_major(self) -> None:
        with raises(ValueError, match="Major versions must be equal; got 2 and 3"):
            _ = list(yield_python_versions("2.0"))

    def test_error_minor(self) -> None:
        with raises(ValueError, match="Minor version must be at most 14; got 15"):
            _ = list(yield_python_versions("3.15"))


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
