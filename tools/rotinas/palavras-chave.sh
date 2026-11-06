#!/bin/bash
# Rotina de palavras-chave (systemd: fabrica-palavras-chave.timer, qua 09:30). Roda claude -p com prompts/palavras-chave.md, sem Hermes.
# Uso: palavras-chave.sh [--teste] [--sem-telegram]   (detalhes em _rotina_claude.sh e README.md)
exec "$(dirname "$0")/_rotina_claude.sh" palavras-chave "$@"
