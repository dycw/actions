from __future__ import annotations

from typing import TYPE_CHECKING

from click import command, echo
from click.testing import CliRunner
from typed_settings import Secret, click_options, option, settings

from actions.publish.settings import empty_str_to_none
from actions.utilities import LOADER

if TYPE_CHECKING:
    from pytest import MonkeyPatch


@settings
class _Settings:
    key: Secret[str] | None = option(default=None, converter=empty_str_to_none)


@command()
@click_options(
    _Settings, [LOADER], show_envvars_in_help=True, reload_settings_on_invoke=True
)
def _cli(settings: _Settings, /) -> None:
    if (value := settings.key) is None:
        echo("key = None")
    else:
        echo(f"key = {value.get_secret_value()}")


class TestEmptyStrToNone:
    def test_value_missing(self) -> None:
        result = CliRunner().invoke(_cli)
        assert result.exit_code == 0
        assert result.stdout == "key = None\n"

    def test_value_via_cli(self) -> None:
        result = CliRunner().invoke(_cli, args=["--key", "value"])
        assert result.exit_code == 0
        assert result.stdout == "key = value\n"

    def test_value_via_env(self, *, monkeypatch: MonkeyPatch) -> None:
        monkeypatch.setenv("KEY", "value")

        @command()
        @click_options(
            _Settings,
            [LOADER],
            show_envvars_in_help=True,
            reload_settings_on_invoke=True,
        )
        def _cli(settings: _Settings, /) -> None:
            if (value := settings.key) is None:
                echo("key = None")
            else:
                echo(f"key = {value.get_secret_value()}")

        result = CliRunner().invoke(_cli)
        assert result.exit_code == 0
        assert result.stdout == "key = value\n"
