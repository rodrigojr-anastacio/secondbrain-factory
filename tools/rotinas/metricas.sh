#!/bin/bash
# Rotina de metricas (systemd: fabrica-metricas.timer). Roda claude -p com prompts/metricas.md, sem Hermes.
# Uso: metricas.sh [--teste] [--sem-telegram]   (detalhes em _rotina_claude.sh e README.md)
exec "$(dirname "$0")/_rotina_claude.sh" metricas "$@"
