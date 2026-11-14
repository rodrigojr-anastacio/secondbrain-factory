#!/usr/bin/env bash
# Fila de jobs claude -p. Uso: tools/fila.sh add [... --agora]|list|tick [--dry-run]|cancel <nome>|retomar <nome>|agora <nome>|capacidade [--backfill]  (janela noturna FILA_JANELA=20-07: ver fila.py)
exec "$(dirname "$(readlink -f "$0")")/.venv/bin/python" "$(dirname "$(readlink -f "$0")")/fila.py" "$@"
