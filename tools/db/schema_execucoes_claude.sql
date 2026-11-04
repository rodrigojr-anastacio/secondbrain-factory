-- Execuções do Claude Code (claude -p) feitas pela fábrica, uma linha por chamada de tools/claude_run.py.
-- Idempotente: pode rodar de novo sem perder dados.  Aplicar: psql -d vida -f tools/db/schema_execucoes_claude.sql
-- custo_usd_equivalente = total_cost_usd do JSON do claude (preço de lista). No plano Max não é cobrança real:
-- serve para comparar etapas, modelos e vídeos (o Claude Max entra no rateio fixo de financas.custo_por_video).
CREATE SCHEMA IF NOT EXISTS youtube;

CREATE TABLE IF NOT EXISTS youtube.execucoes_claude (
  id                     serial PRIMARY KEY,
  video_id               int REFERENCES youtube.videos(id),   -- NULL em testes sem vídeo
  etapa                  text NOT NULL,                       -- roteiro | storyboard | producao | voz | imagens | montagem-render | thumbnail | pacote-youtube | qa | pesquisa-referencia | teste ...
  modelo                 text NOT NULL,                       -- alias pedido (opus/sonnet) ou id completo
  modelo_real            text,                                -- chave(s) de modelUsage no JSON (ex.: claude-sonnet-5-5)
  session_id             text,
  inicio                 timestamptz NOT NULL,
  fim                    timestamptz,
  duracao_ms             bigint,
  num_turns              int,
  input_tokens           bigint,
  output_tokens          bigint,
  cache_read_tokens      bigint,
  cache_creation_tokens  bigint,
  custo_usd_equivalente  numeric(10,4),
  is_error               boolean,
  subtype                text,                                -- success | error_max_turns | timeout | ...
  resultado              text,                                -- resumo (primeiros ~2000 caracteres do result)
  cwd                    text,
  prompt_resumo          text                                 -- primeiros ~300 caracteres do prompt
);

CREATE INDEX IF NOT EXISTS execucoes_claude_video_idx ON youtube.execucoes_claude (video_id, etapa);
CREATE INDEX IF NOT EXISTS execucoes_claude_inicio_idx ON youtube.execucoes_claude (inicio);

CREATE OR REPLACE VIEW youtube.custo_claude_por_video AS
SELECT e.video_id,
       v.canal_slug,
       v.titulo,
       e.etapa,
       count(*)                          AS execucoes,
       sum(e.duracao_ms) / 60000.0       AS minutos,
       sum(e.num_turns)                  AS turnos,
       sum(e.input_tokens + coalesce(e.cache_read_tokens, 0) + coalesce(e.cache_creation_tokens, 0)) AS tokens_entrada,
       sum(e.output_tokens)              AS tokens_saida,
       sum(e.custo_usd_equivalente)      AS custo_usd_equivalente,
       count(*) FILTER (WHERE e.is_error) AS erros
FROM youtube.execucoes_claude e
LEFT JOIN youtube.videos v ON v.id = e.video_id
WHERE e.etapa <> 'teste' AND e.video_id IS NOT NULL   -- rotinas (tendencias, metricas) não são de um vídeo
GROUP BY e.video_id, v.canal_slug, v.titulo, e.etapa;
