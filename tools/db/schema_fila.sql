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
