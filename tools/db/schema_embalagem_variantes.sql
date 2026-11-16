-- 3 pares título+thumb por vídeo, cada thumb de um PADRÃO VISUAL diferente (pedido do Rodrigo, 16/11/2026).
-- Para o "Testar e comparar" do YouTube revelar qual padrão de thumb ganha o clique em cada canal.
-- Quem grava: skill embalagem (proposta, via tools/rotinas/embalagem_variantes.py registrar),
-- pacote-youtube (títulos finais + arquivo), Rodrigo/Métricas (vencedora do Testar e comparar).
-- Quem lê: rotina de métricas (placar por canal) e reembalagem (não repetir padrão que perdeu).
-- Idempotente: psql -d vida -f tools/db/schema_embalagem_variantes.sql

CREATE TABLE IF NOT EXISTS youtube.embalagem_variantes (
  id             bigserial PRIMARY KEY,
  video_id       integer NOT NULL REFERENCES youtube.videos(id),
  letra          char(1) NOT NULL CHECK (letra IN ('A','B','C')),   -- A = T1, B = T2, C = T3 (pareados às thumbs A/B/C)
  origem         text NOT NULL DEFAULT 'embalagem',                 -- embalagem | reembalagem
  titulo         text NOT NULL,
  padrao_titulo  text,                                              -- nome do padrão de título (conhecimento/titulos.md, bíblia)
  padrao_thumb   text NOT NULL,                                     -- eixo visual (vocabulário fechado em skills/embalagem/SKILL.md)
  thumb_conceito text,                                              -- 1 linha: elemento dominante + texto
  thumb_texto    text,                                              -- as ≤ 3 palavras da arte
  thumb_arquivo  text,                                              -- entrega/thumb-<letra>.jpg (relativo à pasta do vídeo)
  vencedora      boolean,                                           -- resultado do "Testar e comparar" (null = sem resultado)
  share_pct      numeric(5,2),                                      -- % de tempo de exibição/participação mostrado no Studio, se o Rodrigo informar
  resultado_em   date,
  notas          text,
  criado_em      timestamptz NOT NULL DEFAULT now(),
  atualizado_em  timestamptz NOT NULL DEFAULT now(),
  UNIQUE (video_id, origem, letra)
);

-- Placar: por canal e padrão de thumb, quantas vezes entrou no teste e quantas venceu.
CREATE OR REPLACE VIEW youtube.padrao_thumb_placar AS
SELECT v.canal_slug, e.padrao_thumb,
       count(*)                                         AS testes,
       count(*) FILTER (WHERE e.vencedora IS NOT NULL)  AS com_resultado,
       count(*) FILTER (WHERE e.vencedora)              AS vitorias,
       round(100.0 * count(*) FILTER (WHERE e.vencedora) / nullif(count(*) FILTER (WHERE e.vencedora IS NOT NULL), 0), 0) AS pct_vitoria,
       round(avg(e.share_pct), 1)                       AS share_medio
FROM youtube.embalagem_variantes e JOIN youtube.videos v ON v.id = e.video_id
GROUP BY v.canal_slug, e.padrao_thumb;

-- Vídeos publicados com 3 variantes e sem vencedora registrada (o Métricas pede ao Rodrigo o resultado do Studio).
CREATE OR REPLACE VIEW youtube.embalagem_sem_resultado AS
SELECT v.id AS video_id, v.canal_slug, v.titulo, v.youtube_id, v.publicado_em,
       string_agg(e.letra || '=' || e.padrao_thumb, ' · ' ORDER BY e.letra) AS variantes
FROM youtube.videos v JOIN youtube.embalagem_variantes e ON e.video_id = v.id
WHERE v.status = 'publicado'
GROUP BY v.id
HAVING bool_and(e.vencedora IS NULL);
