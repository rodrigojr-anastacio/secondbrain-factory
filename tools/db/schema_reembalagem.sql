-- Rotina semanal de reembalagem (padrão Lutz; tools/rotinas/reembalagem.sh, sáb 02:00). Idempotente. 14/11/2026.
-- youtube.reembalagem: 1 linha por tentativa de reembalagem de um vídeo (sugestão da rotina, reembalagem manual ou o lote de 14/11).
-- Ciclo: sugerido → (troca detectada) aplicado → quarentena 21 d → medido: melhorou (encerrado) | nao_melhorou
--        (1 nova tentativa com padrão diferente, teto 2) → embalagem_nao_e_problema (sai da rotina para sempre).
CREATE TABLE IF NOT EXISTS youtube.reembalagem (
  id               serial PRIMARY KEY,
  youtube_id       text NOT NULL,
  canal_slug       text NOT NULL REFERENCES youtube.canais(slug),
  video_id         int REFERENCES youtube.videos(id),
  tentativa        int NOT NULL DEFAULT 1 CHECK (tentativa BETWEEN 1 AND 2),
  origem           text NOT NULL DEFAULT 'rotina',      -- rotina | reembalagem-2026-11-14 | manual
  padrao_lutz      text,                                -- 1-embalagem | 2-conteudo | 3-tema
  sugerido_em      date NOT NULL,
  relatorio        text,                                -- caminho do relatório da semana
  titulo_antes     text,
  thumb_antes_sha1 text,
  t1               text,
  t2               text,
  padrao_t1        text,
  padrao_t2        text,
  thumb_conceito   text,
  porque           text,
  crivo            text,                                -- ex.: 'aprovado r1 (opus)'
  status           text NOT NULL DEFAULT 'sugerido'
                   CHECK (status IN ('sugerido','aplicado','melhorou','nao_melhorou','embalagem_nao_e_problema','descartado')),
  lembrete_em      date,                                -- quando o lembrete "pendente desde" foi mandado (1×)
  aplicado_em      date,
  detectado_por    text,                                -- titulo | thumb | titulo+thumb | manual | lote
  titulo_depois    text,
  -- métricas: janela "antes" (até a troca) e "depois" (mesmo nº de dias após a troca)
  antes_inicio     date, antes_fim date, antes_impressoes bigint, antes_ctr numeric(6,3), antes_retencao numeric(6,2), antes_fonte text,
  depois_inicio    date, depois_fim date, depois_impressoes bigint, depois_ctr numeric(6,3), depois_retencao numeric(6,2), depois_fonte text,
  medido_em        date,
  notas            text,
  criado_em        timestamptz NOT NULL DEFAULT now(),
  atualizado_em    timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS reembalagem_video_idx ON youtube.reembalagem (youtube_id, sugerido_em DESC);
COMMENT ON COLUMN youtube.reembalagem.antes_ctr IS 'CTR em % (5.84 = 5,84%)';

-- Foto semanal do título e da thumb no ar (Data API videos.list + sha1 da hqdefault/maxres via WARP) para detectar a troca.
CREATE TABLE IF NOT EXISTS youtube.embalagem_snapshot (
  youtube_id  text NOT NULL,
  data        date NOT NULL,
  canal_slug  text NOT NULL,
  titulo      text,
  thumb_url   text,
  thumb_sha1  text,
  privacidade text,
  publicado_em timestamptz,
  PRIMARY KEY (youtube_id, data)
);
