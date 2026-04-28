#!/usr/bin/env bash
set -euo pipefail

HOST="${TASK_QUEUE_API_HOST:-127.0.0.1}"
PORT="${TASK_QUEUE_API_PORT:-8080}"
URL="http://${HOST}:${PORT}/dashboard"

echo "$URL"
