from __future__ import annotations

from re import IGNORECASE, search
from typing import TYPE_CHECKING

from github import Github
from github.Auth import Token
from requests import get
from utilities.iterables import one
from utilities.text import strip_and_dedent

from actions import __version__
from actions.logging import LOGGER
from actions.sops.settings import SOPS_SETTINGS

if TYPE_CHECKING:
    from pathlib import Path

    from typed_settings import Secret

    from actions.types import StrDict


def setup_sops(
    *,
    token: Secret[str] | None = SOPS_SETTINGS.token,
    system: str = SOPS_SETTINGS.system,
    machine: str = SOPS_SETTINGS.machine,
    path_binary: Path = SOPS_SETTINGS.path_binary,
    timeout: int = SOPS_SETTINGS.timeout,
    chunk_size: int = SOPS_SETTINGS.chunk_size,
) -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - token       = %s
             - system      = %s
             - machine     = %s
             - path_binary = %s
             - timeout     = %d
             - chunk_size  = %d
        """),
        setup_sops.__name__,
        __version__,
        token,
        system,
        machine,
        path_binary,
        timeout,
        chunk_size,
    )
    gh = Github(auth=None if token is None else Token(token.get_secret_value()))
    repo = gh.get_repo("getsops/sops")
    release = repo.get_latest_release()
    if system not in {"Darwin", "Linux"}:
        msg = f"Invalid system {system!r}"
        raise ValueError(msg)
    asset = one(
        a
        for a in release.get_assets()
        if search(system, a.name, flags=IGNORECASE)
        and search(machine, a.name, flags=IGNORECASE)
        and not a.name.endswith("json")
    )
    headers: StrDict = {}
    if token is not None:
        headers["Authorization"] = f"Bearer {token.get_secret_value()}"
    with get(
        asset.browser_download_url, headers=headers, timeout=timeout, stream=True
    ) as resp:
        resp.raise_for_status()
        path_binary.parent.mkdir(parents=True, exist_ok=True)
        with path_binary.open(mode="wb") as fh:
            fh.writelines(resp.iter_content(chunk_size=chunk_size))
    path_binary.chmod(0o755)


__all__ = ["setup_sops"]
