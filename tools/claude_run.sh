#!/usr/bin/env bash
# Atalho para tools/claude_run.py com o Python do tools/.venv. Mesmos argumentos (veja --help).
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$DIR/.venv/bin/python" "$DIR/claude_run.py" "$@"
