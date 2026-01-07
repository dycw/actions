from __future__ import annotations

from rich.pretty import pretty_repr
from typed_settings import click_options
from utilities.logging import basic_config
from utilities.os import is_pytest
from utilities.text import strip_and_dedent

from actions import __version__
from actions.conformalize_repo.lib import conformalize_repo
from actions.conformalize_repo.settings import Settings
from actions.logging import LOGGER
from actions.utilities import LOADER


@click_options(Settings, [LOADER], show_envvars_in_help=True)
def conformalize_repo_sub_cmd(settings: Settings, /) -> None:
    if is_pytest():
        return
    basic_config(obj=LOGGER)
    LOGGER.info(
        strip_and_dedent("""
            Running '%s' (version %s) with settings:
            %s
        """),
        conformalize_repo.__name__,
        __version__,
        pretty_repr(settings),
    )
    conformalize_repo(
        coverage=settings.coverage,
        description=settings.description,
        envrc=settings.envrc,
        envrc__uv=settings.envrc__uv,
        envrc__uv__native_tls=settings.envrc__uv__native_tls,
        github__pull_request__pre_commit=settings.github__pull_request__pre_commit,
        github__pull_request__pyright=settings.github__pull_request__pyright,
        github__pull_request__pytest__macos=settings.github__pull_request__pytest__macos,
        github__pull_request__pytest__ubuntu=settings.github__pull_request__pytest__ubuntu,
        github__pull_request__pytest__windows=settings.github__pull_request__pytest__windows,
        github__pull_request__ruff=settings.github__pull_request__ruff,
        github__push__publish=settings.github__push__publish,
        github__push__tag=settings.github__push__tag,
        github__push__tag__major=settings.github__push__tag__major,
        github__push__tag__major_minor=settings.github__push__tag__major_minor,
        github__push__tag__latest=settings.github__push__tag__latest,
        gitignore=settings.gitignore,
        package_name=settings.package_name,
        pre_commit__dockerfmt=settings.pre_commit__dockerfmt,
        pre_commit__prettier=settings.pre_commit__prettier,
        pre_commit__python=settings.pre_commit__python,
        pre_commit__ruff=settings.pre_commit__ruff,
        pre_commit__shell=settings.pre_commit__shell,
        pre_commit__taplo=settings.pre_commit__taplo,
        pre_commit__uv=settings.pre_commit__uv,
        pre_commit__uv__script=settings.pre_commit__uv__script,
        pyproject=settings.pyproject,
        pyproject__project__optional_dependencies__scripts=settings.pyproject__project__optional_dependencies__scripts,
        pyproject__tool__uv__indexes=settings.pyproject__tool__uv__indexes,
        pyright=settings.pyright,
        pytest=settings.pytest,
        pytest__asyncio=settings.pytest__asyncio,
        pytest__ignore_warnings=settings.pytest__ignore_warnings,
        pytest__timeout=settings.pytest__timeout,
        python_package_name=settings.python_package_name,
        python_version=settings.python_version,
        readme=settings.readme,
        repo_name=settings.repo_name,
        ruff=settings.ruff,
        run_version_bump=settings.run_version_bump,
        script=settings.script,
    )


__all__ = ["conformalize_repo_sub_cmd"]
