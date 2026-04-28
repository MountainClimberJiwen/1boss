#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: $0 '<payload>'"
  exit 1
fi

PAYLOAD="$*"
exec python3 /Users/jiwen/PycharmProjects/openclaw/.cursor/skills/project-task-enqueue/scripts/add_task.py --payload "$PAYLOAD"
