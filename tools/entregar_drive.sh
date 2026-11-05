#!/usr/bin/env bash
# Uso: tools/entregar_drive.sh <canal_slug> <pasta_do_video | identidade>
#   ex.: tools/entregar_drive.sh dossie-es 001-cia   (sobe canais/dossie-es/videos/001-cia/entrega/)
#        tools/entregar_drive.sh dossie-es identidade (sobe canais/dossie-es/identidade/)
# Destino: Drive do Rodrigo, Youtube/<nome do canal>/<NNN-slug>/ via rclone (remote "gdrive").
# Só copia (nunca apaga nada no Drive). Autorização do rclone: ver BLOQUEIO-drive.md.
set -euo pipefail
export PATH="$HOME/.local/bin:$PATH"
slug="${1:?canal_slug}"; item="${2:?pasta_do_video ou identidade}"
raiz="$(cd "$(dirname "$0")/.." && pwd)"
canal="$raiz/canais/$slug"
nome="$(sed -n 's/^nome:[[:space:]]*\([^#]*[^# ]\).*/\1/p' "$canal/canal.yaml" | head -1)"
[ -n "$nome" ] || { echo "sem 'nome:' em $canal/canal.yaml" >&2; exit 1; }
if [ "$item" = identidade ]; then src="$canal/identidade"; else src="$canal/videos/$item/entrega"; fi
[ -d "$src" ] || { echo "não existe: $src" >&2; exit 1; }
if ! rclone listremotes | grep -qx 'gdrive:'; then
  echo "remote rclone 'gdrive' não configurado: veja BLOQUEIO-drive.md (autorização do Rodrigo)" >&2; exit 2
fi
dest="gdrive:Youtube/$nome/$item"
echo "$src -> $dest"
rclone copy "$src" "$dest" --exclude 'base/**' --exclude 'fontes/**' --exclude 'tools/**' \
  --drive-chunk-size 64M --transfers 2 --progress --stats-one-line
rclone lsl "$dest" | head -50
