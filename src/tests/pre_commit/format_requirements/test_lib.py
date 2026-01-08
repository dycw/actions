from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import fixture, mark, param
from pytest_lazy_fixtures import lf
from utilities.text import strip_and_dedent

from actions.pre_commit.format_requirements.lib import _format_path

if TYPE_CHECKING:
    from pathlib import Path


@fixture
def input_dependencies() -> str:
    return strip_and_dedent("""
[project]
  dependencies = [
    "unbounded",
    "lower1>=1.2.3",
    "lower2    >=    1.2.3",
    "upper1<1.3",
    "upper2    <    1.3",
    "lower-and-upper1>=1.2.3,<1.3",
    "lower-and-upper2<1.3,>=1.2.3",
    "lower-and-upper3    >=    1.2.3    ,    <1.3",
    "with-extra[extra1]",
    "with-extra[extra2]>=1.2.3",
    "with-extra[extra3]    >=    1.2.3",
  ]
""")


@fixture
def output_dependencies() -> str:
    return strip_and_dedent(
        """
[project]
  dependencies = ["unbounded", "lower1 >=1.2.3", "lower2 >=1.2.3", "upper1 <1.3", "upper2 <1.3", "lower-and-upper1 >=1.2.3, <1.3", "lower-and-upper2 >=1.2.3, <1.3", "lower-and-upper3 >=1.2.3, <1.3", "with-extra[extra1]", "with-extra[extra2] >=1.2.3", "with-extra[extra3] >=1.2.3"]
""",
        trailing=True,
    )


##


@fixture
def input_optional_deps() -> str:
    return strip_and_dedent("""
[project.optional-dependencies]
  group = [
    "unbounded",
    "lower>=1.2.3",
    "upper<1.3",
    "lower-and-upper1>=1.2.3,<1.3",
  ]
""")


@fixture
def output_optional_deps() -> str:
    return strip_and_dedent(
        """
[project.optional-dependencies]
  group = ["unbounded", "lower >=1.2.3", "upper <1.3", "lower-and-upper1 >=1.2.3, <1.3"]
""",
        trailing=True,
    )


##


@fixture
def input_dep_groups() -> str:
    return strip_and_dedent("""
[dependency-groups]
  group = [
    "unbounded",
    "lower>=1.2.3",
    "upper<1.3",
    "lower-and-upper1>=1.2.3,<1.3",
  ]
""")


@fixture
def output_dep_groups() -> str:
    return strip_and_dedent(
        """
[dependency-groups]
  group = ["unbounded", "lower >=1.2.3", "upper <1.3", "lower-and-upper1 >=1.2.3, <1.3"]
""",
        trailing=True,
    )


class TestFormatPath:
    @mark.parametrize(
        ("input_", "output"),
        [
            param(lf("input_dependencies"), lf("output_dependencies")),
            param(lf("input_optional_deps"), lf("output_optional_deps")),
            param(lf("input_dep_groups"), lf("output_dep_groups")),
        ],
    )
    def test_main(self, *, tmp_path: Path, input_: str, output: str) -> None:
        path = tmp_path / "file.toml"
        _ = path.write_text(input_)
        for i in range(2):
            modifications: set[Path] = set()
            _format_path(path, modifications=modifications)
            result = path.read_text()
            assert result == output
            assert len(modifications) == (1 if i == 0 else 0)
