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
  atualizado_em timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (video_id, ratio)
);
CREATE TABLE IF NOT EXISTS youtube.analytics_trafego (
  canal_slug text NOT NULL, video_id text NOT NULL, data date NOT NULL, origem text NOT NULL,
  views bigint, minutos numeric(14,2), atualizado_em timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (video_id, data, origem)
);
-- detalhe acumulado desde o 1º dia (snapshot substituído a cada rodada). tipo = RELATED_VIDEO | YT_SEARCH | EXT_URL ...
CREATE TABLE IF NOT EXISTS youtube.analytics_trafego_detalhe (
  canal_slug text NOT NULL, video_id text NOT NULL, tipo text NOT NULL, detalhe text NOT NULL,
  views bigint, minutos numeric(14,2),
  detalhe_titulo text, detalhe_canal text,   -- RELATED_VIDEO: título e canal do vídeo que nos sugere
  atualizado_em timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (video_id, tipo, detalhe)
);
-- público acumulado. video_id = '' para o canal inteiro. dimensao: ageGroup_gender, country, city, deviceType, ...
CREATE TABLE IF NOT EXISTS youtube.analytics_publico (
  canal_slug text NOT NULL, video_id text NOT NULL DEFAULT '', dimensao text NOT NULL, chave text NOT NULL,
  views bigint, minutos numeric(14,2), viewer_pct numeric(8,4),
  atualizado_em timestamptz NOT NULL DEFAULT now(),
  PRIMARY KEY (canal_slug, video_id, dimensao, chave)
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
