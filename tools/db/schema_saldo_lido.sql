-- Saldo real lido das APIs dos fornecedores + fornecedores inativos para alerta (16/11/2026).
-- Por quê: o Runpod tinha ~US$ 35 de saldo real (API) e o banco só US$ 10 lançados → alerta errado de "saldo baixo".
-- A OpenAI API não é mais usada (imagens do historia-ptbr = ChatGPT Plus/Codex, US$ 0) → o saldo negativo
-- (recarga não lançada) disparava alerta à toa. Idempotente: psql -d vida -f tools/db/schema_saldo_lido.sql
-- ATENÇÃO: ~/workspace/_db/schema_financas.sql tem a versão antiga da view saldo_pre_pago; rode ESTE arquivo
-- depois dele (senão a view volta a ignorar o saldo lido e os inativos).

-- Leituras de saldo direto da API do fornecedor (nunca guarda chave nem resposta crua).
CREATE TABLE IF NOT EXISTS financas.saldo_lido (
  id         bigserial PRIMARY KEY,
  fornecedor text NOT NULL,            -- mesmo nome de financas.lancamentos/consumo ('Runpod')
  moeda      text NOT NULL DEFAULT 'USD',
  saldo      numeric(12,4) NOT NULL,
  lido_em    timestamptz NOT NULL DEFAULT now(),
  fonte      text NOT NULL             -- ex.: 'api graphql myself.clientBalance (tools/rotinas/saldo_lido.py)'
);
CREATE INDEX IF NOT EXISTS saldo_lido_forn_ts ON financas.saldo_lido (fornecedor, lido_em DESC);

-- Fornecedores fora dos alertas (sem apagar histórico de lançamentos/consumo).
CREATE TABLE IF NOT EXISTS financas.fornecedor_status (
  fornecedor   text PRIMARY KEY,
  alerta_ativo boolean NOT NULL DEFAULT true,
  motivo       text,
  desde        date NOT NULL DEFAULT current_date
);
INSERT INTO financas.fornecedor_status (fornecedor, alerta_ativo, motivo, desde)
VALUES ('OpenAI', false, 'API não usada desde 14/11/2026: imagens do historia-ptbr pelo ChatGPT Plus/Codex (US$ 0). Histórico mantido em lancamentos/consumo.', '2026-11-16')
ON CONFLICT (fornecedor) DO NOTHING;

-- Todos os fornecedores pré-pagos (histórico completo, inclusive inativos).
-- saldo = o lido da API (≤ 3 dias) quando houver; senão recarregado − consumido.
CREATE OR REPLACE VIEW financas.saldo_pre_pago_todos AS
WITH calc AS (
  SELECT l.fornecedor, l.moeda, sum(l.valor) AS recarregado,
         coalesce((SELECT sum(c.custo) FROM financas.consumo c WHERE c.fornecedor = l.fornecedor), 0) AS consumido
  FROM financas.lancamentos l WHERE l.recorrencia = 'pre_pago'
  GROUP BY l.fornecedor, l.moeda
),
lido AS (
  SELECT DISTINCT ON (fornecedor) fornecedor, saldo, lido_em
  FROM financas.saldo_lido ORDER BY fornecedor, lido_em DESC
)
SELECT c.fornecedor, c.moeda, c.recarregado, c.consumido,
       CASE WHEN li.lido_em > now() - interval '3 days' THEN li.saldo ELSE c.recarregado - c.consumido END AS saldo,
       c.recarregado - c.consumido AS saldo_calculado,
       li.saldo AS saldo_lido, li.lido_em,
       CASE WHEN li.lido_em > now() - interval '3 days' THEN 'api' ELSE 'calculado' END AS fonte_saldo,
       coalesce(fs.alerta_ativo, true) AS alerta_ativo
FROM calc c
LEFT JOIN lido li ON li.fornecedor = c.fornecedor
LEFT JOIN financas.fornecedor_status fs ON fs.fornecedor = c.fornecedor;

-- A view que as rotinas, o painel e os alertas leem: só fornecedores ativos.
-- As 5 primeiras colunas mantêm nome e ordem antigos (compatível com quem já lia a view).
CREATE OR REPLACE VIEW financas.saldo_pre_pago AS
SELECT fornecedor, moeda, recarregado, consumido, saldo, saldo_calculado, saldo_lido, lido_em, fonte_saldo
FROM financas.saldo_pre_pago_todos WHERE alerta_ativo;
