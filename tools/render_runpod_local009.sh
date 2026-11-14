#!/bin/bash
# Render de vídeo Remotion numa GPU alugada no Runpod: o PADRÃO da fábrica para TODO render de vídeo (11/11/2026, Rodrigo).
# Na VPS ficam só stills, thumbs, grades do pré-QA e testes de segundos; VPS = fallback (códigos 2, 3 e 4 abaixo).
# Origem e medições: pesquisa/render-gpu-2026-11/RELATORIO.md. Skill: skills/montagem-render/SKILL.md.
#
# Uso: tools/render_runpod.sh <dir remotion> <composição> <saida.mp4> [quadros a-b]
#   <dir remotion> = pasta do projeto com package.json/package-lock.json (e remotion.config.*); sem [a-b] = vídeo inteiro
# Variáveis (opcionais):
#   VIDEO=<youtube.videos.id>  registra o custo em financas.consumo (fornecedor Runpod, ref_id = vídeo); PROJETO=<canal ou slug>
#   BUNDLE=<dir>               bundle pronto (npx remotion bundle); sem isso o script faz um em /tmp (ENTRY=src/index.jsx se preciso)
#   AMOSTRA_S=10               conferência densa: um quadro a cada N s vira still na VPS e é comparado com o mp4 (480p, LIMIAR_MP4)
#   PROVAS="q1 q2 ..."         quadros da prova no Pod ANTES do render (padrão: 4 das amostras); bom pôr as cenas 3D
#   BLOCO_S=60                 o Pod renderiza em blocos de N s; bloco reprovado é refeito (concorrência / 2) antes de destruir o Pod
#   AUDIO=<wav>                o padrão dos canais (render mudo + mix): junta esse wav na VPS em AAC 192k, vídeo copiado
#                              (= tools/render.sh juntar dos vídeos). AUDIO_AF=<filtro ffmpeg> opcional (Em Relevo: compressor+loudnorm)
#   MUDO=1                     sem áudio. Um dos dois (AUDIO ou MUDO) é obrigatório: áudio dentro da composição NÃO é suportado
#                              (teste de 11/11 com MKV+PCM saiu errado no Pod; nenhum canal usa: todos renderizam mudo + mix.wav)
#   REFS=<dir>                 guarda/reaproveita os stills de referência da VPS (<dir>/<quadro>.png; mesmo bundle!): refação não repete ~8 s/still
#   RFLAGS="..."               flags extras do `remotion render` no Pod (ex.: --offthreadvideo-cache-size-in-bytes=1000000000; Clearance 001, 12/11:
#                              blocos com doc ampliado + filtro CSS estouravam a memória do contêiner e a sessão SSH morria sem log)
#   CONC=8 CRF=18 GPUS=... IMG=... ESPERA_MIN=30 TENTATIVAS_QA=2 LIMIAR=0.95 LIMIAR_MP4=0.95 TETO_S=5400
#
# Passos: (1) stills de referência na VPS (amostras + provas; swangle, ~8 s cada, antes de ligar o Pod: espera não custa);
#   (2) cria o Pod com NVIDIA_DRIVER_CAPABILITIES=all (sem isso não há EGL/GL no contêiner e o Chrome cai em software), lista GPUS em
#   ordem, Community e depois Secure, a cada 60 s até ESPERA_MIN (30 min) → sem GPU = código 4; (3) envia bundle + package.json/lock;
#   na imagem da fábrica (ghcr, IMG padrão) Node/Chrome/node_modules já estão prontos, senão instala (~2 min);
#   (4) PROVA: stills no Pod (angle-egl, Chrome Headless Shell padrão do Remotion; NUNCA chrome-for-testing) × VPS por SSIM;
#   < LIMIAR → destrói e tenta outra máquina (TENTATIVAS_QA = 2) → código 2; (5) render em blocos, mudo, com a memória da GPU amostrada;
#   cada bloco volta e é conferido nas amostras dele (480p, SSIM ≥ LIMIAR_MP4 0,95: bom ≈ 0,97–0,99, quadro escuro ~0,97, defeito
#   0,52–0,93); reprovado → refaz com metade da concorrência (2×); reprovação idêntica nas 2 rodadas = diferença estável (não é a GPU);
#   ainda ruim → código 3; (6) junta os blocos (cópia, sem recodificar), confere o nº de quadros e põe o áudio;
#   (7) DESTRÓI O POD SEMPRE (trap em qualquer saída, erro ou Ctrl-C; apaga também Pod órfão com o mesmo nome) e confere pela API que
#   não sobrou nada; registra custo/h × tempo (saldo antes/depois nas notas).
# Por que a conferência densa: em 11/11 uma 4090 Secure passou nas 5 provas e nos 5 quadros conferidos, mas perdeu a textura satélite
#   (faixas) em trechos do meio do render, sem erro (pesquisa/render-gpu-2026-11/RELATORIO.md, "Rodada completa").
# Códigos: 0 ok · 1 erro · 2 prova reprovada em 2 máquinas · 3 bloco reprovado após refazer · 4 sem GPU. Em 2/3/4 → render na VPS.
# Chave: ~/.segredos/runpod/api_key → arquivo de header temporário (600); nunca vai para log, linha de comando nem git.
# Custo (11/11/2026): RTX 3090 Community US$ 0,22/h, 4090 Secure 0,89/h; vídeo de 12 min com 3D = 15–17 min de Pod ≈ US$ 0,06–0,25.
set -euo pipefail
[ $# -lt 3 ] && { sed -n '2,10p' "$0"; exit 1; }
RAIZ=$(cd "$(dirname "$0")/.." && pwd)
REM=$(realpath "$1"); COMP=$2; OUT=$(realpath -m "$3"); FR=${4:-}
CONC=${CONC:-8}; CRF=${CRF:-18}; LIMIAR=${LIMIAR:-0.95}; LIMIAR_MP4=${LIMIAR_MP4:-0.95}; TETO_S=${TETO_S:-5400}
ESPERA_MIN=${ESPERA_MIN:-30}; TENTATIVAS_QA=${TENTATIVAS_QA:-2}; AMOSTRA_S=${AMOSTRA_S:-10}; BLOCO_S=${BLOCO_S:-60}
NODE_DIR=${NODE_DIR:-$HOME/.hermes/tools/node-26.12.1-linux-x64}
GPUS=${GPUS:-'"NVIDIA GeForce RTX 3090","NVIDIA RTX A5000","NVIDIA GeForce RTX 4090","NVIDIA RTX A4500","NVIDIA RTX A4000","NVIDIA L4"'}
IMG_FABRICA=ghcr.io/rodrigojr-anastacio/fabrica-render-gpu:latest
IMG_BASE=runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04
AUDIO_AF=${AUDIO_AF:-}
[ -n "${AUDIO:-}" ] && { AUDIO=$(realpath "$AUDIO"); [ -s "$AUDIO" ] || { echo "AUDIO não existe: $AUDIO"; exit 1; }; MUDO=1; }
[ -z "${MUDO:-}" ] && { echo "passe AUDIO=<pasta do vídeo>/public/audio/mix.wav (padrão dos canais) ou MUDO=1"; exit 1; }
export PATH=$NODE_DIR/bin:$PATH
STILLS="$RAIZ/tools/remotion_stills.cjs"

T=$(mktemp -d); chmod 700 "$T"; mkdir -p "$T/blocos"; VPSD=${REFS:-$T/vps}; mkdir -p "$VPSD"; VPSD=$(realpath "$VPSD"); POD=""; NOME="rp-render-$(date +%s)-$$"
CUSTO=0; SEG_POD=0; PODS_USADOS=""; S0="?"; T0=0
umask 077; printf 'Authorization: Bearer %s\n' "$(cat ~/.segredos/runpod/api_key)" > "$T/auth"; umask 022
api() { curl -s --max-time 60 -X "$1" "https://rest.runpod.io/v1$2" -H @"$T/auth" -H 'Content-Type: application/json' ${3:+-d "$3"}; }
saldo() { curl -s --max-time 30 https://api.runpod.io/graphql -H @"$T/auth" -H 'Content-Type: application/json' \
  -d '{"query":"query { myself { clientBalance } }"}' | python3 -c "import json,sys;print(round(json.load(sys.stdin)['data']['myself']['clientBalance'],4))" 2>/dev/null || echo "?"; }
log() { echo "[$(date +%H:%M:%S)] $*"; }
pods() { api GET /pods | python3 -c "import json,sys;[print(p['id'],p.get('name','')) for p in json.load(sys.stdin)]" 2>/dev/null || true; }

mata_pod() {  # destrói o Pod atual (e órfãos com o mesmo nome) e soma o custo
  local alvo="$POD" p i s
  for p in $(pods | awk -v n="$NOME" '$2 == n {print $1}'); do [ "$p" != "$POD" ] && alvo="$alvo $p"; done
  for p in $alvo; do for i in 1 2 3 4 5; do api DELETE "/pods/$p" >/dev/null && break; sleep 5; done; done
  if [ -n "$POD" ]; then
    s=$(( $(date +%s) - T0 )); SEG_POD=$((SEG_POD + s))
    CUSTO=$(python3 -c "print(round($CUSTO + ${CPH:-0} * $s / 3600, 4))"); PODS_USADOS="$PODS_USADOS ${GPU_NOME:-?}@${CPH:-?}/h:${s}s"
    log "Pod $POD destruído após $s s (≈ US\$ $(python3 -c "print(round(${CPH:-0} * $s / 3600, 4))"))"
  fi
  POD=""
}
fim() {
  local rc=$?
  set +e
  mata_pod; sleep 5
  local resto np nv s1
  resto=$(pods | awk -v n="$NOME" '$2 == n')
  [ -n "$resto" ] && { sleep 15; mata_pod; resto=$(pods | awk -v n="$NOME" '$2 == n'); }
  np=$(pods | grep -c .); nv=$(api GET /networkvolumes | python3 -c "import json,sys;print(len(json.load(sys.stdin)))" 2>/dev/null || echo "?")
  if [ -n "$resto" ]; then log "ATENÇÃO: Pod deste render ainda existe pela API: $resto. Destrua em runpod.io/console/pods"
  else log "API: nenhum Pod deste render; Pods na conta: $np; volumes: $nv"; fi
  if [ "$SEG_POD" -gt 0 ]; then
    s1=$(saldo)
    log "custo do render ≈ US\$ $CUSTO ($SEG_POD s de Pod;$PODS_USADOS); saldo Runpod $S0 → $s1 (o saldo atualiza com atraso)"
    if [ -n "${VIDEO:-}" ]; then
      psql -d vida -q -v ON_ERROR_STOP=1 -v custo="$CUSTO" -v seg="$SEG_POD" -v vid="$VIDEO" -v proj="${PROJETO:-}" \
        -v serv="render GPU Remotion ($COMP${FR:+ $FR})" -v notas="tools/render_runpod.sh rc=$rc;$PODS_USADOS; saldo $S0 → $s1" <<'SQL' \
        && log "custo registrado em financas.consumo (vídeo $VIDEO)" || log "AVISO: não registrou o custo no banco"
INSERT INTO financas.consumo (dominio, projeto, fornecedor, servico, quantidade, unidade, custo, moeda, custo_brl, ref_tipo, ref_id, notas)
SELECT 'youtube', NULLIF(:'proj', ''), 'Runpod', :'serv', round(:'seg'::numeric / 3600, 2), 'horas', :'custo'::numeric, 'USD',
       :'custo'::numeric * (SELECT brl_por_unidade FROM financas.cambio_pre_pago WHERE fornecedor = 'Runpod'), 'youtube.video', :'vid'::int, :'notas';
SQL
    fi
  fi
  rm -rf "$T"
  exit $rc
}
trap fim EXIT
trap 'exit 1' INT TERM HUP
ssim() { ffmpeg -i "$1" -i "$2" -lavfi ssim -f null - 2>&1 | grep -o 'All:[0-9.]*' | cut -d: -f2; }
ssim480() { ffmpeg -i "$1" -i "$2" -lavfi "[0]scale=480:270:flags=area[a];[1]scale=480:270:flags=area[b];[a][b]ssim" -f null - 2>&1 | grep -o 'All:[0-9.]*' | cut -d: -f2; }
passa() { python3 -c "import sys; sys.exit(0 if float('${1:-0}' or 0) >= ${2:-$LIMIAR} else 1)"; }
espera_vps() { :; }

# ---------- 0. bundle, composição, imagem ----------
if [ -z "${BUNDLE:-}" ]; then
  BUNDLE=$T/bundle; espera_vps; log "fazendo bundle"
  (cd "$REM" && npx remotion bundle ${ENTRY:-} --out-dir="$BUNDLE" >/dev/null 2>&1) || { log "bundle falhou (entrada não achada? passe ENTRY=src/index.jsx)"; exit 1; }
fi
BUNDLE=$(realpath "$BUNDLE")
read -r FPS NTOT <<< "$(node "$STILLS" "$REM" "$BUNDLE" "$COMP" "$T" swangle 1 info 2>/dev/null | tail -1)"
[ -z "${NTOT:-}" ] && { log "não li a composição $COMP"; exit 1; }
A0=0; B0=$((NTOT - 1)); [ -n "$FR" ] && { A0=${FR%-*}; B0=${FR#*-}; }
# blocos e amostras
read -r -a BLOCOS <<< "$(python3 -c "
a,b,n=$A0,$B0,max(1,round($BLOCO_S*$FPS)); l=[[x,min(b,x+n-1)] for x in range(a,b+1,n)]
if len(l)>1 and l[-1][1]-l[-1][0]+1<n//3: u=l.pop(); l[-1][1]=u[1]  # rabo curto entra no bloco anterior
print(' '.join(f'{x}-{y}' for x,y in l))")"
AMOSTRAS=$(python3 -c "
a,b,p=$A0,$B0,max(1,round($AMOSTRA_S*$FPS)); l=list(range(a+min(15,(b-a)//2),b+1,p)); l.append(max(a,b-5)); print(' '.join(str(x) for x in sorted(set(l))))")
[ -z "${PROVAS:-}" ] && PROVAS=$(python3 -c "l='$AMOSTRAS'.split(); k=min(4,len(l)); print(' '.join(l[round(i*(len(l)-1)/max(1,k-1))] for i in range(k)))")
log "$COMP: $FPS fps, quadros $A0–$B0 em ${#BLOCOS[@]} bloco(s); $(echo $AMOSTRAS | wc -w) amostras; provas: $PROVAS"
if [ -z "${IMG:-}" ]; then   # a imagem da fábrica só serve se estiver pública no ghcr (o Runpod puxa sem credencial)
  R=${IMG_FABRICA#ghcr.io/}; R=${R%:*}
  TK=$(curl -s --max-time 20 "https://ghcr.io/token?scope=repository:$R:pull" | python3 -c "import json,sys;print(json.load(sys.stdin).get('token',''))" 2>/dev/null || true)
  C=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 -H "Authorization: Bearer $TK" \
      -H 'Accept: application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.v2+json, application/vnd.oci.image.manifest.v1+json' \
      "https://ghcr.io/v2/$R/manifests/latest" || true)
  if [ "$C" = 200 ]; then IMG=$IMG_FABRICA; else IMG=$IMG_BASE; log "imagem da fábrica indisponível sem credencial (HTTP $C): usando a base + instalação"; fi
fi
log "imagem: $IMG"

# ---------- 1. stills de referência na VPS ----------
espera_vps; t=$(date +%s)
FALTA=$(for q in $(echo $AMOSTRAS $PROVAS | tr ' ' '\n' | sort -nu); do [ -s "$VPSD/$q.png" ] || echo $q; done | paste -sd,)
if [ -n "$FALTA" ]; then
  node "$STILLS" "$REM" "$BUNDLE" "$COMP" "$VPSD" swangle 1 "$FALTA" >/dev/null 2>"$T/stills.err" \
    || { log "stills na VPS falharam: $(tail -3 "$T/stills.err")"; exit 1; }
fi
log "stills de referência na VPS: $(echo "$FALTA" | tr , ' ' | wc -w) novos em $(( $(date +%s) - t )) s${REFS:+ (cache em $REFS)}"
S0=$(saldo); log "saldo Runpod: US\$ $S0"
ssh-keygen -q -t ed25519 -N "" -f "$T/k" -C rp-render

cria() {  # $1 = COMMUNITY | SECURE
  api POST /pods "$(python3 - "$1" "$(cat "$T/k.pub")" "$IMG" "$GPUS" "$NOME" <<'PY'
import json, sys
print(json.dumps({'name': sys.argv[5], 'imageName': sys.argv[3], 'gpuTypeIds': json.loads('[' + sys.argv[4] + ']'),
  'gpuTypePriority': 'custom', 'cloudType': sys.argv[1], 'gpuCount': 1, 'containerDiskInGb': 40, 'volumeInGb': 0,
  'ports': ['22/tcp'], 'supportPublicIp': True,
  'env': {'PUBLIC_KEY': sys.argv[2], 'NVIDIA_DRIVER_CAPABILITIES': 'all'}}))
PY
)"
}
campo() { python3 -c "import json,sys
try: d=json.load(sys.stdin)
except Exception: d={}
print(d.get('$1') or '')"; }

# ---------- 2–4. Pod + prova (até TENTATIVAS_QA máquinas) ----------
S() { ssh "${SSHO[@]}" "$SSH_ALVO" "$@"; }
liga_pod() {
  local fim_espera=$(( $(date +%s) + ESPERA_MIN * 60 )) n=0 R i IP=- PORT=-
  while :; do
    n=$((n + 1))
    R=$(cria COMMUNITY); POD=$(echo "$R" | campo id); [ -n "$POD" ] && break
    R=$(cria SECURE); POD=$(echo "$R" | campo id); [ -n "$POD" ] && break
    [ "$(date +%s)" -ge "$fim_espera" ] && { log "sem GPU após $ESPERA_MIN min ($n tentativas): renderize na VPS"; exit 4; }
    log "sem GPU disponível (tentativa $n): $(echo "$R" | head -c 120)"; sleep 60
  done
  T0=$(date +%s); CPH=$(echo "$R" | campo costPerHr); GPU_NOME=
  log "Pod $POD ($NOME) criado após $n tentativa(s); US\$ $CPH/h"
  for i in $(seq 1 90); do
    read -r IP PORT <<< "$(api GET "/pods/$POD" | python3 -c "import json,sys
try: d=json.load(sys.stdin)
except Exception: d={}
print(d.get('publicIp') or '-', (d.get('portMappings') or {}).get('22') or '-')")"
    [ "$PORT" != "-" ] && [ "$IP" != "-" ] && break; sleep 10
  done
  [ "$PORT" = "-" ] && { log "Pod sem IP/porta em 15 min"; return 1; }
  SSHO=(-i "$T/k" -p "$PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile="$T/kh" -o ConnectTimeout=10 -o ServerAliveInterval=30 -o LogLevel=ERROR)
  SSH_ALVO=root@$IP
  for i in $(seq 1 60); do S true 2>/dev/null && break; sleep 8; done
  S true || { log "SSH não respondeu"; return 1; }
  log "SSH pronto em $(( $(date +%s) - T0 )) s"
}
prepara_pod() {
  local LOCKSHA CFG G
  LOCKSHA=$(sha256sum "$REM/package-lock.json" | cut -d' ' -f1)
  CFG=$(cd "$REM" && ls remotion.config.* 2>/dev/null | head -1 || true)
  tar -cf - --transform "s|^$(basename "$BUNDLE")|bundle|" -C "$(dirname "$BUNDLE")" "$(basename "$BUNDLE")" \
    -C "$REM" package.json package-lock.json $CFG -C "$RAIZ/tools" remotion_stills.cjs \
    | S "mkdir -p /root/proj/remotion && cd /root/proj && tar -xf - && mv package.json package-lock.json $CFG remotion/" || { log "envio falhou"; return 1; }
  if ! S 'test -x /root/node/bin/node'; then   # imagem sem Node (base do Runpod): manda o da VPS
    local NT=$HOME/.cache/fabrica-render/$(basename "$NODE_DIR").tar.xz   # comprimido uma vez só (o xz na VPS custava ~40 s de Pod)
    [ -s "$NT" ] || { mkdir -p "$(dirname "$NT")"; tar -C "$(dirname "$NODE_DIR")" -cJf "$NT.tmp" "$(basename "$NODE_DIR")" && mv "$NT.tmp" "$NT"; }
    S 'tar -xJf - -C /root && mv /root/node-* /root/node' < "$NT" || { log "envio do Node falhou"; return 1; }
  fi
  log "envio ok em $(( $(date +%s) - T0 )) s"
  S "set -e; export PATH=/root/node/bin:\$PATH DEBIAN_FRONTEND=noninteractive; cd /root/proj/remotion
if [ -f /opt/deps/lock.sha256 ] && [ \"\$(cat /opt/deps/lock.sha256)\" = $LOCKSHA ]; then
  ln -s /opt/deps/node_modules node_modules; echo 'deps: node_modules da imagem (mesmo lock)'
else
  if ! dpkg -s libnss3 libgbm1 libegl1 >/dev/null 2>&1; then
    apt-get update -qq >/dev/null 2>&1 || true
    for t in 1 2 3; do apt-get install -y -qq libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2 libegl1 libgl1 libgles2 fonts-liberation > /tmp/apt.log 2>&1 && break; echo \"apt falhou (tentativa \$t): \$(tail -2 /tmp/apt.log)\"; sleep 10; apt-get update -qq >/dev/null 2>&1 || true; done
  fi
  npm ci --no-audit --no-fund --loglevel=error 2>&1 | grep -v 'npm notice' | tail -5; echo 'deps: npm ci (lock diferente do da imagem)'
fi
ls node_modules/@remotion/cli >/dev/null
npx remotion browser ensure >/dev/null 2>&1 || true" || { log "setup falhou"; return 1; }
  log "setup ok em $(( $(date +%s) - T0 )) s"
  G=$(S 'nvidia-smi --query-gpu=name,driver_version --format=csv,noheader' | head -1) || return 1
  log "GPU: $G"; GPU_NOME=${G%%,*}
}
prova_pod() {  # 0 = passou
  local q SS
  S "export PATH=/root/node/bin:\$PATH; mkdir -p /root/proj/provas; node /root/proj/remotion_stills.cjs /root/proj/remotion /root/proj/bundle $COMP /root/proj/provas angle-egl 1 $(echo $PROVAS | tr ' ' ,) >/dev/null 2>/root/proj/provas.err || tail -3 /root/proj/provas.err; cd /root/proj/provas && tar -cf - *.png" | tar -xf - -C "$T/blocos" 2>/dev/null || true
  for q in $PROVAS; do
    SS=$(ssim "$VPSD/$q.png" "$T/blocos/$q.png" 2>/dev/null || true)
    log "prova quadro $q: SSIM ${SS:-erro}"
    passa "$SS" || { log "REPROVADO na prova (quadro $q, SSIM ${SS:-erro} < $LIMIAR): esta máquina não renderiza igual"; cp "$T/blocos/$q.png" "${OUT%.mp4}_prova_${q}_reprovada.png" 2>/dev/null || true; return 1; }
  done
  rm -f "$T"/blocos/*.png
}

OK=0
for tq in $(seq 1 "$TENTATIVAS_QA"); do
  if liga_pod && prepara_pod && prova_pod; then OK=1; break; fi
  mata_pod
  [ -n "${GPU_NOME:-}" ] && GPUS=$(python3 -c "import json,sys;l=json.loads('['+sys.argv[1]+']');g=sys.argv[2];l=[x for x in l if x!=g]+([g] if g in l else []);print(','.join(json.dumps(x) for x in l))" "$GPUS" "$GPU_NOME")
  log "tentativa $tq/$TENTATIVAS_QA falhou"
done
[ $OK = 1 ] || { log "prova reprovou $TENTATIVAS_QA máquinas: renderize na VPS"; exit 2; }

# ---------- 5. render em blocos + conferência densa ----------
QV=$(S "awk '{if(\$1!=\"max\") print int(\$1/\$2)}' /sys/fs/cgroup/cpu.max 2>/dev/null || true"); [ -z "$QV" ] && QV=$(S nproc)
[ "$CONC" -gt "$QV" ] && CONC=$QV
log "concorrência $CONC (vCPU do Pod: $QV)"
render_bloco() {  # $1 = índice, $2 = concorrência → 0 se renderizou e voltou
  local i=$1 c=$2 ab=${BLOCOS[$1]}
  S "export PATH=/root/node/bin:\$PATH; cd /root/proj/remotion
npx remotion render ../bundle $COMP ../b$i.$EXT --frames=$ab --gl=angle-egl --concurrency=$c $CODEC --crf=$CRF --timeout=240000 ${RFLAGS:-} --log=error > ../render_b$i.log 2>&1 & P=\$!
M=0; while kill -0 \$P 2>/dev/null; do m=\$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1); [ \"\$m\" -gt \"\$M\" ] && M=\$m; sleep 2; done
echo \$M > ../gpu_b$i.txt
wait \$P || { echo 'RENDER FALHOU:'; grep -v -E 'dbus|^\\s*at ' ../render_b$i.log | head -20; exit 1; }" || return 1
  S "cat /root/proj/b$i.$EXT" > "$T/blocos/b$i.$EXT" || return 1
}
confere_bloco() {  # $1 = índice → 0 se todas as amostras do bloco passaram
  local i=$1 a=${BLOCOS[$1]%-*} b=${BLOCOS[$1]#*-} q SS ruim=0 lista=""; RUINS=""
  for q in $AMOSTRAS $PROVAS; do
    [ "$q" -lt "$a" ] || [ "$q" -gt "$b" ] && continue
    case " $lista " in *" $q "*) continue;; esac; lista="$lista $q"
    ffmpeg -v error -y -ss "$(python3 -c "print(($q - $a) / $FPS)")" -i "$T/blocos/b$i.$EXT" -frames:v 1 "$T/blocos/q.png"
    SS=$(ssim480 "$VPSD/$q.png" "$T/blocos/q.png" || true)
    passa "$SS" "$LIMIAR_MP4" || { ruim=1; RUINS="$RUINS $q:$(python3 -c "print(round(float('${SS:-0}' or 0),2))")"; log "  bloco $i quadro $q: SSIM ${SS:-erro} < $LIMIAR_MP4"; cp "$T/blocos/q.png" "${OUT%.mp4}_ruim_$q.png" 2>/dev/null || true; }
    echo "$q ${SS:-erro}" >> "$T/ssim.txt"
  done
  return $ruim
}
EXT=mp4; CODEC="--muted"
T_R=$(date +%s); REFEITOS=0; : > "$T/ssim.txt"
for i in "${!BLOCOS[@]}"; do
  c=$CONC; ok=0; ant=""
  for k in 0 1 2; do
    t=$(date +%s)
    render_bloco "$i" "$c" || { log "bloco $i (${BLOCOS[$i]}): render falhou"; c=$(( c > 2 ? c / 2 : 2 )); continue; }
    m=$(S "cat /root/proj/gpu_b$i.txt" 2>/dev/null || echo "?")
    if confere_bloco "$i"; then
      ok=1; log "bloco $i (${BLOCOS[$i]}) ok em $(( $(date +%s) - t )) s (conc $c, pico GPU $m MiB)"; break
    fi
    REFEITOS=$((REFEITOS + 1)); c=$(( c > 2 ? c / 2 : 2 ))
    log "bloco $i (${BLOCOS[$i]}) REPROVADO na conferência (pico GPU $m MiB)"
    if [ -n "$ant" ] && [ "$ant" = "$RUINS" ]; then
      log "  mesma reprovação nas 2 rodadas ($RUINS): diferença estável VPS × GPU, não falha aleatória. Olhe ${OUT%.mp4}_ruim_*.png"; break
    fi
    ant=$RUINS; [ $k -lt 2 ] && log "  refazendo com concorrência $c"
  done
  [ $ok = 1 ] || { log "bloco $i continua reprovado após refazer 2×: renderize na VPS (ou outra máquina)"; exit 3; }
  [ $(( $(date +%s) - T0 )) -gt "$TETO_S" ] && { log "passou do teto de tempo do Pod"; exit 1; }
done
log "render + conferência de ${#BLOCOS[@]} blocos em $(( $(date +%s) - T_R )) s ($REFEITOS refeito(s)); $(wc -l < "$T/ssim.txt") amostras, SSIM 480p mín. $(sort -k2 -n "$T/ssim.txt" | head -1 | cut -d' ' -f2)"
mata_pod   # daqui para frente nada precisa do Pod

# ---------- 6. junta, confere e põe o áudio ----------
mkdir -p "$(dirname "$OUT")"
for i in "${!BLOCOS[@]}"; do echo "file 'b$i.$EXT'"; done > "$T/blocos/lista.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$T/blocos/lista.txt" -c copy "$T/junto.$EXT"
NQ=$(ffprobe -v error -select_streams v:0 -count_packets -show_entries stream=nb_read_packets -of csv=p=0 "$T/junto.$EXT")
log "quadros no vídeo: $NQ (esperado: $((B0 - A0 + 1)))"
[ "$NQ" = $((B0 - A0 + 1)) ] || { log "nº de quadros diferente"; cp "$T/junto.$EXT" "${OUT%.mp4}_bruto.$EXT"; exit 3; }
if [ -n "${AUDIO:-}" ]; then
  ffmpeg -v error -y -i "$T/junto.$EXT" -ss "$(python3 -c "print($A0 / $FPS)")" -i "$AUDIO" -map 0:v -map 1:a -c:v copy ${AUDIO_AF:+-af "$AUDIO_AF" -ar 48000} -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
else
  ffmpeg -v error -y -i "$T/junto.$EXT" -c copy -movflags +faststart "$OUT"
fi
cp "$T/ssim.txt" "${OUT%.mp4}_ssim.txt"
log "RENDER_OK $OUT ($(stat -c %s "$OUT") bytes)"
