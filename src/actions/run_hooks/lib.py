from __future__ import annotations

from contextlib import suppress
from re import search
from subprocess import CalledProcessError
from typing import TYPE_CHECKING

import utilities.time
from utilities.functions import ensure_str, get_func_name
from utilities.tabulate import func_param_desc
from whenever import TimeDelta
from yaml import safe_load

from actions import __version__
from actions.constants import PRE_COMMIT_CONFIG_YAML
from actions.logging import LOGGER
from actions.pre_commit.utilities import get_list_dicts
from actions.run_hooks.settings import SETTINGS
from actions.utilities import logged_run

if TYPE_CHECKING:
    from collections.abc import Iterator

    from utilities.types import StrDict


def run_hooks(
    *,
    repos: list[str] | None = SETTINGS.repos,
    hooks: list[str] | None = SETTINGS.hooks,
    hooks_exclude: list[str] | None = SETTINGS.hooks_exclude,
    sleep: int = SETTINGS.sleep,
) -> None:
    LOGGER.info(
        func_param_desc(
            run_hooks,
            __version__,
            f"{repos=}",
            f"{hooks=}",
            f"{hooks_exclude=}",
            f"{sleep=}",
        )
    )
    results = {
        hook: _run_hook(hook, sleep=sleep)
        for hook in _yield_hooks(repos=repos, hooks=hooks, hooks_exclude=hooks_exclude)
    }
    failed = {hook: result for hook, result in results.items() if not result}
    if len(failed) >= 1:
        msg = f"Failed hook(s): {', '.join(failed)}"
        raise RuntimeError(msg)
    LOGGER.info("Finished running %r", get_func_name(run_hooks))


def _yield_hooks(
    *,
    repos: list[str] | None = SETTINGS.repos,
    hooks: list[str] | None = SETTINGS.hooks,
    hooks_exclude: list[str] | None = SETTINGS.hooks_exclude,
) -> Iterator[str]:
    dict_ = safe_load(PRE_COMMIT_CONFIG_YAML.read_text())
    repos_list = get_list_dicts(dict_, "repos")
    results: set[str] = set()
    for repo in repos_list:
        url = repo["repo"]
        if (repos is not None) and any(search(repo_i, url) for repo_i in repos):
            results.update(_yield_repo_hooks(repo))
        elif hooks is not None:
            for hook in _yield_repo_hooks(repo):
                if any(search(hook_i, hook) for hook_i in hooks):
                    results.add(hook)
    if hooks_exclude is not None:
        for hook in hooks_exclude:
            with suppress(KeyError):
                results.remove(hook)
    yield from sorted(results)


def _yield_repo_hooks(repo: StrDict, /) -> Iterator[str]:
    for hook in get_list_dicts(repo, "hooks"):
        yield ensure_str(hook["id"])


def _run_hook(hook: str, /, *, sleep: int = SETTINGS.sleep) -> bool:
    LOGGER.info("Running '%s'...", hook)
    try:
        logged_run("pre-commit", "run", "--verbose", "--all-files", hook, print=True)
    except CalledProcessError:
        is_success = False
    else:
        is_success = True
    delta = TimeDelta(seconds=sleep)
    LOGGER.info(
        "Hook '%s' %s; sleeping for %s...",
        hook,
        "succeeded" if is_success else "failed",
        delta,
    )
    utilities.time.sleep(sleep)
    LOGGER.info("Finished sleeping for %s", delta)
    return is_success


__all__ = ["run_hooks"]
