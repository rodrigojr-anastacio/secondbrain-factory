#!/usr/bin/env bash
# Registra um evento em ops.event_log. Uso: tools/evento.sh <origem> <tipo> <info|aviso|erro> "<mensagem>" [ref]
# Consulta: psql -d vida -c "select * from ops.event_log order by ts desc limit 20"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$DIR/.venv/bin/python" "$DIR/event_log.py" "$@"
