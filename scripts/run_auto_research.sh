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
export OLLAMA_API_URL="${OLLAMA_API_URL:-http://127.0.0.1:11434/v1/chat/completions}"
export OLLAMA_MODEL="${OLLAMA_MODEL:-qwen3.5:4b}"

cd /Users/jiwen/PycharmProjects/iboss
exec python3 scripts/auto_research.py
