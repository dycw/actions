from __future__ import annotations

from click import group
from utilities.click import CONTEXT_SETTINGS

from actions.clean_dir.cli import clean_dir_sub_cmd
from actions.format_requirements.cli import format_requirements_sub_cmd
from actions.publish_package.cli import publish_package_sub_cmd
from actions.random_sleep.cli import random_sleep_sub_cmd
from actions.replace_sequence_strs.cli import sequence_strs_sub_cmd
from actions.run_hooks.cli import run_hooks_sub_cmd
from actions.tag_commit.cli import tag_commit_sub_cmd


@group(**CONTEXT_SETTINGS)
def _main() -> None: ...


_ = _main.command(name="clean-dir", help="Clean a directory", **CONTEXT_SETTINGS)(
    clean_dir_sub_cmd
)
_ = _main.command(
    name="format-requirements", help="Format a set of requirements", **CONTEXT_SETTINGS
)(format_requirements_sub_cmd)
_ = _main.command(name="publish-package", help="Publish a package", **CONTEXT_SETTINGS)(
    publish_package_sub_cmd
)
_ = _main.command(
    name="replace-sequence-strs", help="Replace `Sequence[str]`", **CONTEXT_SETTINGS
)(sequence_strs_sub_cmd)
_ = _main.command(name="run-hooks", help="Run `pre-commit` hooks", **CONTEXT_SETTINGS)(
    run_hooks_sub_cmd
)
_ = _main.command(
    name="random-sleep", help="Sleep for a random duration", **CONTEXT_SETTINGS
)(random_sleep_sub_cmd)
_ = _main.command(name="tag-commit", help="Tag the current commit", **CONTEXT_SETTINGS)(
    tag_commit_sub_cmd
)


if __name__ == "__main__":
    _main()
