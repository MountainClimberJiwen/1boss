#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/jiwen/PycharmProjects/task-queue-system"
VENV="$ROOT/.venv/bin/activate"

if [[ ! -f "$VENV" ]]; then
  echo "missing venv: $VENV"
  exit 1
fi

source "$VENV"
export TASK_QUEUE_DB_PATH="${TASK_QUEUE_DB_PATH:-$ROOT/data/task_queue.db}"
export TASK_QUEUE_API_HOST="${TASK_QUEUE_API_HOST:-127.0.0.1}"
export TASK_QUEUE_API_PORT="${TASK_QUEUE_API_PORT:-8080}"
export TASK_QUEUE_DASHBOARD_AUTH_ENABLED="${TASK_QUEUE_DASHBOARD_AUTH_ENABLED:-1}"

cd "$ROOT"
export PYTHONPATH="${PYTHONPATH:-src}"
exec python -m task_queue_system.cli run-api --host "$TASK_QUEUE_API_HOST" --port "$TASK_QUEUE_API_PORT"
