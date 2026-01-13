from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import mark, param
from utilities.packaging import Requirement
from utilities.text import strip_and_dedent

from actions.pre_commit.update_requirements.classes import Version2, Version3
from actions.pre_commit.update_requirements.lib import _format_path
from actions.utilities import are_equal_modulo_new_line

if TYPE_CHECKING:
    from pathlib import Path

    from actions.pre_commit.update_requirements.classes import Version2or3, VersionSet


class TestFormatPath:
    @mark.parametrize(
        ("input_", "latest", "output"),
        [
            param("package", None, "package"),
            param("package", Version2(1, 2), "package>=1.2, <2"),
            param("package", Version3(1, 2, 3), "package>=1.2.3, <2"),
            param("package>=1.2", None, "package>=1.2"),
            param("package>=1.2", Version2(1, 2), "package>=1.2"),
            param("package>=1.2", Version2(1, 3), "package>=1.3"),
            param("package>=1.2.3", None, "package>=1.2.3"),
            param("package>=1.2.3", Version3(1, 2, 3), "package>=1.2.3"),
            param("package>=1.2.3", Version3(1, 2, 4), "package>=1.2.4"),
            param("package<2", None, "package<2"),
            param("package<2", Version2(1, 2), "package<2"),
            param("package<2", Version2(2, 3), "package<3"),
            param("package<1.3", None, "package<1.3"),
            param("package<1.3", Version3(1, 2, 3), "package<1.3"),
            param("package<1.3", Version3(1, 3, 0), "package<1.4"),
            param("package>=1.2, <2", None, "package>=1.2, <2"),
            param("package>=1.2, <2", Version2(1, 2), "package>=1.2, <2"),
            param("package>=1.2, <2", Version2(1, 3), "package>=1.3, <2"),
            param("package>=1.2.3, <1.3", None, "package>=1.2.3, <2"),
            param("package>=1.2.3, <1.3", Version3(1, 2, 3), "package>=1.2.3, <2"),
            param("package>=1.2.3, <1.3", Version3(1, 2, 4), "package>=1.2.4, <2"),
            param("package>=1.2.3, <2", None, "package>=1.2.3, <2"),
            param("package>=1.2.3, <2", Version3(1, 2, 3), "package>=1.2.3, <2"),
            param("package>=1.2.3, <2", Version3(1, 2, 4), "package>=1.2.4, <2"),
            param("package[extra]>=1.2.3, <1.3", None, "package[extra]>=1.2.3, <2"),
            param(
                "package[extra]>=1.2.3, <1.3",
                Version3(1, 2, 3),
                "package[extra]>=1.2.3, <2",
            ),
            param(
                "package[extra]>=1.2.3, <1.3",
                Version3(1, 2, 4),
                "package[extra]>=1.2.4, <2",
            ),
        ],
    )
    def test_main(
        self, *, tmp_path: Path, input_: str, latest: Version2or3 | None, output: str
    ) -> None:
        path = tmp_path / "file.toml"
        full_input = strip_and_dedent(f"""
            [project]
              dependencies = ["{input_}"]
        """)
        _ = path.write_text(full_input)
        req = Requirement(input_)
        version_set: VersionSet = {}
        if latest is not None:
            version_set[req.name] = latest
        expected = strip_and_dedent(f"""
            [project]
              dependencies = ["{output}"]
        """)
        changed = input_ != output
        for i in range(2):
            modifications: set[Path] = set()
            _format_path(path, versions=version_set, modifications=modifications)
            result = path.read_text()
            assert are_equal_modulo_new_line(result, expected)
            assert len(modifications) == (int(changed) if i == 0 else 0)
