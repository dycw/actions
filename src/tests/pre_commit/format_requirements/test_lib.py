from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import mark, param
from utilities.text import strip_and_dedent

from actions.pre_commit.format_requirements.lib import _format_path
from actions.utilities import are_equal_modulo_new_line

if TYPE_CHECKING:
    from pathlib import Path


class TestFormatPath:
    @mark.parametrize(
        ("input_", "output"),
        [
            param("package", "package"),
            param("package>=1.2.3", "package>=1.2.3"),
            param("package  >=  1.2.3", "package>=1.2.3"),
            param("package<1.2", "package<1.2"),
            param("package  <  1.2", "package<1.2"),
            param("package>=1.2.3,<1.3", "package>=1.2.3, <1.3"),
            param("package  >=  1.2.3  ,  <  1.3", "package>=1.2.3, <1.3"),
            param("package<1.3,>=1.2.3", "package>=1.2.3, <1.3"),
            param("package[extra]", "package[extra]"),
            param("package[extra]>=1.2.3", "package[extra]>=1.2.3"),
            param("package[extra]  >=  1.2.3", "package[extra]>=1.2.3"),
        ],
    )
    def test_main(self, *, tmp_path: Path, input_: str, output: str) -> None:
        path = tmp_path / "file.toml"
        full_input = strip_and_dedent(f"""
            [project]
              dependencies = ["{input_}"]
        """)
        _ = path.write_text(full_input)
        expected = strip_and_dedent(f"""
            [project]
              dependencies = ["{output}"]
        """)
        changed = input_ != output
        for i in range(2):
            modifications: set[Path] = set()
            _format_path(path, modifications=modifications)
            result = path.read_text()
            assert are_equal_modulo_new_line(result, expected)
            assert len(modifications) == (int(changed) if i == 0 else 0)
