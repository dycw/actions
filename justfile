set dotenv-load := true
set fallback := true
set positional-arguments := true

# cli

# CLI entrypoint
@cli *args:
  cli {{args}}

# Clean a directory
@clean-dir *args:
  clean-dir {{args}}

# Build and publish the package
@publish-package *args:
  publish-package {{args}}

# Random sleep with logging
@random-sleep *args:
  random-sleep {{args}}

# Re-encrypt a JSON file
@re-encrypt *args:
  re-encrypt {{args}}

# Register a Gitea runner
@register-gitea-runner *args:
  register-gitea-runner {{args}}

# Set up 'cron'
@set-up-cron *args:
  set-up-cron {{args}}

# Tag the latest commit
@tag-commit *args:
  tag-commit {{args}}
