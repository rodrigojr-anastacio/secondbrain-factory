#!/bin/bash
# Render do longo 02 no VISUAL V2 (fase 2, 10/11/2026: mistura A/B de shared/estilo_v2.json + fotos grandes; composição LongoV2).
# Blocos curtos e retomáveis (cada comando < 10 min; um render por vez na VPS). Os cortes seguem o SLOT [ATUALIZAR 12/11] (b19–b21):
# os blocos do slot são só dele, então em 12/11 basta re-renderizar o slot e juntar de novo.
# Uso: shared/render_v2.sh plano | continua [segundos] | slot | junta     (bundle em work/bundle-v2; refazer com REBUNDLE=1)
#   continua: renderiza os blocos que faltam até passar do limite (padrão 400 s) e sai; rode de novo até "faltam 0"
#   slot:     apaga os blocos do slot e marca para refazer; depois rode "continua" até "faltam 0" e "junta"
set -e
cd "$(dirname "$0")/../remotion"
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
D=../work/partes_v2; mkdir -p $D
if [ -n "$REBUNDLE" ] || [ ! -d ../work/bundle-v2 ]; then npx remotion bundle --out-dir=../work/bundle-v2 >/dev/null 2>&1; fi
Q=${Q:-120}
python3 - "$Q" <<'PY'
import json, math, sys
Q = int(sys.argv[1])
c = json.load(open("../shared/cues.json")); N = math.ceil(c["duracao"] * c["fps"])
s = c.get("slot"); cortes = [0, N]
if s: cortes = [0, round(s["s"] * c["fps"]) - 6, round(s["e"] * c["fps"]) + 6, N]
bl = []
for k in range(len(cortes) - 1):
    a, b = cortes[k], cortes[k + 1]; n = max(1, math.ceil((b - a) / Q)); q = math.ceil((b - a) / n)
    for i in range(n): bl.append({"a": a + i * q, "b": min(b, a + (i + 1) * q) - 1, "slot": bool(s) and k == 1})
json.dump(bl, open("../work/partes_v2/plano.json", "w"))
PY
NB=$(python3 -c "import json;print(len(json.load(open('$D/plano.json'))))")
faltam() { n=0; for i in $(seq 0 $((NB-1))); do [ -s $D/b$(printf %03d $i).mp4 ] || n=$((n+1)); done; echo $n; }
case "$1" in
  plano) cat $D/plano.json; echo; echo "$NB blocos; faltam $(faltam)";;
  continua)
    LIM=${2:-400}; T0=$(date +%s)
    for i in $(seq 0 $((NB-1))); do
      f=$D/b$(printf %03d $i).mp4; [ -s $f ] && continue
      [ $(( $(date +%s) - T0 )) -gt $LIM ] && break
      read a b <<< $(python3 -c "import json;p=json.load(open('$D/plano.json'))[$i];print(p['a'],p['b'])")
      while pgrep -af "^node .*remotion (render|still)" >/dev/null; do sleep 15; done
      s=$(date +%s)
      npx remotion render ../work/bundle-v2 LongoV2 $D/tmp.mp4 --frames=$a-$b --gl=swangle --concurrency=2 --muted --crf=18 --timeout=240000 2>&1 | grep -E -i "error|exception" | head -5 || true
      if [ -s $D/tmp.mp4 ]; then mv $D/tmp.mp4 $f; fi
      echo "bloco $i ($a-$b): $(( $(date +%s) - s )) s" | tee -a ../work/render-v2-tempos.txt
    done
    echo "faltam $(faltam) de $NB blocos";;
  pedaco)   # bloco pesado $2 em $4 pedaços; $3 = índice do pedaço (0..$4-1) ou "junta" (vira o bNNN.mp4)
    i=$2; n=$4; B=$(printf %03d $i); read a b <<< $(python3 -c "import json;p=json.load(open('$D/plano.json'))[$i];print(p['a'],p['b'])")
    while pgrep -af "^node .*remotion (render|still)" >/dev/null; do sleep 15; done
    s=$(date +%s)
    if [ "$3" = "junta" ]; then : > $D/q$B.txt; for k in $(seq 0 $((n-1))); do echo "file 'q${B}_$k.mp4'" >> $D/q$B.txt; done
      ffmpeg -v error -y -f concat -safe 0 -i $D/q$B.txt -c copy $D/b$B.mp4
    else k=$3; q=$(( (b - a + n) / n )); x=$(( a + k * q )); y=$(( a + (k + 1) * q - 1 )); [ $y -gt $b ] && y=$b
      npx remotion render ../work/bundle-v2 LongoV2 $D/q${B}_$k.mp4 --frames=$x-$y --gl=swangle --concurrency=2 --muted --crf=18 --timeout=240000 2>&1 | grep -E -i "error|exception" | head -5 || true; fi
    echo "bloco $i pedaço $3/$n: $(( $(date +%s) - s )) s" | tee -a ../work/render-v2-tempos.txt;;
  slot)
    for i in $(python3 -c "import json;print(' '.join(str(i) for i,p in enumerate(json.load(open('$D/plano.json'))) if p['slot']))"); do rm -f $D/b$(printf %03d $i).mp4; done
    echo "slot apagado; faltam $(faltam): rode 'continua' até faltam 0 e depois 'junta'";;
  junta)
    [ "$(faltam)" = 0 ] || { echo "ainda faltam $(faltam) blocos"; exit 1; }
    : > $D/lista.txt; for i in $(seq 0 $((NB-1))); do printf "file 'b%03d.mp4'\n" $i >> $D/lista.txt; done
    ffmpeg -v error -y -f concat -safe 0 -i $D/lista.txt -i ../audio/mix.wav -map 0:v -map 1:a -c:v copy -af "acompressor=threshold=0.06:ratio=4:attack=4:release=120:makeup=2.5,alimiter=limit=0.89:level=false,loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart ../out/video.mp4
    echo "ok out/video.mp4";;
  *) echo "uso: $0 plano | continua [s] | slot | junta"; exit 1;;
esac
