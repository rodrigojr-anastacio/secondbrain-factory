#!/bin/bash
# Rotina de tendencias (systemd: fabrica-tendencias.timer). Roda claude -p com prompts/tendencias.md, sem Hermes.
# Uso: tendencias.sh [--teste] [--sem-telegram]   (detalhes em _rotina_claude.sh e README.md)
exec "$(dirname "$0")/_rotina_claude.sh" tendencias "$@"
