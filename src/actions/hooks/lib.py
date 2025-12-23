from __future__ import annotations

from pathlib import Path
from re import search
from subprocess import CalledProcessError
from typing import TYPE_CHECKING, Any

from utilities.functions import ensure_class, ensure_str
from utilities.text import strip_and_dedent
from yaml import safe_load

from actions import __version__
from actions.hooks.settings import HOOKS_SETTINGS
from actions.logging import LOGGER
from actions.utilities import log_run

if TYPE_CHECKING:
    from collections.abc import Iterator


def run_hooks(
    *,
    repos: list[str] | None = HOOKS_SETTINGS.repos,
    hooks: list[str] | None = HOOKS_SETTINGS.hooks,
) -> None:
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
             - repos = %s
             - hooks = %s
        """),
        run_hooks.__name__,
        __version__,
        repos,
        hooks,
    )
    results = {hook: _run_hook(hook) for hook in _yield_hooks(repos=repos, hooks=hooks)}
    failed = {hook: result for hook, result in results.items() if not result}
    if len(failed) >= 1:
        msg = f"Failed hook(s): {', '.join(failed)}"
        raise RuntimeError(msg)


def _yield_hooks(
    *,
    repos: list[str] | None = HOOKS_SETTINGS.repos,
    hooks: list[str] | None = HOOKS_SETTINGS.hooks,
) -> Iterator[str]:
    dict_ = safe_load(Path(".pre-commit-config.yaml").read_text())
    repos_list = ensure_class(dict_["repos"], list)
    for repo in (ensure_class(r, dict) for r in repos_list):
        url = repo["repo"]
        if (repos is not None) and any(search(repo_i, url) for repo_i in repos):
            yield from _yield_repo_hooks(repo)
        elif hooks is not None:
            for hook in _yield_repo_hooks(repo):
                if any(search(hook_i, hook) for hook_i in hooks):
                    yield hook


def _yield_repo_hooks(repo: dict[str, Any], /) -> Iterator[str]:
    hooks = ensure_class(repo["hooks"], list)
    for hook in (ensure_class(r, dict) for r in hooks):
        yield ensure_str(hook["id"])


def _run_hook(hook: str, /) -> bool:
    LOGGER.info("Running '%s'...", hook)
    try:
        log_run("pre-commit", "run", "--verbose", "--all-files", hook, print=True)
    except CalledProcessError:
        return False
    return True


__all__ = ["run_hooks"]
