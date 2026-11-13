#!/usr/bin/env bash
# Limpeza de disco da VPS (classe A). Uso: tools/limpeza_disco.sh [--dry-run]
exec python3 "$(dirname "$(readlink -f "$0")")/limpeza_disco.py" "$@"
