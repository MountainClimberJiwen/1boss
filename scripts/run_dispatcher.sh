#!/usr/bin/env bash
set -euo pipefail

ROOT="/Users/jiwen/PycharmProjects/task-queue-system"
VENV="$ROOT/.venv/bin/activate"

if [[ ! -f "$VENV" ]]; then
  echo "missing venv: $VENV"
  exit 1
fi

export TASK_QUEUE_DB_PATH="${TASK_QUEUE_DB_PATH:-$ROOT/data/task_queue.db}"
export TASK_QUEUE_DISPATCHER_PROJECT_ID="${TASK_QUEUE_DISPATCHER_PROJECT_ID:-all}"
export TASK_QUEUE_DISPATCHER_BACKEND="${TASK_QUEUE_DISPATCHER_BACKEND:-hermes}"
if [[ -x "/Users/jiwen/.local/bin/kimi" ]]; then
  export TASK_QUEUE_KIMI_BIN="${TASK_QUEUE_KIMI_BIN:-/Users/jiwen/.local/bin/kimi}"
fi

exec "$ROOT/.venv/bin/python3" -m task_queue_system.cli run-dispatcher
