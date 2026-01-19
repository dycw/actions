from __future__ import annotations

from typing import TYPE_CHECKING

from hypothesis import given
from hypothesis.strategies import booleans, integers, none, sampled_from
from pytest import mark, param, raises
from typed_settings import Secret
from utilities.hypothesis import temp_paths, text_ascii
from utilities.pathlib import temp_cwd
from utilities.text import strip_and_dedent

from actions.constants import GITEA_PULL_REQUEST_YAML, GITHUB_PULL_REQUEST_YAML
from actions.pre_commit.conformalize_repo.lib import (
    _add_envrc_uv_text,
    add_ci_pull_request_yaml,
    add_ci_push_yaml,
    add_coveragerc_toml,
    add_envrc,
    add_pyproject_toml,
    add_pytest_toml,
    add_readme_md,
    yield_python_versions,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestAddCIPullRequestYaml:
    @given(
        root=temp_paths(),
        gitea=booleans(),
        certificates=booleans(),
        pre_commit=text_ascii() | none(),
        pre_commit__submodules=sampled_from(["true", "false"]) | none(),
        pyright=booleans(),
        pytest__macos=booleans(),
        pytest__ubuntu=booleans(),
        pytest__windows=booleans(),
        pytest__all_versions=booleans(),
        pytest__sops_age_key=text_ascii().map(Secret) | none(),
        pytest__timeout=integers() | none(),
        python_version=sampled_from([f"3.{i}" for i in range(1, 11)]),
        repo_name=text_ascii() | none(),
        ruff=booleans(),
        script=text_ascii() | none(),
        token_checkout=text_ascii().map(Secret) | none(),
        token_github=text_ascii().map(Secret) | none(),
        uv__native_tls=booleans(),
    )
    def test_main(
        self,
        *,
        root: Path,
        gitea: bool,
        certificates: bool,
        pre_commit: bool,
        pre_commit__submodules: str | None,
        pyright: bool,
        pytest__macos: bool,
        pytest__ubuntu: bool,
        pytest__windows: bool,
        pytest__all_versions: bool,
        pytest__sops_age_key: Secret[str] | None,
        pytest__timeout: int | None,
        python_version: str,
        repo_name: str | None,
        ruff: bool,
        script: str | None,
        token_checkout: Secret[str] | None,
        token_github: Secret[str] | None,
        uv__native_tls: bool,
    ) -> None:
        def run() -> None:
            add_ci_pull_request_yaml(
                gitea=gitea,
                certificates=certificates,
                pre_commit=pre_commit,
                pre_commit__submodules=pre_commit__submodules,
                pyright=pyright,
                pytest__macos=pytest__macos,
                pytest__ubuntu=pytest__ubuntu,
                pytest__windows=pytest__windows,
                pytest__all_versions=pytest__all_versions,
                pytest__sops_age_key=pytest__sops_age_key,
                pytest__timeout=pytest__timeout,
                python_version=python_version,
                repo_name=repo_name,
                ruff=ruff,
                script=script,
                token_checkout=token_checkout,
                token_github=token_github,
                uv__native_tls=uv__native_tls,
            )

        path = GITEA_PULL_REQUEST_YAML if gitea else GITHUB_PULL_REQUEST_YAML

        with temp_cwd(root):
            run()
            assert path.is_file()
            current = path.read_text()
            run()
            assert path.read_text() == current


class TestAddCIPushYaml:
    def test_main(self, *, tmp_path: Path) -> None:
        with temp_cwd(tmp_path):
            for _ in range(2):
                add_ci_push_yaml()


class TestAddCoverageRcToml:
    def test_main(self, *, tmp_path: Path) -> None:
        with temp_cwd(tmp_path):
            for _ in range(2):
                add_coveragerc_toml()


class TestAddEnvrc:
    def test_main(self, *, tmp_path: Path) -> None:
        with temp_cwd(tmp_path):
            for _ in range(2):
                add_envrc()


class TestAddEnvrcUvText:
    def test_main(self) -> None:
        result = _add_envrc_uv_text()
        expected = strip_and_dedent("""
            # uv
            export UV_MANAGED_PYTHON='true'
            export UV_PRERELEASE='disallow'
            export UV_PYTHON='3.14'
            export UV_RESOLUTION='highest'
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


class TestAddPyProjectToml:
    def test_main(self, *, tmp_path: Path) -> None:
        with temp_cwd(tmp_path):
            for _ in range(2):
                add_pyproject_toml()


class TestAddPytestToml:
    def test_main(self, *, tmp_path: Path) -> None:
        with temp_cwd(tmp_path):
            for _ in range(2):
                add_pytest_toml()


class TestAddReadMeMd:
    def test_main(self, *, tmp_path: Path) -> None:
        with temp_cwd(tmp_path):
            for _ in range(2):
                add_readme_md()


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
