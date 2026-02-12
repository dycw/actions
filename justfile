set dotenv-load := true
set fallback := true
set positional-arguments := true

# cli

@cli *args:
  cli {{args}}

@clean-dir *args:
  clean-dir {{args}}

@publish-package *args:
  publish-package {{args}}

@random-sleep *args:
  random-sleep {{args}}

@re-encrypt *args:
  re-encrypt {{args}}

@register-gitea-runner *args:
  register-gitea-runner {{args}}

@set-up-cron *args:
  set-up-cron {{args}}

@tag-commit *args:
  tag-commit {{args}}
