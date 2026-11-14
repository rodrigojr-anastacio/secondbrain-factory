#!/bin/bash
# Fábrica noturna (14/11/2026). Uso: noturna.sh planejar [--dry-run] [--noite AAAA-MM-DD] [--forcar] [--sem-telegram]
#                                   | vigia [--sem-telegram] | manha [--noite AAAA-MM-DD] [--dry-run] [--sem-telegram]
# Timers: fabrica-noturna (dom/ter/qui/sex/sáb 20:00), fabrica-noturna-vigia (10 min), fabrica-noturna-manha (07:30).
# Detalhes: tools/rotinas/noturna.py e tools/rotinas/README.md.
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin"
export TMPDIR="$HOME/cache/tmp"; mkdir -p "$TMPDIR"
unset ANTHROPIC_API_KEY
FAB="$HOME/workspace/fabrica-youtube"
exec "$FAB/tools/.venv/bin/python" "$FAB/tools/rotinas/noturna.py" "$@"
