#!/bin/bash
# Render do longo 02 em partes (< 10 min cada; um render por vez na VPS) + junção com o mix.
# As partes são alinhadas ao SLOT [ATUALIZAR 12/11] (b19–b21): o slot tem partes só dele, então em 12/11 basta
# re-renderizar essas partes (shared/render.sh slot) e juntar de novo.
# Uso: shared/render.sh plano | <i> | todas | slot | junta    (bundle em work/bundle; refazer com REBUNDLE=1)
set -e
cd "$(dirname "$0")/../remotion"
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
mkdir -p ../work/partes
[ -n "$REBUNDLE" ] && npx remotion bundle --out-dir=../work/bundle >/dev/null 2>&1
python3 - <<'PY'
import json, math
c = json.load(open("../shared/cues.json")); N = math.ceil(c["duracao"] * c["fps"]); Q = 500
s = c.get("slot"); cortes = [0, N]
if s: cortes = [0, round(s["s"] * c["fps"]) - 6, round(s["e"] * c["fps"]) + 6, N]
partes = []
for k in range(len(cortes) - 1):
    a, b = cortes[k], cortes[k + 1]; n = max(1, math.ceil((b - a) / Q)); q = math.ceil((b - a) / n)
    for i in range(n): partes.append({"a": a + i * q, "b": min(b, a + (i + 1) * q) - 1, "slot": bool(s) and k == 1})
json.dump(partes, open("../work/partes/plano.json", "w"))
PY
NP=$(python3 -c "import json;print(len(json.load(open('../work/partes/plano.json'))))")
render_parte() {
  i=$1; read a b <<< $(python3 -c "import json;p=json.load(open('../work/partes/plano.json'))[$i];print(p['a'],p['b'])")
  while pgrep -af "^node .*remotion (render|still)" >/dev/null; do sleep 20; done
  s=$(date +%s)
  npx remotion render ../work/bundle Longo ../work/partes/p$(printf %02d $i).mp4 --frames=$a-$b --gl=swangle --concurrency=2 --muted --crf=18 2>&1 | grep -E -i "error|exception" | head -5 || true
  echo "parte $i ($a-$b de $NP partes): $(( $(date +%s) - s )) s" | tee -a ../work/render-tempos.txt
}
case "$1" in
  meia)   # parte $2 em 2 metades (parte pesada: cada comando < 10 min); $3 = a|b|junta
    i=$2; read a b <<< $(python3 -c "import json;p=json.load(open('../work/partes/plano.json'))[$i];print(p['a'],p['b'])"); m=$(( (a + b) / 2 )); P=$(printf %02d $i)
    while pgrep -af "^node .*remotion (render|still)" >/dev/null; do sleep 20; done
    s=$(date +%s)
    case "$3" in
      a) npx remotion render ../work/bundle Longo ../work/partes/h${P}a.mp4 --frames=$a-$m --gl=swangle --concurrency=2 --muted --crf=18 2>&1 | grep -E -i "error|exception" | head -5 || true;;
      b) npx remotion render ../work/bundle Longo ../work/partes/h${P}b.mp4 --frames=$((m+1))-$b --gl=swangle --concurrency=2 --muted --crf=18 2>&1 | grep -E -i "error|exception" | head -5 || true;;
      junta) printf "file 'h%sa.mp4'\nfile 'h%sb.mp4'\n" $P $P > ../work/partes/h$P.txt; ffmpeg -v error -y -f concat -safe 0 -i ../work/partes/h$P.txt -c copy ../work/partes/p$P.mp4;;
    esac
    echo "parte $i metade $3: $(( $(date +%s) - s )) s" | tee -a ../work/render-tempos.txt;;
  pedaco)   # parte $2 em $4 pedaços; $3 = índice do pedaço (0..$4-1) ou "junta"
    i=$2; n=$4; read a b <<< $(python3 -c "import json;p=json.load(open('../work/partes/plano.json'))[$i];print(p['a'],p['b'])"); P=$(printf %02d $i)
    while pgrep -af "^node .*remotion (render|still)" >/dev/null; do sleep 20; done
    s=$(date +%s)
    if [ "$3" = "junta" ]; then : > ../work/partes/q$P.txt; for k in $(seq 0 $((n-1))); do echo "file 'q${P}_$k.mp4'" >> ../work/partes/q$P.txt; done
      ffmpeg -v error -y -f concat -safe 0 -i ../work/partes/q$P.txt -c copy ../work/partes/p$P.mp4
    else k=$3; q=$(( (b - a + n) / n )); x=$(( a + k * q )); y=$(( a + (k + 1) * q - 1 )); [ $y -gt $b ] && y=$b
      npx remotion render ../work/bundle Longo ../work/partes/q${P}_$k.mp4 --frames=$x-$y --gl=swangle --concurrency=2 --muted --crf=18 2>&1 | grep -E -i "error|exception" | head -5 || true; fi
    echo "parte $i pedaço $3/$n: $(( $(date +%s) - s )) s" | tee -a ../work/render-tempos.txt;;
  plano) cat ../work/partes/plano.json; echo; echo "$NP partes";;
  slot) for i in $(python3 -c "import json;print(' '.join(str(i) for i,p in enumerate(json.load(open('../work/partes/plano.json'))) if p['slot']))"); do render_parte $i; done;;
  junta)
    : > ../work/partes/lista.txt
    for i in $(seq 0 $((NP-1))); do printf "file 'p%02d.mp4'\n" $i >> ../work/partes/lista.txt; done
    ffmpeg -v error -y -f concat -safe 0 -i ../work/partes/lista.txt -i ../audio/mix.wav -map 0:v -map 1:a -c:v copy -af "acompressor=threshold=0.06:ratio=4:attack=4:release=120:makeup=2.5,alimiter=limit=0.89:level=false,loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -shortest -movflags +faststart ../out/video.mp4
    echo "ok out/video.mp4";;
  *) render_parte $1;;
esac
