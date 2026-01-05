from __future__ import annotations

from pathlib import Path
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
    from typed_settings import Secret


def setup_sops(
    *,
    token: Secret[str] | None = SOPS_SETTINGS.token,
    system: str = SOPS_SETTINGS.system,
    platform: str = SOPS_SETTINGS.platform,
) -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - token    = %s
             - system   = %s
             - platform = %s
        """),
        setup_sops.__name__,
        __version__,
        token,
        system,
        platform,
    )
    if token is None:
        msg = "'token' must be given"
        raise ValueError(msg)
    gh = Github(auth=Token(token.get_secret_value()))
    repo = gh.get_repo("getsops/sops")
    release = repo.get_latest_release()
    if system not in {"Darwin", "Linux"}:
        msg = f"Invalid system {system!r}"
        raise ValueError(msg)
    asset = one(
        a
        for a in release.get_assets()
        if search(system, a.name, flags=IGNORECASE)
        and search(platform, a.name, flags=IGNORECASE)
    )
    path = Path("/usr/local/bin")
    with get(
        asset.browser_download_url,
        headers={"Authorization": f"Bearer {token.get_secret_value()}"},
        timeout=60,
        stream=True,
    ) as resp:
        resp.raise_for_status()
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open(mode="wb") as fh:
            fh.writelines(resp.iter_content(chunk_size=8192))
    path.chmod(0o755)


__all__ = ["setup_sops"]
