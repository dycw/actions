from __future__ import annotations

from subprocess import check_call

from utilities.pathlib import get_repo_root


class TestCLI:
    def test_main(self) -> None:
        _ = check_call(["action", "--dry-run"], cwd=get_repo_root())
