from __future__ import annotations

from typing import TYPE_CHECKING

from hypothesis import given
from hypothesis.strategies import booleans, integers, none, sampled_from
from pytest import mark, param, raises
from typed_settings import Secret
from utilities.hypothesis import temp_paths, text_ascii
from utilities.pathlib import temp_cwd

from actions.constants import GITEA_PULL_REQUEST_YAML, GITHUB_PULL_REQUEST_YAML
from actions.pre_commit.conformalize_repo.lib import (
    add_coveragerc_toml,
    add_pytest_toml,
    yield_python_versions,
)

if TYPE_CHECKING:
    from pathlib import Path


class TestAddCoverageRcToml:
    def test_main(self, *, tmp_path: Path) -> None:
        with temp_cwd(tmp_path):
            for _ in range(2):
                add_coveragerc_toml()


class TestAddPytestToml:
    def test_main(self, *, tmp_path: Path) -> None:
        with temp_cwd(tmp_path):
            for _ in range(2):
                add_pytest_toml()
