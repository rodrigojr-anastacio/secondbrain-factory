-- Schema ops: operação da vida toda (não só YouTube). Idempotente. Aplicar: psql -d vida -f tools/db/schema_ops.sql
CREATE SCHEMA IF NOT EXISTS ops;

CREATE TABLE IF NOT EXISTS ops.event_log (
    id         bigserial PRIMARY KEY,
    ts         timestamptz NOT NULL DEFAULT now(),
    origem     text NOT NULL,   -- ex.: rotina:tendencias, job_api, batch, preqa
    tipo       text NOT NULL,   -- api_erro, api_credito, teto_atingido, teto_aviso, fallback_max, fallback_ok, fallback_falhou, info
    severidade text NOT NULL DEFAULT 'info' CHECK (severidade IN ('info', 'aviso', 'erro')),
    mensagem   text NOT NULL,
    detalhes   jsonb NOT NULL DEFAULT '{}'::jsonb,  -- status HTTP, modelo, grupo, gasto, teto, duração. NUNCA segredo
    ref        text             -- vídeo / brief
);
CREATE INDEX IF NOT EXISTS event_log_ts_idx ON ops.event_log (ts DESC);
CREATE INDEX IF NOT EXISTS event_log_tipo_idx ON ops.event_log (tipo);
