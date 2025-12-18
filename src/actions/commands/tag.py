from __future__ import annotations

from contextlib import suppress
from subprocess import CalledProcessError, check_output

from utilities.version import parse_version

from actions import __version__
from actions.logging import LOGGER
from actions.settings import SETTINGS


def actions(
    *,
    user_name: str = SETTINGS.tag.user_name,
    user_email: str = SETTINGS.tag.user_email,
    major_minor: bool = SETTINGS.tag.major_minor,
    major: bool = SETTINGS.tag.major,
    latest: bool = SETTINGS.tag.latest,
) -> None:
    LOGGER.info(
        """\
Running 'tag', version %s with settings:
 - user_name   = %s
 - user_email  = %s
 - major_minor = %s
 - major       = %s
 - latest      = %s
""",
        __version__,
        user_name,
        user_email,
        major_minor,
        major,
        latest,
    )
    _ = _log_run("git", "config", "--global", "user.name", user_name)
    _ = _log_run("git", "config", "--global", "user.email", user_email)
    version = parse_version(_log_run("bump-my-version", "show", "current_version"))
    _tag(str(version))
    if major_minor:
        _tag(f"{version.major}.{version.minor}")
    if major:
        _tag(str(version.major))
    if latest:
        _tag("latest")


def _tag(version: str, /) -> None:
    with suppress(CalledProcessError):
        _ = _log_run("git", "tag", "--delete", version)
    with suppress(CalledProcessError):
        _ = _log_run("git", "push", "--delete", "origin", version)
    _ = _log_run("git", "tag", "-a", version, "HEAD", "-m", version)
    _ = _log_run("git", "push", "--tags", "--force", "--set-upstream", "origin")


def _log_run(*cmds: str) -> str:
    LOGGER.info("Running '%s'...", " ".join(cmds))
    return check_output(cmds, text=True)


__all__ = ["actions"]
