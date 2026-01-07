from __future__ import annotations

from pathlib import Path

import click
from click import argument

path_argument = argument(
    "paths",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
)


__all__ = ["path_argument"]
