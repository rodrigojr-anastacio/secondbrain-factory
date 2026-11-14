#!/bin/bash
# Rotina semanal de reembalagem, padrão Lutz (systemd: fabrica-reembalagem.timer, sáb 02:00). Pedido do Rodrigo, 14/11/2026.
# 1) reembalagem.py preparar (sem IA): Reporting API, foto de título/thumb, fonte (API 28 d ou Studio), classificação nos
#    3 padrões, ciclo de vida em youtube.reembalagem → ~/workspace/relatorios/reembalagem/dados/<data>[-teste].{json,md}
# 2) _rotina_claude.sh reembalagem (Claude pela API, sonnet, US$ 4): propostas do padrão 1 com pesquisa + crivo (Task opus),
#    lições dos padrões 2/3, relatório, resumo e Telegram (hermes send).
# Uso: reembalagem.sh [--teste] [--sem-telegram]   (--teste: não grava em youtube.reembalagem, 1 vídeo; LIMITE=2 para 2)
set -u
FAB="$HOME/workspace/fabrica-youtube"
PY="$FAB/tools/.venv/bin/python"
TESTE=0
for a in "$@"; do [ "$a" = --teste ] && TESTE=1; done
DATA=$(date +%F)
LOGD="$HOME/workspace/relatorios/reembalagem/logs"; mkdir -p "$LOGD"
LOG="$LOGD/$DATA$([ $TESTE = 1 ] && echo -teste)-preparar-$(date +%H%M%S).log"
ARGS=(preparar --data "$DATA")
[ $TESTE = 1 ] && ARGS+=(--teste --limite "${LIMITE:-1}")
echo "== $(date -Is) reembalagem.py ${ARGS[*]}" | tee -a "$LOG"
if ! "$PY" "$FAB/tools/rotinas/reembalagem.py" "${ARGS[@]}" >>"$LOG" 2>&1; then
  echo "== preparar FALHOU (o agente relata o erro): $(tail -n 3 "$LOG" | tr '\n' ' ')" | tee -a "$LOG"
fi
exec "$(dirname "$0")/_rotina_claude.sh" reembalagem "$@"
