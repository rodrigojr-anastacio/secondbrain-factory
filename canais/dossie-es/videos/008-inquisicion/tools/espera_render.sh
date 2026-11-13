#!/bin/bash
# Espera o render do outro job terminar (2 vCPU: um render por vez). Padrão ancorado em "^node ": casa só o processo do
# render, nunca a linha do próprio shell (o pgrep -f "[r]emotion" do 1º laço casava o bash que chamava "npx remotion").
# Uso: tools/espera_render.sh [max_s=540] → 0 livre, 1 ainda ocupado. Acumula o tempo esperado em qa/espera.log.
max=${1:-540}; t0=$(date +%s)
while pgrep -f "^node .*remotion (render|still)" >/dev/null; do
  [ $(( $(date +%s) - t0 )) -ge $max ] && { echo "$(date +%T) esperou $(( $(date +%s) - t0 )) s (ainda ocupado)" >> qa/espera.log; exit 1; }
  sleep 10
done
w=$(( $(date +%s) - t0 )); echo "$(date +%T) esperou $w s (livre)" >> qa/espera.log; echo "livre após $w s"; exit 0
