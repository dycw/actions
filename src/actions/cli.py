from __future__ import annotations

from click import command
from rich.pretty import pretty_repr
from typed_settings import EnvLoader, click_options
from utilities.click import CONTEXT_SETTINGS
from utilities.logging import basic_config

from actions import __version__
from actions.lib import action
from actions.logging import LOGGER
from actions.settings import Settings


@command(**CONTEXT_SETTINGS)
@click_options(Settings, [EnvLoader("")], show_envvars_in_help=True)
def _main(settings: Settings, /) -> None:
    basic_config(obj=LOGGER)
    LOGGER.info(
        """\
Running version %s with settings:
%s""",
        __version__,
        pretty_repr(settings),
    )
    if settings.dry_run:
        LOGGER.info("Dry run; exiting...")
        return
    action(flag=settings.flag)


if __name__ == "__main__":
    _main()
