#!/usr/bin/env bash
set -euo pipefail

BOT_DIR="/home/ubuntu/RAVENCOIN"
LOG_FILE="$BOT_DIR/bot.log"
PROCESS_PATTERN="$BOT_DIR/venv/bin/python $BOT_DIR/main.py"
UPDATE_INTERVAL_SECONDS=1800
MAX_LOG_AGE_SECONDS=$((UPDATE_INTERVAL_SECONDS * 2 + 600))

process_count=$(pgrep -fc "$PROCESS_PATTERN" || true)
if [ "$process_count" -ne 1 ]; then
  echo "CRITICAL: expected 1 bot process, found $process_count"
  exit 2
fi

if [ ! -f "$LOG_FILE" ]; then
  echo "CRITICAL: log file missing at $LOG_FILE"
  exit 2
fi

now_epoch=$(date +%s)
log_epoch=$(stat -c %Y "$LOG_FILE")
log_age=$((now_epoch - log_epoch))
if [ "$log_age" -gt "$MAX_LOG_AGE_SECONDS" ]; then
  echo "CRITICAL: log stale for ${log_age}s (max ${MAX_LOG_AGE_SECONDS}s)"
  exit 2
fi

if ! tail -n 200 "$LOG_FILE" | grep -q "Editing existing message"; then
  echo "WARNING: no recent embed-edit log in last 200 lines"
  exit 1
fi

echo "OK: ravencoin bot healthy"
