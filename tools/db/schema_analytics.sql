-- Analytics completo (YouTube Analytics API v2). Idempotente; upsert por chave natural.
CREATE TABLE IF NOT EXISTS youtube.analytics_video_dia (
  canal_slug text NOT NULL, video_id text NOT NULL, data date NOT NULL,
  views bigint, engaged_views bigint, minutos numeric(14,2), duracao_media_s numeric(10,2), pct_media numeric(8,4),
  inscritos_ganhos int, inscritos_perdidos int, likes int, dislikes int, comentarios int, compartilhamentos int,
  adicionados_playlist int, card_cliques int, card_impressoes int, card_ctr numeric(8,6),
  atualizado_em timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (video_id, data)
);
CREATE TABLE IF NOT EXISTS youtube.analytics_retencao (
  canal_slug text NOT NULL, video_id text NOT NULL, ratio numeric(6,4) NOT NULL,
  audiencia_ratio numeric(10,6), retencao_relativa numeric(10,6),
  lido_em date NOT NULL DEFAULT current_date, rodada timestamptz NOT NULL DEFAULT now(),
  atualizado_em timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (video_id, ratio, lido_em)
);
CREATE TABLE IF NOT EXISTS youtube.analytics_trafego (
  canal_slug text NOT NULL, video_id text NOT NULL, data date NOT NULL, origem text NOT NULL,
  views bigint, minutos numeric(14,2), atualizado_em timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (video_id, data, origem)
);
-- detalhe acumulado desde o 1º dia; cada leitura (lido_em) é um snapshot novo, nada é sobrescrito. tipo = RELATED_VIDEO | YT_SEARCH | EXT_URL ...
CREATE TABLE IF NOT EXISTS youtube.analytics_trafego_detalhe (
  canal_slug text NOT NULL, video_id text NOT NULL, tipo text NOT NULL, detalhe text NOT NULL,
  views bigint, minutos numeric(14,2),
  detalhe_titulo text, detalhe_canal text,   -- RELATED_VIDEO: título e canal do vídeo que nos sugere
  lido_em date NOT NULL DEFAULT current_date, rodada timestamptz NOT NULL DEFAULT now(),
  atualizado_em timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (video_id, tipo, detalhe, lido_em)
);
-- público acumulado. video_id = '' para o canal inteiro. dimensao: ageGroup_gender, country, city, deviceType, ...
CREATE TABLE IF NOT EXISTS youtube.analytics_publico (
  canal_slug text NOT NULL, video_id text NOT NULL DEFAULT '', dimensao text NOT NULL, chave text NOT NULL,
  views bigint, minutos numeric(14,2), viewer_pct numeric(8,4),
  lido_em date NOT NULL DEFAULT current_date, rodada timestamptz NOT NULL DEFAULT now(),
  atualizado_em timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (canal_slug, video_id, dimensao, chave, lido_em)
);
CREATE TABLE IF NOT EXISTS youtube.analytics_receita (
  canal_slug text NOT NULL, data date NOT NULL, receita_usd numeric(14,4), cpm_usd numeric(10,4),
  atualizado_em timestamptz NOT NULL DEFAULT now(), PRIMARY KEY (canal_slug, data)
);
-- totais acumulados por rodada, para "mudança desde a última rodada"
CREATE TABLE IF NOT EXISTS youtube.analytics_rodadas (
  rodada timestamptz NOT NULL DEFAULT now(), canal_slug text NOT NULL,
  views bigint, minutos numeric(14,2), inscritos_liquidos int, videos int,
  PRIMARY KEY (rodada, canal_slug)
);

-- Migração idempotente (11/11/2026): as 3 tabelas de snapshot passam a guardar histórico (lido_em na chave).
DO $mig$
DECLARE t text; pk text; novo text;
BEGIN
  FOREACH t IN ARRAY ARRAY['analytics_retencao','analytics_publico','analytics_trafego_detalhe'] LOOP
    EXECUTE format('ALTER TABLE youtube.%I ADD COLUMN IF NOT EXISTS lido_em date', t);
    EXECUTE format('ALTER TABLE youtube.%I ADD COLUMN IF NOT EXISTS rodada timestamptz', t);
    EXECUTE format('UPDATE youtube.%I SET lido_em = DATE ''2026-11-11'' WHERE lido_em IS NULL', t);
    EXECUTE format('UPDATE youtube.%I SET rodada = atualizado_em WHERE rodada IS NULL', t);
    EXECUTE format('ALTER TABLE youtube.%I ALTER COLUMN lido_em SET DEFAULT current_date, ALTER COLUMN lido_em SET NOT NULL', t);
    EXECUTE format('ALTER TABLE youtube.%I ALTER COLUMN rodada SET DEFAULT now(), ALTER COLUMN rodada SET NOT NULL', t);
    SELECT pg_get_constraintdef(oid) INTO pk FROM pg_constraint WHERE contype='p' AND conrelid = ('youtube.'||t)::regclass;
    IF pk NOT LIKE '%lido_em%' THEN
      novo := CASE t WHEN 'analytics_retencao' THEN 'video_id, ratio, lido_em'
                     WHEN 'analytics_publico' THEN 'canal_slug, video_id, dimensao, chave, lido_em'
                     ELSE 'video_id, tipo, detalhe, lido_em' END;
      EXECUTE format('ALTER TABLE youtube.%I DROP CONSTRAINT %I', t, t||'_pkey');
      EXECUTE format('ALTER TABLE youtube.%I ADD PRIMARY KEY (%s)', t, novo);
    END IF;
  END LOOP;
END
$mig$;

-- contador atual + status por vídeo (Data API), 1 linha por vídeo por rodada
CREATE TABLE IF NOT EXISTS youtube.videos_contador (
  canal_slug text NOT NULL, video_id text NOT NULL, lido_em timestamptz NOT NULL DEFAULT now(),
  status text, publish_at timestamptz, views bigint, likes bigint, comentarios bigint,
  PRIMARY KEY (video_id, lido_em)
);
