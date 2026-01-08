from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import fixture, mark, param
from utilities.iterables import _sort_iterable_cmp
from utilities.packaging import Requirement
from utilities.text import strip_and_dedent

from actions.pre_commit.update_requirements.classes import (
    Version2,
    Version3,
    Versions,
    VersionSet,
)
from actions.pre_commit.update_requirements.lib import _format_path
from actions.utilities import are_equal_modulo_new_line

if TYPE_CHECKING:
    from pathlib import Path


@fixture
def input_() -> str:
    return strip_and_dedent("""
[project]
  dependencies = [
    "unbounded",
    "lower-unchanged1 >=1.2.3",
    "lower-unchanged2 >=1.2.3",
    "lower-changed >=1.2.3",
    "upper-unchanged1 <1.3",
    "upper-unchanged2 <1.3",
    "upper-changed <1.3",
  ]
""")

    # "lower-and-upper-unchanged1 >=1.2.3, <1.3",
    # "lower-and-upper-unchanged1 >=1.2.3, <1.3",
    # "lower-and-upper-unchanged2 >=1.2.3, <1.3",
    # "lower-and-upper-changed1 >=1.2.3, <1.3",
    # "lower-and-upper-changed2 >=1.2.3, <9.9",


@fixture
def output() -> str:
    return strip_and_dedent(
        """
[project]
  dependencies = ["unbounded", "lower-unchanged1>=1.2.3", "lower-unchanged2>=1.2.3", "lower-changed>=1.2.4", "upper-unchanged1<1.3", "upper-unchanged2<1.3", "upper-changed<1.4"]
""",
        trailing=True,
    )


# dependencies = ["unbounded", "lower-unchanged1>=1.2.3", "lower-unchanged2>=1.2.3", "lower-changed>=1.2.4", "upper-unchanged1<1.3", "upper-unchanged2<1.3", "upper-changed<1.4", "lower-and-upper1>=1.2.3, <1.3", "lower-and-upper2>=1.2.3, <1.3", "lower-and-upper3>=1.2.3, <1.3", "with-extra[extra1]", "with-extra[extra2]>=1.2.3", "with-extra[extra3]>=1.2.3"]


class TestFormatPath:
    @mark.parametrize(
        ("input_", "versions", "output"),
        [
            param("unbounded", Versions(), "unbounded"),
            param(
                "lower>=1.2.3",
                Versions(pyproject_lower=Version3(1, 2, 3)),
                "lower>=1.2.3",
            ),
            param(
                "lower>=1.2.3",
                Versions(pyproject_lower=Version3(1, 2, 3), latest=Version3(1, 2, 3)),
                "lower>=1.2.3",
            ),
            param(
                "lower>=1.2.3",
                Versions(pyproject_lower=Version3(1, 2, 3), latest=Version3(1, 2, 4)),
                "lower>=1.2.4",
            ),
            param(
                "lower>=1.2.3",
                Versions(pyproject_lower=Version3(1, 2, 3), latest=Version3(1, 3, 0)),
                "lower>=1.3.0",
            ),
            param("upper<1.3", Versions(pyproject_upper=Version2(1, 3)), "upper<1.3"),
            param(
                "upper<1.3",
                Versions(pyproject_upper=Version2(1, 3), latest=Version3(1, 2, 3)),
                "upper<1.3",
            ),
            param(
                "upper<1.3",
                Versions(pyproject_upper=Version2(1, 3), latest=Version3(1, 2, 999)),
                "upper<1.3",
            ),
            param(
                "upper<1.3",
                Versions(pyproject_upper=Version2(1, 3), latest=Version3(1, 3, 0)),
                "upper<1.4",
            ),
            param(
                "lower>=1.2.3, <1.3",
                Versions(
                    pyproject_lower=Version3(1, 2, 3), pyproject_upper=Version2(1, 3)
                ),
                "lower>=1.2.3, <2",
                marks=mark.only,
            ),
            param(
                "lower>=1.2.3, <1.3",
                Versions(
                    pyproject_lower=Version3(1, 2, 3),
                    pyproject_upper=Version2(1, 3),
                    latest=Version3(1, 2, 3),
                ),
                "lower>=1.2.3, <2",
            ),
        ],
    )
    def test_main(
        self, *, tmp_path: Path, input_: str, versions: Versions, output: str
    ) -> None:
        path = tmp_path / "file.toml"
        full_input = strip_and_dedent(f"""
            [project]
              dependencies = ["{input_}"]
        """)
        _ = path.write_text(full_input)
        # versions: VersionSet = {
        #     "lower-and-upper-unchanged1": Versions(
        #         pyproject_lower=Version3(1, 2, 3), pyproject_upper=Version2(1, 3)
        #     ),
        #     "lower-and-upper-unchanged2": Versions(
        #         pyproject_lower=Version3(1, 2, 3),
        #         pyproject_upper=Version2(1, 3),
        #         latest=Version3(1, 2, 3),
        #     ),
        #     "lower-and-upper-changed1": Versions(
        #         pyproject_lower=Version3(1, 2, 3),
        #         pyproject_upper=Version2(1, 3),
        #         latest=Version3(1, 2, 4),
        #     ),
        #     "lower-and-upper-changed2": Versions(
        #         pyproject_lower=Version3(1, 2, 3),
        #         pyproject_upper=Version2(9, 9),
        #         latest=Version3(1, 2, 3),
        #     ),
        # }
        req = Requirement.new(input_)
        version_set: VersionSet = {req.name: versions}
        expected = strip_and_dedent(
            f"""
                [project]
                  dependencies = ["{output}"]
            """
        )
        changed = input_ != output
        for i in range(2):
            modifications: set[Path] = set()
            _format_path(path, versions=version_set, modifications=modifications)
            result = path.read_text()
            assert are_equal_modulo_new_line(result, expected)
            assert len(modifications) == (int(changed) if i == 0 else 0)
