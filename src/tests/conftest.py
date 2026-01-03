from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import fixture
from utilities.hypothesis import setup_hypothesis_profiles
from utilities.importlib import files

if TYPE_CHECKING:
    from pathlib import Path

setup_hypothesis_profiles()


@fixture
def path_tests() -> Path:
    path = files(anchor="tests")
    if not path.is_dir():
        raise NotADirectoryError(path)
    return path
