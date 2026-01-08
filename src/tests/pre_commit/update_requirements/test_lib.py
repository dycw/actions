from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import mark, param
from utilities.packaging import Requirement
from utilities.text import strip_and_dedent

from actions.update_requirements.classes import Version2, Version3, Versions, VersionSet
from actions.update_requirements.lib import _format_path
from actions.utilities import are_equal_modulo_new_line

if TYPE_CHECKING:
    from pathlib import Path


class TestFormatPath:
    @mark.parametrize(
        ("input_", "versions", "output"),
        [
            param("package", Versions(), "package"),
            param(
                "package>=1.2", Versions(pyproject_lower=Version2(1, 2)), "package>=1.2"
            ),
            param(
                "package>=1.2",
                Versions(pyproject_lower=Version2(1, 2), latest=Version2(1, 2)),
                "package>=1.2",
            ),
            param(
                "package>=1.2",
                Versions(pyproject_lower=Version2(1, 2), latest=Version2(1, 3)),
                "package>=1.3",
            ),
            param(
                "package>=1.2.3",
                Versions(pyproject_lower=Version3(1, 2, 3)),
                "package>=1.2.3",
            ),
            param(
                "package>=1.2.3",
                Versions(pyproject_lower=Version3(1, 2, 3), latest=Version3(1, 2, 3)),
                "package>=1.2.3",
            ),
            param(
                "package>=1.2.3",
                Versions(pyproject_lower=Version3(1, 2, 3), latest=Version3(1, 2, 4)),
                "package>=1.2.4",
            ),
            param("package<2", Versions(pyproject_upper=2), "package<2"),
            param(
                "package<2",
                Versions(pyproject_upper=2, latest=Version2(1, 2)),
                "package<2",
            ),
            param(
                "package<2",
                Versions(pyproject_upper=2, latest=Version2(2, 3)),
                "package<3",
            ),
            param(
                "package<1.3", Versions(pyproject_upper=Version2(1, 3)), "package<1.3"
            ),
            param(
                "package<1.3",
                Versions(pyproject_upper=Version2(1, 3), latest=Version3(1, 2, 3)),
                "package<1.3",
            ),
            param(
                "package<1.3",
                Versions(pyproject_upper=Version2(1, 3), latest=Version3(1, 3, 0)),
                "package<1.4",
            ),
            param(
                "package>=1.2, <2",
                Versions(pyproject_lower=Version2(1, 2), pyproject_upper=2),
                "package>=1.2, <2",
            ),
            param(
                "package>=1.2, <2",
                Versions(
                    pyproject_lower=Version2(1, 2),
                    pyproject_upper=2,
                    latest=Version2(1, 2),
                ),
                "package>=1.2, <2",
            ),
            param(
                "package>=1.2, <2",
                Versions(
                    pyproject_lower=Version2(1, 2),
                    pyproject_upper=2,
                    latest=Version2(1, 3),
                ),
                "package>=1.3, <2",
            ),
            param(
                "package>=1.2.3, <1.3",
                Versions(
                    pyproject_lower=Version3(1, 2, 3), pyproject_upper=Version2(1, 3)
                ),
                "package>=1.2.3, <2",
            ),
            param(
                "package>=1.2.3, <1.3",
                Versions(
                    pyproject_lower=Version3(1, 2, 3),
                    pyproject_upper=Version2(1, 3),
                    latest=Version3(1, 2, 3),
                ),
                "package>=1.2.3, <2",
            ),
            param(
                "package>=1.2.3, <1.3",
                Versions(
                    pyproject_lower=Version3(1, 2, 3),
                    pyproject_upper=Version2(1, 3),
                    latest=Version3(1, 2, 4),
                ),
                "package>=1.2.4, <2",
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
