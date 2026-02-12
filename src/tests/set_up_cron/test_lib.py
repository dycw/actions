from __future__ import annotations

from pytest import mark
from utilities.constants import MINUTE, SECOND, USER
from utilities.core import normalize_multi_line_str

from actions.set_up_cron.lib import Job, _get_crontab


class TestGetCronTab:
    def test_main(self) -> None:
        result = _get_crontab(Job("name", "command"))
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    @mark.only
    def test_multiple(self) -> None:
        result = _get_crontab(Job("name1", "command1"), Job("name2", "command2"))
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name1'..."; flock --nonblock --verbose /tmp/cron-name1.lock timeout --kill-after=10s --verbose 60s command1; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name1' with exit code $?") 2>&1 | tee -a /var/log/name1.log
* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name2'..."; flock --nonblock --verbose /tmp/cron-name2.lock timeout --kill-after=10s --verbose 60s command2; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name2' with exit code $?") 2>&1 | tee -a /var/log/name2.log
"""
        assert result == expected

    def test_prepend_path(self) -> None:
        result = _get_crontab("name", "command", prepend_path=["/foo/bin"])
        expected = f"""\
PATH=/foo/bin:/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_env_vars_one(self) -> None:
        result = _get_crontab("name", "command", env_vars={"KEY": "value"})
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin
KEY=value

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_env_vars_multiple(self) -> None:
        result = _get_crontab(
            "name", "command", env_vars={"KEY1": "value1", "KEY2": "value2"}
        )
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin
KEY1=value1
KEY2=value2

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_schedule(self) -> None:
        result = _get_crontab("name", "command", schedule="*/5 * * * *")
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

*/5 * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_user(self) -> None:
        result = _get_crontab("name", "command", user="user")
        expected = """\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * user (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_timeout(self) -> None:
        result = _get_crontab("name", "command", timeout=120)
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 120s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_kill_after(self) -> None:
        result = _get_crontab("name", "command", kill_after=20)
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=20s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected

    def test_sudo(self) -> None:
        result = _get_crontab("name", "command", sudo=True)
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | sudo tee -a /var/log/name.log
"""
        assert result == expected

    def test_args(self) -> None:
        result = _get_crontab("name", "command", "--dry-run")
        expected = f"""\
PATH=/usr/local/bin:/usr/bin:/bin

* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command --dry-run; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
"""
        assert result == expected


class TestJob:
    def test_main(self) -> None:
        result = Job("name", "command").text
        expected = normalize_multi_line_str(f"""
* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
""")
        assert result == expected

    def test_schedule(self) -> None:
        result = Job("name", "command", schedule="*/5 * * * *").text
        expected = normalize_multi_line_str(f"""
*/5 * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
""")
        assert result == expected

    def test_user(self) -> None:
        result = Job("name", "command", user="user").text
        expected = normalize_multi_line_str("""
* * * * * user (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
""")
        assert result == expected

    def test_timeout(self) -> None:
        result = Job("name", "command", timeout=2 * MINUTE).text
        expected = normalize_multi_line_str(f"""
* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 120s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
""")
        assert result == expected

    def test_kill_after(self) -> None:
        result = Job("name", "command", kill_after=20 * SECOND).text
        expected = normalize_multi_line_str(f"""
* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=20s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
""")
        assert result == expected

    def test_sudo(self) -> None:
        result = Job("name", "command", sudo=True).text
        expected = normalize_multi_line_str(f"""
* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | sudo tee -a /var/log/name.log
""")
        assert result == expected

    def test_args(self) -> None:
        result = Job("name", "command", args=["--dry-run"]).text
        expected = normalize_multi_line_str(f"""
* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command --dry-run; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/name.log
""")
        assert result == expected

    def test_log(self) -> None:
        result = Job("name", "command", log="other").text
        expected = normalize_multi_line_str(f"""
* * * * * {USER} (echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Starting 'name'..."; flock --nonblock --verbose /tmp/cron-name.lock timeout --kill-after=10s --verbose 60s command; echo "[$(date '+\\%Y-\\%m-\\%d \\%H:\\%M:\\%S') | $$] Finished 'name' with exit code $?") 2>&1 | tee -a /var/log/other.log
""")
        assert result == expected
