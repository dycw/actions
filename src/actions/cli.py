from __future__ import annotations

from click import group
from utilities.click import CONTEXT_SETTINGS

from actions.clean_dir.cli import clean_dir_sub_cmd
from actions.pre_commit.conformalize_repo.cli import conformalize_repo_sub_cmd
from actions.pre_commit.conformalize_repo.constants import CONFORMALIZE_REPO_SUB_CMD
from actions.pre_commit.format_requirements.cli import format_requirements_sub_cmd
from actions.pre_commit.format_requirements.constants import FORMAT_REQUIREMENTS_SUB_CMD
from actions.pre_commit.replace_sequence_strs.cli import replace_sequence_strs_sub_cmd
from actions.pre_commit.replace_sequence_strs.constants import (
    REPLACE_SEQUENCE_STRS_SUB_CMD,
)
from actions.pre_commit.touch_empty_py.cli import touch_empty_py_sub_cmd
from actions.pre_commit.touch_empty_py.constants import (
    TOUCH_EMPTY_PY_DOCSTRING,
    TOUCH_EMPTY_PY_SUB_CMD,
)
from actions.pre_commit.touch_py_typed.constants import (
    TOUCH_PY_TYPED_DOCSTRING,
    TOUCH_PY_TYPED_SUB_CMD,
)
from actions.publish_package.cli import publish_package_sub_cmd
from actions.publish_package.constants import PUBLISH_PACKAGE_DOCSTRING
from actions.random_sleep.cli import random_sleep_sub_cmd
from actions.random_sleep.constants import RANDOM_SLEEP_DOCSTRING
from actions.run_hooks.cli import run_hooks_sub_cmd
from actions.run_hooks.constants import RUN_HOOKS_DOCSTRING
from actions.setup_cronjob.cli import setup_cronjob_sub_cmd
from actions.tag_commit.cli import tag_commit_sub_cmd
from actions.tag_commit.constants import TAG_COMMIT_DOCSTRING


@group(**CONTEXT_SETTINGS)
def _main() -> None: ...


_ = _main.command(name="clean-dir", help="Clean a directory", **CONTEXT_SETTINGS)(
    clean_dir_sub_cmd
)
_ = _main.command(
    name="publish-package", help=PUBLISH_PACKAGE_DOCSTRING, **CONTEXT_SETTINGS
)(publish_package_sub_cmd)
_ = _main.command(name="run-hooks", help=RUN_HOOKS_DOCSTRING, **CONTEXT_SETTINGS)(
    run_hooks_sub_cmd
)
_ = _main.command(name="random-sleep", help=RANDOM_SLEEP_DOCSTRING, **CONTEXT_SETTINGS)(
    random_sleep_sub_cmd
)
_ = _main.command(name="setup-cronjob", help="Setup a cronjob", **CONTEXT_SETTINGS)(
    setup_cronjob_sub_cmd
)
_ = _main.command(name="tag-commit", help=TAG_COMMIT_DOCSTRING, **CONTEXT_SETTINGS)(
    tag_commit_sub_cmd
)


@_main.group(name="pre-commit", help="Pre-commit hooks", **CONTEXT_SETTINGS)
def pre_commit_sub_cmd() -> None: ...


_ = pre_commit_sub_cmd.command(
    name=CONFORMALIZE_REPO_SUB_CMD, help="Conformalize a repo", **CONTEXT_SETTINGS
)(conformalize_repo_sub_cmd)
_ = pre_commit_sub_cmd.command(
    name=FORMAT_REQUIREMENTS_SUB_CMD,
    help="Format a set of requirements",
    **CONTEXT_SETTINGS,
)(format_requirements_sub_cmd)
_ = pre_commit_sub_cmd.command(
    name=REPLACE_SEQUENCE_STRS_SUB_CMD,
    help="Replace 'Sequence[str]' with 'list[str]'",
    **CONTEXT_SETTINGS,
)(replace_sequence_strs_sub_cmd)
_ = pre_commit_sub_cmd.command(
    name=TOUCH_EMPTY_PY_SUB_CMD, help=TOUCH_EMPTY_PY_DOCSTRING, **CONTEXT_SETTINGS
)(touch_empty_py_sub_cmd)
_ = pre_commit_sub_cmd.command(
    name=TOUCH_PY_TYPED_SUB_CMD, help=TOUCH_PY_TYPED_DOCSTRING, **CONTEXT_SETTINGS
)(touch_empty_py_sub_cmd)


if __name__ == "__main__":
    _main()
