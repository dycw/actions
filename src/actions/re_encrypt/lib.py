from __future__ import annotations

from contextlib import contextmanager
from os import environ
from pathlib import Path
from typing import TYPE_CHECKING, assert_never

from typed_settings import Secret
from utilities.core import TemporaryFile, write_text, yield_temp_environ
from utilities.subprocess import run
from utilities.tabulate import func_param_desc
from xdg_base_dirs import xdg_config_home

from actions import __version__
from actions.logging import LOGGER
from actions.re_encrypt.settings import SETTINGS

if TYPE_CHECKING:
    from collections.abc import Iterator

    from utilities.types import PathLike


def re_encrypt(
    path: PathLike,
    /,
    *,
    key_file: PathLike | None = SETTINGS.key_file,
    key: Secret[str] | None = SETTINGS.key,
    new_key_file: PathLike | None = SETTINGS.new_key_file,
    new_key: Secret[str] | None = SETTINGS.new_key,
) -> None:
    """Re-encrypt a JSON file."""
    LOGGER.info(
        func_param_desc(
            re_encrypt,
            __version__,
            f"{path=}",
            f"{key_file=}",
            f"{key=}",
            f"{new_key_file=}",
            f"{new_key=}",
        )
    )
    with _yield_env(key_file=key_file, key=key):
        decrypted = run(
            "sops",
            "decrypt",
            "--input-type",
            "json",
            "--output-type",
            "json",
            "--ignore-mac",
            str(path),
            return_=True,
        )
    with _yield_env(key_file=new_key_file, key=new_key):
        identity = _get_recipient()
    with TemporaryFile(text=decrypted) as temp:
        encrypted = run(
            "sops",
            "encrypt",
            "--age",
            identity,
            "--input-type",
            "json",
            "--output-type",
            "json",
            str(temp),
            return_=True,
        )
    write_text(path, encrypted, overwrite=True)
    LOGGER.info("Finished re-encrypting '%s'", path)


@contextmanager
def _yield_env(
    *,
    key_file: PathLike | None = SETTINGS.key_file,
    key: Secret[str] | None = SETTINGS.key,
) -> Iterator[None]:
    match key_file, key:
        case Path() | str(), _:
            with yield_temp_environ(SOPS_AGE_KEY_FILE=str(key_file)):
                yield
        case None, Secret():
            with yield_temp_environ(SOPS_AGE_KEY=key.get_secret_value()):
                yield
        case None, None:
            path = xdg_config_home() / "sops/age/keys.txt"
            with yield_temp_environ(SOPS_AGE_KEY_FILE=str(path)):
                yield
        case never:
            assert_never(never)


def _get_recipient() -> str:
    try:
        key_file = environ["SOPS_AGE_KEY_FILE"]
    except KeyError:
        with TemporaryFile(text=environ["SOPS_AGE_KEY"]) as temp:
            return _get_recipient_from_path(temp)
    else:
        return _get_recipient_from_path(key_file)


def _get_recipient_from_path(path: PathLike, /) -> str:
    recipient, *_ = run("age-keygen", "-y", str(path), return_=True).splitlines()
    return recipient


__all__ = ["re_encrypt"]
