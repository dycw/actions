from __future__ import annotations

from typing import TYPE_CHECKING

import utilities.click
from click import command, option
from utilities.click import ListStrs, Str
from utilities.core import is_pytest, set_up_logging

from actions.constants import sudo_option
from actions.register_gitea_runner.constants import (
    GITEA_CONTAINER_NAME,
    GITEA_CONTAINER_USER,
    GITEA_HOST,
    GITEA_PORT,
    RUNNER_CAPACITY,
    RUNNER_CERTIFICATE,
    RUNNER_CONTAINER_NAME,
    RUNNER_INSTANCE_NAME,
    RUNNER_LABELS,
    SSH_HOST,
    SSH_USER,
)
from actions.register_gitea_runner.lib import register_gitea_runner

if TYPE_CHECKING:
    from utilities.types import MaybeSequenceStr, PathLike


@option("--runner_token", type=Str(), default=None, help="Registration token")
@option("--ssh-user", type=Str(), default=SSH_USER, help="SSH username")
@option("--ssh-host", type=Str(), default=SSH_HOST, help="SSH host")
@option(
    "--gitea-container-user",
    type=Str(),
    default=GITEA_CONTAINER_USER,
    help="Gitea container user name",
)
@option(
    "--gitea-container-name",
    type=Str(),
    default=GITEA_CONTAINER_NAME,
    help="Gitea container name",
)
@option(
    "--runner-certificate",
    type=utilities.click.Path(exist="existing file"),
    default=RUNNER_CERTIFICATE,
    help="Runner root certificate",
)
@option("--runner-capacity", type=int, default=RUNNER_CAPACITY, help="Runner capacity")
@option("--runner-labels", type=ListStrs(), default=RUNNER_LABELS, help="Runner labels")
@option(
    "--runner-container-name",
    type=Str(),
    default=RUNNER_CONTAINER_NAME,
    help="Runner container name",
)
@option("--gitea-host", type=Str(), default=GITEA_HOST, help="Gitea host")
@option("--gitea-port", type=int, default=GITEA_PORT, help="Gitea port")
@sudo_option
@option(
    "--runner-instance-name",
    type=Str(),
    default=RUNNER_INSTANCE_NAME,
    help="Runner instance name",
)
def register_gitea_runner_sub_cmd(
    *,
    runner_token: str | None,
    ssh_user: str,
    ssh_host: str,
    gitea_container_user: str,
    gitea_container_name: str,
    runner_certificate: PathLike,
    runner_capacity: int,
    runner_labels: MaybeSequenceStr | None,
    runner_container_name: str,
    gitea_host: str,
    gitea_port: int,
    sudo: bool,
    runner_instance_name: str,
) -> None:
    if is_pytest():
        return
    set_up_logging(__name__, root=True)
    register_gitea_runner(
        runner_token=runner_token,
        ssh_user=ssh_user,
        ssh_host=ssh_host,
        gitea_container_user=gitea_container_user,
        gitea_container_name=gitea_container_name,
        runner_certificate=runner_certificate,
        runner_capacity=runner_capacity,
        runner_labels=runner_labels,
        runner_container_name=runner_container_name,
        gitea_host=gitea_host,
        gitea_port=gitea_port,
        sudo=sudo,
        runner_instance_name=runner_instance_name,
    )


cli = command(register_gitea_runner_sub_cmd)


__all__ = ["cli", "register_gitea_runner_sub_cmd"]
