#!/bin/bash
# Rotina backlog vivo (14/11/2026): reordena o youtube.backlog 2× por semana, logo depois do garimpo de seg/qui.
# Encadeada no fabrica-tendencias.service (ExecStopPost → fabrica-backlog.service); na mão: tools/rotinas/backlog.sh [--teste] [--sem-telegram]
# 1) backlog.py tudo (sem IA)  2) agente pela API (prompts/backlog.md, sonnet, US$ 3; fallback Max)  3) backlog.py tudo + commit dos espelhos
set -u
FAB="$HOME/workspace/fabrica-youtube"; PY="$FAB/tools/.venv/bin/python"
"$PY" "$FAB/tools/rotinas/backlog.py" tudo || true
ORCAMENTO=${ORCAMENTO:-3} "$(dirname "$0")/_rotina_claude.sh" backlog "$@"
RC=$?
"$PY" "$FAB/tools/rotinas/backlog.py" tudo || true
cd "$FAB" || exit $RC
MDS="canais/historia-ptbr/backlog.md canais/dossie-es/backlog.md canais/em-relevo/backlog.md canais/lugares-guerra-en/backlog.md"
if [ -n "$(git status --porcelain -- $MDS)" ]; then
  for i in 1 2 3 4 5 6; do
    [ -e .git/index.lock ] && { sleep 10; continue; }
    git add -- $MDS && git commit -q -m "backlog vivo: espelho regenerado ($(date +%F) rotina backlog)" -- $MDS && break
    sleep 10
  done
fi
exit $RC
