-- Análises do garimpo em lote (tools/garimpo_batch.py, Batch API). Idempotente.
-- Uma linha por vídeo e lote; reanalisar o mesmo vídeo em outro lote cria outra linha.
CREATE TABLE IF NOT EXISTS youtube.garimpo_analises (
  video_id        text NOT NULL,
  lote            text NOT NULL,
  channel_id      text,
  analisado_em    date NOT NULL,
  modelo          text,
  titulo          text,
  canal           text,
  formula         text,
  gatilho_titulo  text,
  nicho           text,
  idioma          text,
  thumb_elementos text,
  thumb_texto     text,
  thumb_cores     text,
  thumb_personagem text,
  thumb_composicao text,
  hook_frases     text,
  hook_tecnica    text,
  edicao          text,
  modelavel_faceless boolean,
  motivo_modelavel text,
  por_que_funciona text,
  nota_formato    int,
  views           bigint,
  duracao_min     numeric(6,1),
  json_completo   jsonb NOT NULL,
  PRIMARY KEY (video_id, lote)
);
CREATE INDEX IF NOT EXISTS garimpo_analises_canal ON youtube.garimpo_analises (channel_id);
CREATE INDEX IF NOT EXISTS garimpo_analises_nicho ON youtube.garimpo_analises (nicho);
