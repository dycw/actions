from __future__ import annotations

from contextlib import suppress
from subprocess import CalledProcessError

from utilities.version import parse_version

from actions.logging import LOGGER
from actions.tag_commit.settings import SETTINGS
from actions.utilities import log_func_call, logged_run


def tag_commit(
    *,
    user_name: str = SETTINGS.user_name,
    user_email: str = SETTINGS.user_email,
    major_minor: bool = SETTINGS.major_minor,
    major: bool = SETTINGS.major,
    latest: bool = SETTINGS.latest,
) -> None:
    variables = [
        f"{user_name=}",
        f"{user_email=}",
        f"{major_minor=}",
        f"{major=}",
        f"{latest=}",
    ]
    LOGGER.info(log_func_call(tag_commit, *variables))
    logged_run("git", "config", "--global", "user.name", user_name)
    logged_run("git", "config", "--global", "user.email", user_email)
    version = parse_version(
        logged_run("bump-my-version", "show", "current_version", return_=True)
    )
    _tag(str(version))
    if major_minor:
        _tag(f"{version.major}.{version.minor}")
    if major:
        _tag(str(version.major))
    if latest:
        _tag("latest")


def _tag(version: str, /) -> None:
    with suppress(CalledProcessError):
        logged_run("git", "tag", "--delete", version)
    with suppress(CalledProcessError):
        logged_run("git", "push", "--delete", "origin", version)
    logged_run("git", "tag", "-a", version, "HEAD", "-m", version)
    logged_run("git", "push", "--tags", "--force", "--set-upstream", "origin")


__all__ = ["tag_commit"]
