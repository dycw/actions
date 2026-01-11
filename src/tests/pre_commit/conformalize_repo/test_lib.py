from __future__ import annotations

from pytest import mark, param, raises
from utilities.text import strip_and_dedent

from actions.pre_commit.conformalize_repo.lib import (
    _add_envrc_uv_text,
    yield_python_versions,
)


class TestAddEnvrcUvText:
    def test_main(self) -> None:
        result = _add_envrc_uv_text()
        expected = strip_and_dedent("""
            # uv
            export UV_MANAGED_PYTHON='true'
            export UV_PRERELEASE='disallow'
            export UV_PYTHON='3.14'
            if ! command -v uv >/dev/null 2>&1; then
            \techo_date "ERROR: 'uv' not found" && exit 1
            fi
            activate='.venv/bin/activate'
            if [ -f $activate ]; then
            \t. $activate
            else
            \tuv venv
            fi
            uv sync --all-extras --all-groups --active --locked
        """)
        assert result == expected


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
