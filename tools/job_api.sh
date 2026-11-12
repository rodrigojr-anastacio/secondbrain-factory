#!/bin/bash
# Dispara um brief como job pela API (Agent SDK, créditos da API, grupo `dev`), em vez de `claude -p` (cota do Max).
# Uso: tools/job_api.sh <brief.md> <log> [--modelo opus|sonnet|haiku] [--orcamento US$] [--timeout s] [--max-turns n]
# Nohup-friendly (primeiro plano; o chamador põe nohup/&):
#   nohup tools/job_api.sh ~/workspace/referencias/BRIEF-x.md ~/workspace/referencias/x.log --modelo opus --orcamento 8 >/dev/null 2>&1 &
# ANTHROPIC_API_KEY é removida do ambiente; a chave vai só no processo do Agent SDK (job_api.py).
set -u
BRIEF="${1:?uso: job_api.sh <brief.md> <log> [opções]}"; LOG="${2:?log}"; shift 2
export CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0
unset ANTHROPIC_API_KEY
FAB="$(cd "$(dirname "$0")/.." && pwd)"
cd "$FAB" || exit 2
mkdir -p "$(dirname "$LOG")"
echo "== $(date -Is) job_api $BRIEF" >> "$LOG"
"$FAB/tools/.venv/bin/python" "$FAB/tools/job_api.py" "$BRIEF" "$@" >> "$LOG" 2>&1
RC=$?
echo "== $(date -Is) fim (código $RC)" >> "$LOG"
exit $RC
