from __future__ import annotations

from click import group
from utilities.click import CONTEXT_SETTINGS

from actions.clean_dir.lib import clean_dir
from actions.format_requirements.cli import requirements_sub_cmd
from actions.publish_package.cli import publish_sub_cmd
from actions.random_sleep.cli import sleep_sub_cmd
from actions.replace_sequence_strs.cli import sequence_strs_sub_cmd
from actions.run_hooks.cli import hooks_sub_cmd
from actions.tag_commit.cli import tag_sub_cmd


@group(**CONTEXT_SETTINGS)
def _main() -> None: ...


_ = _main.command(name="clean-dir", help="Clean a directory", **CONTEXT_SETTINGS)(
    clean_dir
)
_ = _main.command(name="hooks", **CONTEXT_SETTINGS)(hooks_sub_cmd)
_ = _main.command(name="publish", **CONTEXT_SETTINGS)(publish_sub_cmd)
_ = _main.command(name="requirements", **CONTEXT_SETTINGS)(requirements_sub_cmd)
_ = _main.command(name="sequence-strs", **CONTEXT_SETTINGS)(sequence_strs_sub_cmd)
_ = _main.command(name="sleep", **CONTEXT_SETTINGS)(sleep_sub_cmd)
_ = _main.command(name="tag", **CONTEXT_SETTINGS)(tag_sub_cmd)


if __name__ == "__main__":
    _main()
