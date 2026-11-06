#!/bin/bash
# Roda uma rotina da fábrica pelo Claude Code (claude -p via tools/claude_run.sh), sem depender do Hermes.
# Uso: _rotina_claude.sh <tendencias|metricas|palavras-chave> [--teste] [--sem-telegram]
# Saídas: ~/workspace/relatorios/<rotina>/<data>.md (relatório), <data>-resumo.txt (resumo executivo),
#         logs/<rotina>-<data>.log; resumo entregue no Telegram (home channel do default) por `hermes send`,
#         que usa o token do bot direto, sem LLM e sem gateway. Se o envio falhar, fica só o arquivo.
set -u
ROTINA="${1:?rotina}"; shift
MODO=completo; TELEGRAM=1
for a in "$@"; do
  case "$a" in --teste) MODO=teste ;; --sem-telegram) TELEGRAM=0 ;; *) echo "arg desconhecido: $a" >&2; exit 2 ;; esac
done
export CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0   # -p: espera tarefas de fundo em vez de matá-las após 10 min (redundante com ~/.claude/settings.json)
FAB="$HOME/workspace/fabrica-youtube"
DATA=$(date +%F)
SUF=""; [ "$MODO" = teste ] && SUF="-teste"
OUT="$HOME/workspace/relatorios/$ROTINA"; mkdir -p "$OUT/logs"
REL="$OUT/$DATA$SUF.md"; RESUMO="$OUT/$DATA$SUF-resumo.txt"; LOG="$OUT/logs/$DATA$SUF-$(date +%H%M%S).log"
TIMEOUT=${TIMEOUT:-5400}
PROMPT=$(mktemp); trap 'rm -f "$PROMPT"' EXIT
sed -e "s|{{DATA}}|$DATA|g" -e "s|{{MODO}}|$MODO|g" -e "s|{{RELATORIO}}|$REL|g" -e "s|{{RESUMO}}|$RESUMO|g" \
  "$FAB/tools/rotinas/prompts/$ROTINA.md" > "$PROMPT"
rm -f "$RESUMO"

echo "== $(date -Is) rotina $ROTINA ($MODO) → $REL" | tee -a "$LOG"
"$FAB/tools/claude_run.sh" --etapa "$ROTINA" --cwd "$FAB" --prompt-file "$PROMPT" --modelo sonnet \
  --timeout "$TIMEOUT" --permission-mode bypassPermissions >>"$LOG" 2>&1
RC=$?
echo "== $(date -Is) claude_run saiu com $RC" | tee -a "$LOG"
[ $RC -eq 3 ] && exit 3   # trava ocupada: outra execução da mesma rotina em andamento

# Resumo: o arquivo que o Claude escreveu; senão, o fim do log (texto final do claude)
if [ -s "$RESUMO" ]; then MSG=$(cat "$RESUMO"); else
  MSG="Rotina $ROTINA ($DATA) terminou com código $RC sem resumo. Log: $LOG"$'\n'"$(tail -n 15 "$LOG")"
  printf '%s\n' "$MSG" > "$RESUMO"
fi
[ -s "$REL" ] && MSG="$MSG"$'\n'"MEDIA:$REL"

if [ $TELEGRAM -eq 1 ]; then
  if printf '%s\n' "$MSG" | "$HOME/.local/bin/hermes" send --to telegram --subject "[fábrica] $ROTINA $DATA${SUF:+ (teste)}" --quiet >>"$LOG" 2>&1; then
    echo "== telegram ok" | tee -a "$LOG"
  else
    echo "== telegram FALHOU; ficou só o arquivo $RESUMO" | tee -a "$LOG"
  fi
fi
exit $RC
