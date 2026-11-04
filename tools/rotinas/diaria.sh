#!/bin/bash
# Rotina diária determinística (sem IA): coleta métricas dos nossos canais e faz backup do banco.
set -u
cd "$(dirname "$0")/.."
echo "== $(date -Is) coleta"; .venv/bin/python report.py --coletar
echo "== $(date -Is) backup"
pg_dump -d vida | gzip > ~/backups/vida/vida-$(date +%F).sql.gz && find ~/backups/vida -name "*.sql.gz" -mtime +14 -delete

# Cérebros: commit do que escapou + push para o GitHub (secondbrain-*)
"$HOME/workspace/_infra/git-diario.sh" || echo "git-diario falhou"
