#!/bin/bash
# Roda uma rotina da fábrica com o Claude pela API (Agent SDK, créditos de US$ 100/mês do Max, chave
# ~/.segredos/anthropic/rotinas.env), fora da cota do Claude Max. Desde 12/11/2026; antes era claude -p.
# Uso: _rotina_claude.sh <tendencias|metricas|palavras-chave> [--teste] [--sem-telegram]
# Saídas: ~/workspace/relatorios/<rotina>/<data>.md (relatório), <data>-resumo.txt (resumo executivo),
#         logs/<data>-<hora>.log; resumo entregue no Telegram (home channel do default) por `hermes send`,
#         que usa o token do bot direto, sem LLM e sem gateway. Se o envio falhar, fica só o arquivo.
# Motor: tools/rotinas/rotina_api.py (modelo por rotina; MODELO=<sonnet|haiku|opus> e ORCAMENTO=<US$> sobrescrevem).
#   Se a API falhar, a rotina registra o erro no resumo/Telegram e NÃO chama claude -p sozinha.
#   Só na mão, para comparar ou se a API estiver fora: MOTOR=claude-code tools/rotinas/<rotina>.sh (cota do Max).
# Tendências (modo completo): depois do agente roda tools/garimpo_batch.py (Batch API, padrões em lote).
set -u
ROTINA="${1:?rotina}"; shift
MODO=completo; TELEGRAM=1
for a in "$@"; do
  case "$a" in --teste) MODO=teste ;; --sem-telegram) TELEGRAM=0 ;; *) echo "arg desconhecido: $a" >&2; exit 2 ;; esac
done
export CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS=0
unset ANTHROPIC_API_KEY   # a chave vai só no processo do Agent SDK (rotina_api.py), nunca no ambiente
FAB="$HOME/workspace/fabrica-youtube"
PY="$FAB/tools/.venv/bin/python"
DATA=$(date +%F)
SUF=""; [ "$MODO" = teste ] && SUF="-teste"
OUT="$HOME/workspace/relatorios/$ROTINA"; mkdir -p "$OUT/logs"
REL="$OUT/$DATA$SUF.md"; RESUMO="$OUT/$DATA$SUF-resumo.txt"; LOG="$OUT/logs/$DATA$SUF-$(date +%H%M%S).log"
TIMEOUT=${TIMEOUT:-5400}
MOTOR=${MOTOR:-api}
PROMPT=$(mktemp); trap 'rm -f "$PROMPT"' EXIT
sed -e "s|{{DATA}}|$DATA|g" -e "s|{{MODO}}|$MODO|g" -e "s|{{RELATORIO}}|$REL|g" -e "s|{{RESUMO}}|$RESUMO|g" \
  "$FAB/tools/rotinas/prompts/$ROTINA.md" > "$PROMPT"
rm -f "$RESUMO"

echo "== $(date -Is) rotina $ROTINA ($MODO, motor $MOTOR) → $REL" | tee -a "$LOG"
if [ "$MOTOR" = claude-code ]; then
  "$FAB/tools/claude_run.sh" --etapa "$ROTINA" --cwd "$FAB" --prompt-file "$PROMPT" --modelo sonnet \
    --timeout "$TIMEOUT" --permission-mode bypassPermissions >>"$LOG" 2>&1
else
  ARGS=(--rotina "$ROTINA" --prompt-file "$PROMPT" --timeout "$TIMEOUT")
  [ -n "${MODELO:-}" ] && ARGS+=(--modelo "$MODELO")
  [ -n "${ORCAMENTO:-}" ] && ARGS+=(--orcamento "$ORCAMENTO")
  "$PY" "$FAB/tools/rotinas/rotina_api.py" "${ARGS[@]}" >>"$LOG" 2>&1
fi
RC=$?
echo "== $(date -Is) motor $MOTOR saiu com $RC" | tee -a "$LOG"
[ $RC -eq 3 ] && exit 3   # trava ocupada: outra execução da mesma rotina em andamento

# Garimpo em lote (Batch API): só tendências no modo completo; roda mesmo se o agente falhou (usa o banco)
LINHA_BATCH=""
if [ "$ROTINA" = tendencias ] && { [ "$MODO" = completo ] || [ "${BATCH:-0}" = 1 ]; } && [ "$MOTOR" != claude-code ]; then
  echo "== $(date -Is) garimpo_batch.py" | tee -a "$LOG"
  BJSON=$(cd "$FAB" && "$PY" tools/garimpo_batch.py --espera "${BATCH_ESPERA:-40}" 2>>"$LOG" | tail -n 1)
  BRC=$?
  echo "== garimpo_batch saiu com $BRC: $BJSON" | tee -a "$LOG"
  LINHA_BATCH=$("$PY" -c 'import json,sys
try:
    j=json.loads(sys.argv[1])
except Exception:
    print("Garimpo em lote: falhou (ver log)."); sys.exit()
p=" · lote pendente para a próxima rodada" if j.get("pendentes") else ""
r=(" · " + j["relatorio"]) if j.get("relatorio") else ""
print(f"Garimpo em lote (Batch API): {j[\"analisados\"]} vídeos analisados, US$ {j[\"custo_usd\"]:.2f}{r}{p}.")' "$BJSON")
fi

# Resumo: o arquivo que o Claude escreveu; senão, o fim do log (texto final do claude ou o erro da API)
if [ -s "$RESUMO" ]; then MSG=$(cat "$RESUMO"); else
  MSG="Rotina $ROTINA ($DATA) terminou com código $RC sem resumo (motor $MOTOR; a rotina não chama claude -p sozinha). Log: $LOG"$'\n'"$(grep -v '^\[tool\]\|^\[claude\]\|^\[cli\]' "$LOG" | tail -n 12)"
  printf '%s\n' "$MSG" > "$RESUMO"
fi
if [ -n "$LINHA_BATCH" ]; then
  # MEDIA: fica no fim; a linha do lote entra antes delas
  MSG=$(printf '%s\n' "$MSG" | grep -v '^MEDIA:'; echo "$LINHA_BATCH"; printf '%s\n' "$MSG" | grep '^MEDIA:')
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
