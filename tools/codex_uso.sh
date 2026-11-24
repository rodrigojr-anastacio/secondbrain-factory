#!/usr/bin/env bash
# Resumo por dia do uso do Codex (ChatGPT Plus) para imagens: imagens Codex × fallback, limites e erros, cota e,
# desde 24/11/2026, IMAGENS POR JANELA (o limite de imagem é uma janela de 24 h da 1ª imagem, não o % do 5 h;
# tools/codex_janela.py) + estado atual da janela e do portão da noite.
# Fonte: ops.event_log (origem img_codex; 1 evento codex_lote por execução do tools/img_codex.py) e financas.consumo.
# Uso: tools/codex_uso.sh [dias]   (padrão 14)
set -euo pipefail
DIAS="${1:-14}"
psql -d vida -v dias="$DIAS" <<'SQL'
\echo '== Imagens por dia (img_codex) =='
SELECT ts::date AS dia,
       count(*) FILTER (WHERE tipo = 'codex_lote')                                  AS execucoes,
       coalesce(sum((detalhes->>'codex_ok')::int)      FILTER (WHERE tipo = 'codex_lote'), 0) AS codex,
       coalesce(sum((detalhes->>'fallback_ok')::int)   FILTER (WHERE tipo = 'codex_lote'), 0) AS fal_fallback,
       coalesce(sum((detalhes->>'faltando')::int)      FILTER (WHERE tipo = 'codex_lote'), 0) AS faltando,
       count(*) FILTER (WHERE tipo = 'codex_limite')                                AS limites,
       count(*) FILTER (WHERE tipo = 'codex_erro')                                  AS erros,
       max((detalhes->'cota'->>'pct_5h')::numeric)     FILTER (WHERE tipo = 'codex_lote') AS max_pct_5h,
       max((detalhes->'cota'->>'pct_semana')::numeric) FILTER (WHERE tipo = 'codex_lote') AS max_pct_semana
FROM ops.event_log
WHERE origem = 'img_codex' AND ts > now() - (:'dias' || ' days')::interval
GROUP BY 1 ORDER BY 1 DESC;

\echo '== Imagens por janela de 24 h (codex_limite: até o 429; Hipótese até 3 noites medidas) =='
SELECT to_char((detalhes->>'inicio_janela')::timestamptz, 'DD/MM HH24:MI') AS janela_aberta,
       (detalhes->>'imagens_ate_limite')::int AS imagens_ate_429,
       to_char((detalhes->>'limite_em')::timestamptz, 'DD/MM HH24:MI') AS deu_429,
       to_char((detalhes->>'reset_em')::timestamptz, 'DD/MM HH24:MI') AS reset,
       detalhes->>'reset_fonte' AS fonte, detalhes->>'janela_min' AS janela_min
FROM ops.event_log
WHERE origem = 'img_codex' AND tipo = 'codex_limite' AND detalhes ? 'imagens_ate_limite'
  AND ts > now() - (:'dias' || ' days')::interval
ORDER BY ts DESC;
\echo '(antes do registro: 270, 250 e 196 imagens até o 429 em 16, 22 e 23/11/2026, medidas nos codex_log.jsonl)'

\echo '== Portão da noite e esperas (codex_janela_inicio, codex_portao_liberado, codex_aguarda) =='
SELECT to_char(ts, 'DD/MM HH24:MI') AS quando, tipo, left(mensagem, 120) AS mensagem
FROM ops.event_log
WHERE origem = 'img_codex' AND tipo IN ('codex_janela_inicio', 'codex_portao_liberado', 'codex_aguarda')
  AND ts > now() - (:'dias' || ' days')::interval
ORDER BY ts DESC LIMIT 15;

\echo '== Limites e erros recentes =='
SELECT to_char(ts, 'DD/MM HH24:MI') AS quando, tipo, left(mensagem, 110) AS mensagem
FROM ops.event_log
WHERE origem = 'img_codex' AND tipo IN ('codex_limite', 'codex_limite_lote', 'codex_erro') AND ts > now() - (:'dias' || ' days')::interval
ORDER BY ts DESC LIMIT 15;

\echo '== Volume e custo (financas.consumo): Codex US$ 0 × fal do fallback =='
SELECT ocorrido_em::date AS dia, fornecedor, sum(quantidade) AS imagens, round(sum(custo), 3) AS usd
FROM financas.consumo
WHERE ocorrido_em > now() - (:'dias' || ' days')::interval
  AND (fornecedor = 'OpenAI ChatGPT Plus' OR (fornecedor IN ('fal.ai', 'Google Gemini API') AND notas LIKE 'fallback codex%'))
GROUP BY 1, 2 ORDER BY 1 DESC, 2;
SQL
echo '== Janela atual e portão (tools/codex_janela.py status) =='
"$(dirname "$0")/.venv/bin/python" "$(dirname "$0")/codex_janela.py" status
