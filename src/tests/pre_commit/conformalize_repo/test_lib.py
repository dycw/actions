from __future__ import annotations

from pytest import mark, param, raises
from utilities.text import strip_and_dedent

from actions.constants import YAML_INSTANCE
from actions.pre_commit.conformalize_repo.lib import (
    _add_envrc_uv_text,
    _add_pre_commit_config_repo,
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
            export UV_VENV_CLEAR=1
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


class TestAddPreCommitConfigRepo:
    def test_main(self) -> None:
        text = strip_and_dedent("""
            repos:
              - repo: url
                rev: rev
                hooks:
                  - id: id
                    args:
                      - --arg
        """)
        pre_commit_dict = YAML_INSTANCE.load(text)
        _add_pre_commit_config_repo(
            pre_commit_dict, "url", "id", args=("add", ["--arg"])
        )
        assert pre_commit_dict == YAML_INSTANCE.load(text)


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
