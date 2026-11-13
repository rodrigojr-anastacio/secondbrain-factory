-- Fila de jobs claude -p (executor: tools/fila.py). Idempotente. Aplicar: psql -d vida -f tools/db/schema_fila.sql
CREATE SCHEMA IF NOT EXISTS ops;
CREATE TABLE IF NOT EXISTS ops.fila_jobs (
    id           serial PRIMARY KEY,
    nome         text NOT NULL UNIQUE,
    brief        text NOT NULL,
    log          text NOT NULL,
    modelo       text NOT NULL DEFAULT 'opus' CHECK (modelo IN ('opus','sonnet')),
    motor        text NOT NULL DEFAULT 'max' CHECK (motor IN ('max','api')),
    prioridade   int  NOT NULL DEFAULT 5,
    prazo        timestamptz,
    depende_de   text,
    status       text NOT NULL DEFAULT 'fila' CHECK (status IN ('fila','rodando','pausado_limite','concluido','bloqueado','falhou','cancelado')),
    unit         text,
    session_id   text,
    retomar_em   timestamptz,
    tentativas   int NOT NULL DEFAULT 0,
    criado_em    timestamptz NOT NULL DEFAULT now(),
    iniciado_em  timestamptz,
    terminado_em timestamptz,
    resumo       text,
    obs          text
);
CREATE INDEX IF NOT EXISTS fila_jobs_status_idx ON ops.fila_jobs (status);

-- Capacidade (13/11/2026): amostras por tick, métricas por job, janelas do Max.
ALTER TABLE ops.fila_jobs
    ADD COLUMN IF NOT EXISTS mem_pico_mb int,
    ADD COLUMN IF NOT EXISTS cpu_seg numeric,
    ADD COLUMN IF NOT EXISTS duracao_seg numeric NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS limites_batidos int NOT NULL DEFAULT 0,
    ADD COLUMN IF NOT EXISTS tokens_entrada bigint,
    ADD COLUMN IF NOT EXISTS tokens_saida bigint,
    ADD COLUMN IF NOT EXISTS tokens_cache_leitura bigint,
    ADD COLUMN IF NOT EXISTS tokens_cache_escrita bigint,
    ADD COLUMN IF NOT EXISTS custo_equivalente_usd numeric(10,4);

CREATE TABLE IF NOT EXISTS ops.fila_amostras (
    id                serial PRIMARY KEY,
    ts                timestamptz NOT NULL DEFAULT now(),
    job_nome          text,            -- null = VPS inteira
    mem_mb            numeric,
    mem_pico_mb       numeric,
    cpu_seg           numeric,
    mem_disponivel_mb numeric,
    swap_usado_mb     numeric,
    load1             numeric,
    jobs_rodando      int,
    disco_livre_gb    numeric
);
CREATE INDEX IF NOT EXISTS fila_amostras_ts_idx ON ops.fila_amostras (ts);
CREATE INDEX IF NOT EXISTS fila_amostras_job_idx ON ops.fila_amostras (job_nome, ts);

CREATE TABLE IF NOT EXISTS ops.max_janelas (
    id              serial PRIMARY KEY,
    detectado_em    timestamptz NOT NULL DEFAULT now(),
    reseta_em       timestamptz,
    tipo            text NOT NULL DEFAULT '5h' CHECK (tipo IN ('5h','semanal')),
    job_nome        text,
    janela_ini      timestamptz,       -- reset anterior (ou detectado_em - 5 h)
    tokens_entrada  bigint,
    tokens_saida    bigint,
    tokens_cache_leitura bigint,
    tokens_cache_escrita bigint,
    custo_equivalente_usd numeric(10,4),
    sessoes         int
);
CREATE UNIQUE INDEX IF NOT EXISTS max_janelas_uni ON ops.max_janelas (job_nome, reseta_em, tipo);
