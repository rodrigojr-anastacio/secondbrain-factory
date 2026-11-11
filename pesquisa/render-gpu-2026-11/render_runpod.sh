#!/bin/bash
# Render de um projeto Remotion numa GPU alugada no Runpod (teste de 11/11/2026, RELATORIO.md ao lado).
# Liga um Pod RTX 3090/A5000 (Community; se não houver, Secure), envia bundle + package.json, instala, renderiza
# com --gl=angle-egl (Chrome Headless Shell, NÃO chrome-for-testing), traz o mp4 e DESTRÓI o Pod (trap em qualquer saída).
#
# Uso: render_runpod.sh <dir remotion> <dir bundle> <composição> <saida.mp4> [quadros a-b] [concorrência]
#   ex.: render_runpod.sh pesquisa/canal-clima-2026-11/longo-02/remotion pesquisa/canal-clima-2026-11/longo-02/work/bundle-v2 \
#          LongoV2 /tmp/video_mudo.mp4            (vídeo inteiro, mudo; o áudio é juntado depois, como no render_v2.sh junta)
# Trava de QA (obrigatória): antes do render, PROVAS (quadros; padrão = 3 dentro do trecho) viram stills na VPS (swangle) e no Pod
#   (angle-egl); SSIM < LIMIAR (0,95) em qualquer um → aborta sem renderizar. Motivo: em 11/11 a 3090 Community saiu igual,
#   mas uma 4090 Secure perdeu a textura satélite (SSIM 0,89) sem erro nenhum. Vídeo inteiro: passe PROVAS="q1 q2 ..." (cenas 3D).
# Chave: lida de ~/.segredos/runpod/api_key para um arquivo de header temporário (600); nunca vai para log nem linha de comando.
# Custo de referência: ~US$ 0,22/h (3090 community); vídeo de 12 min = ~15 min de Pod ≈ US$ 0,06 (4090 Secure: ~US$ 0,22).
set -euo pipefail
REM=$(realpath "$1"); BUN=$(realpath "$2"); COMP=$3; OUT=$(realpath -m "$4"); FR=${5:-}; CONC=${6:-16}
NODE_DIR=${NODE_DIR:-$HOME/.hermes/tools/node-26.12.1-linux-x64}
GPUS=${GPUS:-'"NVIDIA GeForce RTX 3090","NVIDIA RTX A5000","NVIDIA RTX A4500","NVIDIA RTX A4000","NVIDIA GeForce RTX 4090"'}   # em ordem; 3090/A5000 às vezes esgotam
IMG=${IMG:-runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04}
LIMIAR=${LIMIAR:-0.95}
if [ -z "${PROVAS:-}" ]; then
  [ -z "$FR" ] && { echo "vídeo inteiro: defina PROVAS=\"quadros com cenas 3D\""; exit 1; }
  A=${FR%-*}; B=${FR#*-}; PROVAS="$((A + 30)) $(( (A + B) / 2 )) $((B - 10))"
fi
TETO_S=${TETO_S:-5400}   # vida máxima do Pod (s); passou disso, destrói e sai

T=$(mktemp -d); chmod 700 "$T"; POD=""
umask 077; printf 'Authorization: Bearer %s\n' "$(cat ~/.segredos/runpod/api_key)" > "$T/auth"; umask 022
api() { curl -s -X "$1" "https://rest.runpod.io/v1$2" -H @"$T/auth" -H 'Content-Type: application/json' ${3:+-d "$3"}; }
log() { echo "[$(date +%H:%M:%S)] $*"; }
destroi() {
  if [ -n "$POD" ]; then
    for i in 1 2 3 4 5; do api DELETE "/pods/$POD" >/dev/null && break; sleep 5; done
    sleep 5; R=$(api GET /pods); log "Pod $POD destruído; pods restantes: $R"
  fi
  rm -rf "$T"
}
trap destroi EXIT
trap 'exit 1' INT TERM

# stills de referência na VPS (antes de ligar o Pod: espera não custa)
export PATH=$NODE_DIR/bin:$PATH
for q in $PROVAS; do
  while pgrep -af "^node .*remotion (render|still)" >/dev/null; do sleep 15; done
  (cd "$REM" && npx remotion still "$BUN" "$COMP" "$T/vps_$q.png" --frame=$q --gl=swangle --timeout=240000 --log=error >/dev/null 2>&1) || { echo "still $q falhou na VPS"; exit 1; }
done
log "stills de referência na VPS: $PROVAS"

ssh-keygen -q -t ed25519 -N "" -f "$T/k" -C rp-render
cria() {  # $1 = COMMUNITY | SECURE
  api POST /pods "$(python3 - "$1" "$(cat "$T/k.pub")" "$IMG" "$GPUS" <<'PY'
import json, sys
print(json.dumps({'name': 'rp-render', 'imageName': sys.argv[3], 'gpuTypeIds': json.loads('[' + sys.argv[4] + ']'),
  'gpuTypePriority': 'custom', 'cloudType': sys.argv[1], 'gpuCount': 1, 'containerDiskInGb': 40, 'volumeInGb': 0,
  'ports': ['22/tcp'], 'supportPublicIp': True,
  # NVIDIA_DRIVER_CAPABILITIES=all monta as libs gráficas (EGL/GLES/Vulkan) no contêiner; sem isso o Chrome cai em software
  'env': {'PUBLIC_KEY': sys.argv[2], 'NVIDIA_DRIVER_CAPABILITIES': 'all'}}))
PY
)"
}
pid_de() { python3 -c "import json,sys;print(json.load(sys.stdin).get('id') or '')" 2>/dev/null || true; }
TENTA=${TENTA:-10}   # estoque com IP público oscila: tenta Community e Secure a cada 60 s
for n in $(seq 1 "$TENTA"); do
  R=$(cria COMMUNITY); POD=$(echo "$R" | pid_de); [ -n "$POD" ] && break
  R=$(cria SECURE); POD=$(echo "$R" | pid_de); [ -n "$POD" ] && break
  log "sem GPU disponível (tentativa $n/$TENTA): $(echo "$R" | head -c 120)"; [ "$n" -lt "$TENTA" ] && sleep 60
done
[ -z "$POD" ] && { log "não criou Pod"; exit 1; }
T0=$(date +%s)
CPH=$(echo "$R" | python3 -c "import json,sys;print(json.load(sys.stdin).get('costPerHr'))"); log "Pod $POD custo/h US\$ $CPH"

IP=""; PORT=""
for i in $(seq 1 60); do
  read IP PORT <<< "$(api GET "/pods/$POD" | python3 -c "import json,sys;d=json.load(sys.stdin);print(d.get('publicIp') or '-', (d.get('portMappings') or {}).get('22') or '-')")"
  [ "$PORT" != "-" ] && [ "$IP" != "-" ] && break; sleep 10
done
[ "$PORT" = "-" ] && { log "Pod sem IP/porta"; exit 1; }
SSHO=(-i "$T/k" -p "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile="$T/kh" -o ConnectTimeout=10 -o ServerAliveInterval=30)
S() { ssh "${SSHO[@]}" root@"$IP" "$@"; }
for i in $(seq 1 40); do S true 2>/dev/null && break; sleep 8; done
log "SSH pronto em $(( $(date +%s) - T0 )) s"

# envio: tar por pipe de ssh (a imagem não tem rsync); só bundle + package.json/lock + config
tar -cf - --transform "s|^$(basename "$BUN")|bundle|" -C "$(dirname "$BUN")" "$(basename "$BUN")" \
  -C "$REM" package.json package-lock.json remotion.config.js | S 'mkdir -p /root/proj/remotion && cd /root/proj && tar -xf - && mv package.json package-lock.json remotion.config.js remotion/'
tar -C "$(dirname "$NODE_DIR")" -cJf - "$(basename "$NODE_DIR")" | S 'tar -xJf - -C /root && mv /root/node-* /root/node'
log "envio ok em $(( $(date +%s) - T0 )) s"

S 'set -e; export DEBIAN_FRONTEND=noninteractive
apt-get update -qq >/dev/null 2>&1 || true
for t in 1 2 3; do apt-get install -y -qq libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 libegl1 libgl1 libgles2 fonts-liberation > /tmp/apt.log 2>&1 && break; echo "apt falhou (tentativa \$t): \$(tail -2 /tmp/apt.log)"; sleep 10; apt-get update -qq >/dev/null 2>&1 || true; done
export PATH=/root/node/bin:$PATH; cd /root/proj/remotion; npm ci --no-audit --no-fund --loglevel=error 2>&1 | tail -5; ls node_modules/@remotion/cli >/dev/null
npx remotion browser ensure >/dev/null 2>&1 || true'
log "setup ok em $(( $(date +%s) - T0 )) s"
[ $(( $(date +%s) - T0 )) -gt "$TETO_S" ] && { log "passou do teto de tempo"; exit 1; }

S 'nvidia-smi --query-gpu=name,driver_version --format=csv,noheader' | sed 's/^/GPU: /'
for q in $PROVAS; do
  S "export PATH=/root/node/bin:\$PATH; cd /root/proj/remotion; npx remotion still ../bundle $COMP ../p_$q.png --frame=$q --gl=angle-egl --timeout=240000 --log=error >/dev/null 2>&1 && cat ../p_$q.png" > "$T/pod_$q.png" || true
  SS=$(ffmpeg -i "$T/vps_$q.png" -i "$T/pod_$q.png" -lavfi ssim -f null - 2>&1 | grep -o 'All:[0-9.]*' | cut -d: -f2)
  log "prova quadro $q: SSIM ${SS:-erro}"
  python3 -c "import sys; sys.exit(0 if float('${SS:-0}') >= $LIMIAR else 1)" || { log "REPROVADO na prova (quadro $q, SSIM ${SS:-erro} < $LIMIAR): esta máquina não renderiza igual; abortando"; cp "$T/pod_$q.png" "${OUT%.mp4}_prova_$q.png" 2>/dev/null || true; exit 2; }
done

# render; amostra a GPU no meio para provar que não caiu em SwiftShader (memória de vídeo > 1 GB)
S "export PATH=/root/node/bin:\$PATH; cd /root/proj/remotion
C=$CONC; Q=\$(awk '{if(\$1!=\"max\") print int(\$1/\$2)}' /sys/fs/cgroup/cpu.max 2>/dev/null); [ -n \"\$Q\" ] && [ \$C -gt \$Q ] && C=\$Q; echo \"concorrência \$C (vCPU do Pod: \${Q:-?})\"
npx remotion render ../bundle $COMP ../out.mp4 ${FR:+--frames=$FR} --gl=angle-egl --concurrency=\$C --muted --crf=18 --timeout=240000 --log=error > ../render.log 2>&1 & P=\$!
M=0; while kill -0 \$P 2>/dev/null; do m=\$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1); [ \"\$m\" -gt \"\$M\" ] && M=\$m; sleep 3; done
echo \"pico de memória da GPU: \$M MiB\"; [ \"\$M\" -lt 1000 ] && echo 'AVISO: GPU parada, pode ter caído em software'
wait \$P || { echo 'RENDER FALHOU:'; grep -v -E 'dbus|^\\s*at ' ../render.log | head -30; exit 1; }; tail -2 ../render.log"
log "render ok em $(( $(date +%s) - T0 )) s"
S 'cat /root/proj/out.mp4' > "$OUT"
log "trouxe $OUT ($(stat -c %s "$OUT") bytes) em $(( $(date +%s) - T0 )) s; custo ≈ US\$ $(python3 -c "print(round($CPH*($(date +%s)-$T0)/3600,3))")"
# conferência pós-render: os quadros de prova dentro do trecho, tirados do mp4, contra os stills da VPS (mp4 crf 18 × png ≈ 0,97–0,99)
A0=${FR%-*}; [ -z "$FR" ] && A0=0; RUIM=0
for q in $PROVAS; do
  [ -n "$FR" ] && { [ $q -lt $A0 ] || [ $q -gt ${FR#*-} ]; } && continue
  ffmpeg -v error -y -i "$OUT" -vf "select=eq(n\,$((q - A0)))" -frames:v 1 "$T/mp4_$q.png"
  SS=$(ffmpeg -i "$T/vps_$q.png" -i "$T/mp4_$q.png" -lavfi ssim -f null - 2>&1 | grep -o 'All:[0-9.]*' | cut -d: -f2)
  log "mp4 quadro $q: SSIM ${SS:-erro}"; python3 -c "import sys; sys.exit(0 if float('${SS:-0}') >= $LIMIAR else 1)" || RUIM=1
done
[ $RUIM = 1 ] && { log "REPROVADO no mp4: quadro diferente da VPS; não use $OUT sem olhar"; exit 3; }
# trap destrói o Pod
