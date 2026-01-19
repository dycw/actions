from __future__ import annotations

from typing import TYPE_CHECKING

from utilities.pathlib import temp_cwd

from actions.pre_commit.conformalize_repo.lib import (
    add_coveragerc_toml,
    add_pytest_toml,
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
