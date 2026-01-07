from __future__ import annotations

from click import group
from utilities.click import CONTEXT_SETTINGS

import actions.publish_package.doc
import actions.random_sleep.doc
import actions.run_hooks.doc
import actions.tag_commit.doc
from actions.clean_dir.cli import clean_dir_sub_cmd
from actions.pre_commit.conformalize_repo.cli import conformalize_repo_sub_cmd
from actions.pre_commit.format_requirements.cli import format_requirements_sub_cmd
from actions.pre_commit.replace_sequence_strs.cli import sequence_strs_sub_cmd
from actions.publish_package.cli import publish_package_sub_cmd
from actions.random_sleep.cli import random_sleep_sub_cmd
from actions.run_hooks.cli import run_hooks_sub_cmd
from actions.setup_cronjob.cli import setup_cronjob_sub_cmd
from actions.tag_commit.cli import tag_commit_sub_cmd


@group(**CONTEXT_SETTINGS)
def _main() -> None: ...


_ = _main.command(name="clean-dir", help="Clean a directory", **CONTEXT_SETTINGS)(
    clean_dir_sub_cmd
)
_ = _main.command(
    name="conformalize-repo", help="Conformalize a repo", **CONTEXT_SETTINGS
)(conformalize_repo_sub_cmd)
_ = _main.command(
    name="format-requirements", help="Format a set of requirements", **CONTEXT_SETTINGS
)(format_requirements_sub_cmd)
_ = _main.command(
    name="publish-package",
    help=actions.publish_package.doc.DOCSTRING,
    **CONTEXT_SETTINGS,
)(publish_package_sub_cmd)
_ = _main.command(
    name="replace-sequence-strs",
    help="Replace 'Sequence[str]' with 'list[str]'",
    **CONTEXT_SETTINGS,
)(sequence_strs_sub_cmd)
_ = _main.command(
    name="run-hooks", help=actions.run_hooks.doc.DOCSTRING, **CONTEXT_SETTINGS
)(run_hooks_sub_cmd)
_ = _main.command(
    name="random-sleep", help=actions.random_sleep.doc.DOCSTRING, **CONTEXT_SETTINGS
)(random_sleep_sub_cmd)
_ = _main.command(name="setup-cronjob", help="Setup a cronjob", **CONTEXT_SETTINGS)(
    setup_cronjob_sub_cmd
)
_ = _main.command(
    name="tag-commit", help=actions.tag_commit.doc.DOCSTRING, **CONTEXT_SETTINGS
)(tag_commit_sub_cmd)


if __name__ == "__main__":
    _main()
