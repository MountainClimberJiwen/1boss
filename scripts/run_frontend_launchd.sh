#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/jiwen/PycharmProjects/iboss/vue"
NODE_BIN_DIR="/Users/jiwen/.nvm/versions/node/v22.14.0/bin"
NPM_BIN="$NODE_BIN_DIR/npm"

# launchd uses a minimal PATH; prepend Node path explicitly.
export PATH="$NODE_BIN_DIR:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

cd "$ROOT"

# Ensure dependencies exist after reboot or cleanups.
if [[ ! -d node_modules ]]; then
  "$NPM_BIN" install
fi

exec "$NPM_BIN" run dev
