#!/usr/bin/env bash
set -euo pipefail

CODEX_BIN="/Users/jiwen/.nvm/versions/node/v22.14.0/bin/codex"
WORKDIR="/Users/jiwen/PycharmProjects/iboss"
MEMORY_FILE="/Users/jiwen/PycharmProjects/memory.md"
LOG_FILE="/tmp/codex-daily-memory-summary.log"
AUDIT_FILE="/tmp/codex-daily-memory-summary-audit.log"
FALLBACK_BIN="/Users/jiwen/PycharmProjects/iboss/scripts/daily_memory_summary_fallback.py"
RUNTIME_CODEX_HOME="/Users/jiwen/PycharmProjects/iboss/.codex_runtime"
TIMEOUT_SECONDS="${SUMMARY_TIMEOUT_SECONDS:-600}"
TARGET_DATE="${TARGET_DATE_OVERRIDE:-$(date -v-1d '+%Y-%m-%d' 2>/dev/null || date -d 'yesterday' '+%Y-%m-%d')}"
export PATH="/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
export PATH="/Users/jiwen/.nvm/versions/node/v22.14.0/bin:$PATH"
export OTEL_SDK_DISABLED="true"

mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$(dirname "$AUDIT_FILE")"
mkdir -p "$RUNTIME_CODEX_HOME"/{sessions,history}

# Use project-local CODEX_HOME to avoid ~/.codex/sessions permission issues in launchd/non-interactive runs.
if [ -f "/Users/jiwen/.codex/auth.json" ] && [ ! -f "$RUNTIME_CODEX_HOME/auth.json" ]; then
  cp "/Users/jiwen/.codex/auth.json" "$RUNTIME_CODEX_HOME/auth.json"
fi
if [ -f "/Users/jiwen/.codex/config.toml" ] && [ ! -f "$RUNTIME_CODEX_HOME/config.toml" ]; then
  cp "/Users/jiwen/.codex/config.toml" "$RUNTIME_CODEX_HOME/config.toml"
fi
export CODEX_HOME="$RUNTIME_CODEX_HOME"

PROMPT="把我昨天一天的codex session都分析一下，按事情本身范畴合并相同类型任务，不要按session分组。每一条都包含：做的事情、想解决的问题、使用的方法。再尝试为每一条总结匹配 project-task-enqueue 里的 project（优先依据 project_id、aliases、repo/path 关键词；可参考 http://127.0.0.1:8080/api/projects/state 的 projects 列表）。如果能匹配，在该条后面追加一行：project: <project_id>；如果不能匹配就不写 project 行。最后追加写入 ${MEMORY_FILE}。"

run_codex_with_timeout() {
  local timeout="$1"
  "$CODEX_BIN" exec \
    --dangerously-bypass-approvals-and-sandbox \
    --skip-git-repo-check \
    "$PROMPT" < /dev/null &
  local pid=$!
  local elapsed=0
  while kill -0 "$pid" 2>/dev/null; do
    if [ "$elapsed" -ge "$timeout" ]; then
      echo "[$(date '+%Y-%m-%d %H:%M:%S %z')] codex timed out after ${timeout}s, terminating pid=$pid"
      kill "$pid" 2>/dev/null || true
      sleep 2
      kill -9 "$pid" 2>/dev/null || true
      wait "$pid" 2>/dev/null || true
      return 124
    fi
    sleep 1
    elapsed=$((elapsed + 1))
  done
  wait "$pid"
  return $?
}

start_ts="$(date '+%Y-%m-%d %H:%M:%S %z')"
echo "[$start_ts] START daily memory summary" >> "$AUDIT_FILE"

{
  echo "[$start_ts] start daily memory summary"
  cd "$WORKDIR"
  set +e
  run_codex_with_timeout "$TIMEOUT_SECONDS"
  cmd_status=$?
  if [ "$cmd_status" -ne 0 ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S %z')] first attempt failed exit_code=$cmd_status, retry once after 10s"
    sleep 10
    run_codex_with_timeout "$TIMEOUT_SECONDS"
    cmd_status=$?
  fi
  set -e
  end_ts="$(date '+%Y-%m-%d %H:%M:%S %z')"
  if [ "$cmd_status" -eq 0 ]; then
    if grep -q "^## ${TARGET_DATE} Codex " "$MEMORY_FILE" 2>/dev/null; then
      echo "[$end_ts] done"
      echo "[$end_ts] SUCCESS exit_code=0 target_date=${TARGET_DATE}" >> "$AUDIT_FILE"
    else
      echo "[$end_ts] codex returned 0 but memory missing target_date=${TARGET_DATE}, running fallback"
      /usr/bin/python3 "$FALLBACK_BIN" --target-date "$TARGET_DATE"
      fb_status=$?
      if [ "$fb_status" -eq 0 ] && grep -q "^## ${TARGET_DATE} Codex " "$MEMORY_FILE" 2>/dev/null; then
        echo "[$end_ts] fallback done after codex success"
        echo "[$end_ts] SUCCESS_FALLBACK_AFTER_ZERO target_date=${TARGET_DATE}" >> "$AUDIT_FILE"
      else
        echo "[$end_ts] fallback failed after codex success"
        echo "[$end_ts] FAILED_AFTER_ZERO target_date=${TARGET_DATE}" >> "$AUDIT_FILE"
        exit 1
      fi
    fi
  else
    echo "[$end_ts] codex failed exit_code=$cmd_status, running fallback summary"
    /usr/bin/python3 "$FALLBACK_BIN" --target-date "$TARGET_DATE"
    fb_status=$?
    if [ "$fb_status" -eq 0 ] && grep -q "^## ${TARGET_DATE} Codex " "$MEMORY_FILE" 2>/dev/null; then
      echo "[$end_ts] fallback done"
      echo "[$end_ts] SUCCESS_FALLBACK codex_exit=$cmd_status fallback_exit=0 target_date=${TARGET_DATE}" >> "$AUDIT_FILE"
    else
      echo "[$end_ts] fallback failed exit_code=$fb_status"
      echo "[$end_ts] FAILED codex_exit=$cmd_status fallback_exit=$fb_status target_date=${TARGET_DATE}" >> "$AUDIT_FILE"
      exit "$cmd_status"
    fi
  fi
} >> "$LOG_FILE" 2>&1
