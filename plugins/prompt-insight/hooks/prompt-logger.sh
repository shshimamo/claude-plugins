#!/bin/bash
# Prompt Insight - UserPromptSubmit hook
LOG_DIR="$HOME/.claude-plugins/prompt-insight/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).jsonl"

INPUT=$(cat)
PROMPT=$(echo "$INPUT" | jq -r '.prompt // empty' 2>/dev/null)
CWD=$(echo "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
SESSION=$(echo "$INPUT" | jq -r '.session_id // empty' 2>/dev/null)

if [ -n "$PROMPT" ]; then
  ENTRY=$(jq -n \
    --arg ts "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --arg prompt "$PROMPT" \
    --arg cwd "$CWD" \
    --arg session "$SESSION" \
    '{timestamp: $ts, prompt: $prompt, cwd: $cwd, session_id: $session}')
  echo "$ENTRY" >> "$LOG_FILE"
fi
