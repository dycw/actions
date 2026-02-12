from __future__ import annotations

from typing import TYPE_CHECKING

import utilities.click
from click import Command, argument, command, option
from utilities.click import CONTEXT_SETTINGS, Str
from utilities.core import is_pytest, set_up_logging
from utilities.types import PathLike

from actions.re_encrypt.lib import re_encrypt

if TYPE_CHECKING:
    from collections.abc import Callable

    from utilities.types import PathLike, SecretLike


RE_ENCRYPT_SUB_CMD = "re-encrypt"


def make_re_encrypt_cmd(
    *, cli: Callable[..., Command] = command, name: str | None = None
) -> Command:
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
        help="The new key file for encryption, if different",
    )
    @option(
        "--new-key",
        type=Str(),
        default=None,
        help="The new age identity for encryption, if different",
    )
    def func(
        *,
        path: PathLike,
        key_file: PathLike | None = None,
        key: SecretLike | None = None,
        new_key_file: PathLike | None = None,
        new_key: SecretLike | None = None,
    ) -> None:
        if is_pytest():
            return
        set_up_logging(__name__, root=True)
        re_encrypt(
            path, key_file=key_file, key=key, new_key_file=new_key_file, new_key=new_key
        )

    return cli(name=name, help="Re-encrypt a JSON file", **CONTEXT_SETTINGS)(func)


cli = make_re_encrypt_cmd()


__all__ = ["RE_ENCRYPT_SUB_CMD", "cli", "make_re_encrypt_cmd"]
