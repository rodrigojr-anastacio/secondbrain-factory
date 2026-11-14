#!/bin/bash
# Rotina diária determinística (sem IA): coleta métricas dos nossos canais e faz backup do banco.
set -u
cd "$(dirname "$0")/.."
echo "== $(date -Is) coleta"; .venv/bin/python report.py --coletar
# Reporting API (impressões/CTR): download diário desde 14/11/2026 (1 relatório por dia e por job; jobs que faltarem são criados).
# O fabrica-analytics.timer também chama reporting.baixar(), sem duplicar (cada relatório é gravado 1× por report_id).
echo "== $(date -Is) reporting"; .venv/bin/python reporting.py --criar-jobs --baixar || echo "reporting falhou"
echo "== $(date -Is) backup"
pg_dump -d vida | gzip > ~/backups/vida/vida-$(date +%F).sql.gz && find ~/backups/vida -name "*.sql.gz" -mtime +14 -delete

# Cérebros: commit do que escapou + push para o GitHub (secondbrain-*)
"$HOME/workspace/_infra/git-diario.sh" || echo "git-diario falhou"
