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
export TASK_QUEUE_DISPATCHER_PROJECT_ID="${TASK_QUEUE_DISPATCHER_PROJECT_ID:-all}"
export TASK_QUEUE_DISPATCHER_BACKEND="${TASK_QUEUE_DISPATCHER_BACKEND:-hermes}"

exec task-queue run-dispatcher
