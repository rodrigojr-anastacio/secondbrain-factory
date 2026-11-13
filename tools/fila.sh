#!/usr/bin/env bash
# Fila de jobs claude -p. Uso: tools/fila.sh add|list|tick [--dry-run]|cancel <nome>|retomar <nome>
exec "$(dirname "$(readlink -f "$0")")/.venv/bin/python" "$(dirname "$(readlink -f "$0")")/fila.py" "$@"
