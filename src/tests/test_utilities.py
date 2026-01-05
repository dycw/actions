from __future__ import annotations

from typing import TYPE_CHECKING

from click import command, echo
from click.testing import CliRunner
from pytest import mark, param
from typed_settings import Secret, click_options, option, secret, settings

from actions.publish.settings import convert_str
from actions.utilities import LOADER, convert_list_strs, convert_secret_str

if TYPE_CHECKING:
    from pytest import MonkeyPatch


@settings
class _SettingsWithList:
    key: list[str] | None = option(default=None, converter=convert_list_strs)


@command()
@click_options(_SettingsWithList, [LOADER], show_envvars_in_help=True)
def _cli_with_list(settings: _SettingsWithList, /) -> None:
    echo(f"key = {settings.key}")


class TestConvertListStr:
    def test_missing(self) -> None:
        result = CliRunner().invoke(_cli_with_list)
        assert result.exit_code == 0
        assert result.stdout == "key = None\n"

    def test_cli(self) -> None:
        result = CliRunner().invoke(_cli_with_list, args=["--key", "value"])
        assert result.exit_code == 0
        assert result.stdout == "key = ['value']\n"

    def test_cli2(self) -> None:
        result = CliRunner().invoke(
            _cli_with_list, args=["--key", "value1", "--key", "value2"]
        )
        assert result.exit_code == 0
        assert result.stdout == "key = ['value1', 'value2']\n"

    @mark.parametrize(
        ("value", "expected"),
        [
            param("value", "['value']"),
            param("value1\nvalue2", "['value1', 'value2']"),
            param("", "None"),
        ],
    )
    def test_env(self, *, monkeypatch: MonkeyPatch, value: str, expected: str) -> None:
        monkeypatch.setenv("KEY", value)

        @command()
        @click_options(_SettingsWithList, [LOADER], show_envvars_in_help=True)
        def _cli_with_list(settings: _SettingsWithList, /) -> None:
            echo(f"key = {settings.key}")

        result = CliRunner().invoke(_cli_with_list)
        assert result.exit_code == 0
        assert result.stdout == f"key = {expected}\n"


@settings
class _SettingsWithSecret:
    key: Secret[str] | None = secret(default=None, converter=convert_secret_str)


@command()
@click_options(_SettingsWithSecret, [LOADER], show_envvars_in_help=True)
def _cli_with_secret(settings: _SettingsWithSecret, /) -> None:
    if (value := settings.key) is None:
        echo("key = None")
    else:
        echo(f"key = {value.get_secret_value()}")


class TestConvertSecretStr:
    def test_missing(self) -> None:
        result = CliRunner().invoke(_cli_with_secret)
        assert result.exit_code == 0
        assert result.stdout == "key = None\n"

    def test_cli(self) -> None:
        result = CliRunner().invoke(_cli_with_secret, args=["--key", "value"])
        assert result.exit_code == 0
        assert result.stdout == "key = value\n"

    @mark.parametrize(
        ("value", "expected"), [param("value", "value"), param("", "None")]
    )
    def test_env(self, *, monkeypatch: MonkeyPatch, value: str, expected: str) -> None:
        monkeypatch.setenv("KEY", value)

        @command()
        @click_options(_SettingsWithSecret, [LOADER], show_envvars_in_help=True)
        def _cli_with_secret(settings: _SettingsWithSecret, /) -> None:
            if (value := settings.key) is None:
                echo("key = None")
            else:
                echo(f"key = {value.get_secret_value()}")

        result = CliRunner().invoke(_cli_with_secret)
        assert result.exit_code == 0
        assert result.stdout == f"key = {expected}\n"


@settings
class _SettingsWithStr:
    key: str | None = option(default=None, converter=convert_str)


@command()
@click_options(_SettingsWithStr, [LOADER], show_envvars_in_help=True)
def _cli_with_str(settings: _SettingsWithStr, /) -> None:
    echo(f"key = {settings.key}")


class TestConvertStr:
    def test_missing(self) -> None:
        result = CliRunner().invoke(_cli_with_str)
        assert result.exit_code == 0
        assert result.stdout == "key = None\n"

    def test_cli(self) -> None:
        result = CliRunner().invoke(_cli_with_str, args=["--key", "value"])
        assert result.exit_code == 0
        assert result.stdout == "key = value\n"

    @mark.parametrize(
        ("value", "expected"), [param("value", "value"), param("", "None")]
    )
    def test_env(self, *, monkeypatch: MonkeyPatch, value: str, expected: str) -> None:
        monkeypatch.setenv("KEY", value)

        @command()
        @click_options(_SettingsWithStr, [LOADER], show_envvars_in_help=True)
        def _cli_with_str(settings: _SettingsWithStr, /) -> None:
            echo(f"key = {settings.key}")

        result = CliRunner().invoke(_cli_with_str)
        assert result.exit_code == 0
        assert result.stdout == f"key = {expected}\n"
