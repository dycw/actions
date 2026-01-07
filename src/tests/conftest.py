from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import fixture
from utilities.hypothesis import setup_hypothesis_profiles
from utilities.importlib import files

if TYPE_CHECKING:
    from pathlib import Path

setup_hypothesis_profiles()


@fixture
def tests_pre_commit() -> Path:
    path = files(anchor="tests") / "pre_commit"
    if not path.is_dir():
        raise NotADirectoryError(path)
    return path
