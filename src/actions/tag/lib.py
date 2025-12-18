from __future__ import annotations

from contextlib import suppress
from subprocess import CalledProcessError

from utilities.version import parse_version

from actions import __version__
from actions.logging import LOGGER
from actions.tag.settings import TAG_SETTINGS
from actions.utilities import log_run


def tag_commit(
    *,
    user_name: str = TAG_SETTINGS.user_name,
    user_email: str = TAG_SETTINGS.user_email,
    major_minor: bool = TAG_SETTINGS.major_minor,
    major: bool = TAG_SETTINGS.major,
    latest: bool = TAG_SETTINGS.latest,
) -> None:
    LOGGER.info(
        """\
Running %r (version %s) with settings:
 - user_name   = %s
 - user_email  = %s
 - major_minor = %s
 - major       = %s
 - latest      = %s
""",
        tag_commit.__name__,
        __version__,
        user_name,
        user_email,
        major_minor,
        major,
        latest,
    )
    _ = log_run("git", "config", "--global", "user.name", user_name)
    _ = log_run("git", "config", "--global", "user.email", user_email)
    version = parse_version(log_run("bump-my-version", "show", "current_version"))
    _tag(str(version))
    if major_minor:
        _tag(f"{version.major}.{version.minor}")
    if major:
        _tag(str(version.major))
    if latest:
        _tag("latest")


def _tag(version: str, /) -> None:
    with suppress(CalledProcessError):
        _ = log_run("git", "tag", "--delete", version)
    with suppress(CalledProcessError):
        _ = log_run("git", "push", "--delete", "origin", version)
    _ = log_run("git", "tag", "-a", version, "HEAD", "-m", version)
    _ = log_run("git", "push", "--tags", "--force", "--set-upstream", "origin")


__all__ = ["tag_commit"]
