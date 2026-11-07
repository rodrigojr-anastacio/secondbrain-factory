-- Esquema da fábrica do YouTube no banco "vida" (Postgres local da VPS).
-- Idempotente: pode rodar de novo sem perder dados.
CREATE SCHEMA IF NOT EXISTS youtube;
SET search_path = youtube;

-- Nossos canais
CREATE TABLE IF NOT EXISTS canais (
  slug        text PRIMARY KEY,               -- igual à pasta canais/<slug>
  nome        text NOT NULL,
  channel_id  text UNIQUE,                    -- UC… (preenchido na 1ª coleta)
  idioma      text,
  nicho       text,
  status      text NOT NULL DEFAULT 'ativo',  -- preparacao | ativo | pausado | arquivado
  criado_em   timestamptz NOT NULL DEFAULT now()
);

-- Esteira: cada vídeo nosso, da ideia à publicação
CREATE TABLE IF NOT EXISTS videos (
  id            serial PRIMARY KEY,
  canal_slug    text NOT NULL REFERENCES canais(slug),
  numero        int,                          -- NNN da pasta
  titulo        text NOT NULL,
  status        text NOT NULL DEFAULT 'ideia',-- ideia | roteiro | producao | qa | pronto | publicado | arquivado
  pasta         text,                         -- canais/<slug>/videos/NNN-slug
  youtube_id    text UNIQUE,
  publicado_em  date,
  duracao_s     int,
  notas         text,
  criado_em     timestamptz NOT NULL DEFAULT now(),
  atualizado_em timestamptz NOT NULL DEFAULT now(),
  UNIQUE (canal_slug, numero)
);
-- Versão da bíblia de roteiro com que o vídeo foi escrito (comparativo de desempenho entre versões).
-- historia-ptbr: 'v1' = 001–005 (biblia/roteiro-v1.md), 'v2' = 006+ (biblia/roteiro.md, aprovada em 07/11/2026).
-- A skill roteiro grava a versão ao escrever o roteiro. Comparação: canais/historia-ptbr/biblia/README.md.
ALTER TABLE videos ADD COLUMN IF NOT EXISTS biblia_versao text;
UPDATE videos SET biblia_versao = 'v1'
 WHERE canal_slug = 'historia-ptbr' AND numero BETWEEN 1 AND 5 AND biblia_versao IS NULL;

-- Métricas diárias (snapshot do dia) dos nossos canais e vídeos
CREATE TABLE IF NOT EXISTS metricas_canal (
  channel_id text NOT NULL,
  data       date NOT NULL,
  inscritos  int, views bigint, videos int,
  PRIMARY KEY (channel_id, data)
);
CREATE TABLE IF NOT EXISTS metricas_video (
  youtube_id          text NOT NULL,
  data                date NOT NULL,
  views               bigint, likes int, comentarios int,  -- tempo real (Data API)
  media_assistida_s   int, pct_assistido numeric(5,2),     -- Analytics (acumulado desde a publicação; atraso de 1–3 dias)
  minutos_assistidos  bigint, inscritos_ganhos int,
  PRIMARY KEY (youtube_id, data)
);

-- Garimpo de tendências
CREATE TABLE IF NOT EXISTS garimpo_execucoes (
  id            serial PRIMARY KEY,
  executado_em  timestamptz NOT NULL DEFAULT now(),
  buscas        jsonb, criterios jsonb,
  canais_vistos int, candidatos int,
  relatorio_md  text                          -- caminho do .md gerado
);
CREATE TABLE IF NOT EXISTS garimpo_canais (
  channel_id      text PRIMARY KEY,
  titulo          text, url text, pais text,
  criado          date, primeiro_video date,
  primeira_vez    timestamptz NOT NULL DEFAULT now(),
  ultima_vez      timestamptz NOT NULL DEFAULT now(),
  formula         text,                       -- preenchido pela análise (ex.: "What If You Could See X?")
  decisao         text,                       -- investir | testar | descartar
  notas           text
);
CREATE TABLE IF NOT EXISTS garimpo_snapshots (
  execucao_id  int  NOT NULL REFERENCES garimpo_execucoes(id) ON DELETE CASCADE,
  channel_id   text NOT NULL REFERENCES garimpo_canais(channel_id),
  videos int, views bigint, inscritos int, media_views int, score int, idade_dias int,
  PRIMARY KEY (execucao_id, channel_id)
);
CREATE TABLE IF NOT EXISTS garimpo_videos (
  video_id    text PRIMARY KEY,
  channel_id  text NOT NULL REFERENCES garimpo_canais(channel_id),
  titulo text, publicado date, duracao_min numeric(6,1), views bigint, thumb text,
  atualizado_em timestamptz NOT NULL DEFAULT now()
);

-- Vídeos "assistidos" pelo watch.py (hook transcrito, frames, ritmo, anúncios)
CREATE TABLE IF NOT EXISTS assistidos (
  video_id        text PRIMARY KEY,
  titulo text, canal text, idioma text, duracao_s int,
  cortes_por_min  numeric(5,1),
  anuncios        boolean,
  hook            text,
  capitulos       jsonb,
  assets          text,                       -- pasta com thumb, hook_sheet e video_sheet
  analisado_em    timestamptz NOT NULL DEFAULT now()
);

-- Views prontas para consulta
CREATE OR REPLACE VIEW garimpo_crescimento AS
SELECT c.channel_id, c.titulo, c.url, c.formula, c.decisao,
       s.videos, s.views, s.inscritos, s.media_views, e.executado_em,
       s.views - lag(s.views) OVER w AS views_desde_anterior
FROM garimpo_snapshots s
JOIN garimpo_execucoes e ON e.id = s.execucao_id
JOIN garimpo_canais c ON c.channel_id = s.channel_id
WINDOW w AS (PARTITION BY s.channel_id ORDER BY e.executado_em);
