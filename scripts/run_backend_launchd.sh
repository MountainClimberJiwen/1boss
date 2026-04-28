#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/jiwen/PycharmProjects/task-queue-system"
VENV_PYTHON="$ROOT/.venv/bin/python"

if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "missing python in venv: $VENV_PYTHON"
  exit 1
fi

export PATH="$ROOT/.venv/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"
export TASK_QUEUE_DB_PATH="${TASK_QUEUE_DB_PATH:-$ROOT/data/task_queue.db}"
export TASK_QUEUE_API_HOST="${TASK_QUEUE_API_HOST:-127.0.0.1}"
export TASK_QUEUE_API_PORT="${TASK_QUEUE_API_PORT:-8080}"
export TASK_QUEUE_DASHBOARD_AUTH_ENABLED="${TASK_QUEUE_DASHBOARD_AUTH_ENABLED:-0}"
export PYTHONPATH="${PYTHONPATH:-$ROOT/src}"

cd "$ROOT"
exec "$VENV_PYTHON" -m task_queue_system.cli run-api --host "$TASK_QUEUE_API_HOST" --port "$TASK_QUEUE_API_PORT"
