-- Exportações manuais do YouTube Studio (Modo avançado → Conteúdo), enviadas pelo Rodrigo ~2x/semana.
-- CTR e impressões só existem no Studio (ou na Reporting API, não usada). Idempotente.
CREATE TABLE IF NOT EXISTS youtube.studio_video (
  exportado_em      date    NOT NULL,          -- dia da exportação
  periodo_inicio    date    NOT NULL,
  periodo_fim       date    NOT NULL,
  canal_slug        text    NOT NULL REFERENCES youtube.canais(slug),
  youtube_id        text    NOT NULL,
  views             integer,
  horas_exibicao    numeric(10,4),
  inscritos         integer,
  media_assistida_s integer,
  impressoes        integer,
  ctr_pct           numeric(5,2),
  PRIMARY KEY (exportado_em, youtube_id, periodo_inicio)
);
CREATE OR REPLACE VIEW youtube.studio_ultimo AS
SELECT DISTINCT ON (youtube_id) * FROM youtube.studio_video ORDER BY youtube_id, exportado_em DESC;
ALTER TABLE youtube.studio_video ADD COLUMN IF NOT EXISTS espectadores_unicos integer;
ALTER TABLE youtube.studio_video ADD COLUMN IF NOT EXISTS pct_visualizada numeric(5,2);
