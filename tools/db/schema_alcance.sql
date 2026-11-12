-- Alcance diário (YouTube Reporting API): impressões e CTR da thumbnail; origem de tráfego. Idempotente.
-- origem = '' quando a linha vem do relatório de alcance sem quebra por origem.
CREATE TABLE IF NOT EXISTS youtube.alcance_diario (
  canal_slug  text NOT NULL REFERENCES youtube.canais(slug),
  video_id    text NOT NULL,
  data        date NOT NULL,
  origem      text NOT NULL DEFAULT '',
  impressoes  bigint,
  ctr         numeric(8,6),          -- fração (0.0402 = 4,02%)
  views       bigint,
  minutos     numeric(14,2),
  fonte       text NOT NULL,         -- tipo de relatório
  baixado_em  timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (canal_slug, video_id, data, origem, fonte)
);
CREATE TABLE IF NOT EXISTS youtube.reporting_jobs (
  canal_slug text NOT NULL, tipo text NOT NULL, job_id text NOT NULL,
  criado_em timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (canal_slug, tipo)
);
CREATE TABLE IF NOT EXISTS youtube.reporting_relatorios (
  report_id text PRIMARY KEY, canal_slug text NOT NULL, tipo text NOT NULL,
  inicio date, fim date, linhas int, baixado_em timestamptz NOT NULL DEFAULT now()
);
