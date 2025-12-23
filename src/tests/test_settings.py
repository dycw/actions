from __future__ import annotations

from click import command, echo
from click.testing import CliRunner
from pytest import mark
from typed_settings import (
    EnvLoader,
    Secret,
    click_options,
    load_settings,
    option,
    settings,
)
from utilities.os import temp_environ

from actions.publish.settings import empty_str_to_none
from actions.settings import CommonSettings
from actions.utilities import LOADER


class TestCommonSettings:
    def test_empty_strs(self) -> None:
        with temp_environ(TOKEN=""):
            settings = load_settings(CommonSettings, [EnvLoader("")])
        assert settings.token is None


@mark.only
class TestEmptyStrToNone:
    def test_value_missing(self) -> None:
        @settings
        class Settings:
            key: Secret[str] | None = option(default=None, converter=empty_str_to_none)

        @command()
        @click_options(Settings, [LOADER], show_envvars_in_help=True)
        def cli(settings: Settings, /) -> None:
            if (value := settings.key) is None:
                echo("key = None")
            else:
                echo(f"key = {value.get_secret_value()}")

        result = CliRunner().invoke(cli)
        assert result.exit_code == 0
        assert result.stdout == "key = None\n"

    def test_value_via_cli(self) -> None:
        @settings
        class Settings:
            key: Secret[str] | None = option(default=None, converter=empty_str_to_none)

        @command()
        @click_options(Settings, [LOADER], show_envvars_in_help=True)
        def cli(settings: Settings, /) -> None:
            if (value := settings.key) is None:
                echo("key = None")
            else:
                echo(f"key = {value.get_secret_value()}")

        result = CliRunner().invoke(cli, args=["--key", "value"])
        assert result.exit_code == 0
        assert result.stdout == "key = value\n"

    def test_value_via_env(self) -> None:
        @settings
        class Settings:
            key: Secret[str] | None = option(default=None, converter=empty_str_to_none)

        @command()
        @click_options(Settings, [LOADER], show_envvars_in_help=True)
        def cli(settings: Settings, /) -> None:
            if (value := settings.key) is None:
                echo("key = None")
            else:
                echo(f"key = {value.get_secret_value()}")

        result = CliRunner().invoke(cli, env={"KEY": "value"})
        assert result.exit_code == 0
        assert result.stdout == "key = value\n"
