#!/bin/bash
# Espera em primeiro plano até não haver render/still do Remotion (ancorado em ^node: não casa o próprio shell). Máx. $1 s (padrão 540).
lim=${1:-540}; t=0
while pgrep -f "^node .*remotion (render|still)" >/dev/null; do sleep 15; t=$((t+15)); [ $t -ge $lim ] && { echo "AINDA_OCUPADO ${t}s"; exit 1; }; done
echo "LIVRE apos ${t}s"
