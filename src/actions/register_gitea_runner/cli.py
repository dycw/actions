from __future__ import annotations

from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest

from actions.logging import LOGGER
from actions.register_gitea_runner.lib import register_gitea_runner
from actions.register_gitea_runner.settings import Settings
from actions.utilities import LOADER


@click_options(Settings, [LOADER], show_envvars_in_help=True)
def register_gitea_runner_sub_cmd(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    register_gitea_runner(
        ssh_user=settings.ssh_user,
        ssh_host=settings.ssh_host,
        gitea_container_user=settings.gitea_container_user,
        gitea_container_name=settings.gitea_container_name,
        runner_certificate=settings.runner_certificate,
        runner_capacity=settings.runner_capacity,
        runner_container_name=settings.runner_container_name,
        gitea_host=settings.gitea_host,
        gitea_port=settings.gitea_port,
        runner_instance_name=settings.runner_instance_name,
    )


__all__ = ["register_gitea_runner_sub_cmd"]
