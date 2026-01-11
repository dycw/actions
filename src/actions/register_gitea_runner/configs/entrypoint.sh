#!/usr/bin/env sh
set -euxo

# echo
echo_date() { echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" >&2; }

# main
wait-for-it.sh \
	--host="${GITEA_HOST}" \
	--port="${GITEA_PORT}" \
	--strict \
	-- \
	echo "${GITEA_HOST}:${GITEA_PORT} is up"

if ! command -v update-ca-certificates >/dev/null 2>&1; then
	echo_date "Installing 'ca-certificates'..."
	apk update
	apk add --no-cache ca-certificates
fi

update-ca-certificates || true

exec /sbin/tini -- run.sh
