from __future__ import annotations

from typing import TYPE_CHECKING

import utilities.click
from click import argument, option
from utilities.click import Str
from utilities.core import is_pytest
from utilities.logging import basic_config

from actions.logging import LOGGER
from actions.re_encrypt.lib import re_encrypt

if TYPE_CHECKING:
    from utilities.pydantic import SecretLike
    from utilities.types import PathLike


@argument("path", type=utilities.click.Path(exist="existing file"))
@option(
    "--key-file",
    type=utilities.click.Path(exist="file if exists"),
    default=None,
    help="The key file",
)
@option("--key", type=Str(), default=None, help="The age identity")
@option(
    "--new-key-file",
    type=utilities.click.Path(exist="file if exists"),
    default=None,
    help="The new key file for encryption",
)
@option(
    "--new-key", type=Str(), default=None, help="The new age identity for encryption"
)
def re_encrypt_sub_cmd(
    *,
    path: PathLike,
    key_file: PathLike | None = None,
    key: SecretLike | None = None,
    new_key_file: PathLike | None = None,
    new_key: SecretLike | None = None,
) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    re_encrypt(
        path, key_file=key_file, key=key, new_key_file=new_key_file, new_key=new_key
    )


__all__ = ["re_encrypt_sub_cmd"]
