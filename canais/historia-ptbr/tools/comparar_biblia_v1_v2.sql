-- Comparativo v1 × v2 do historia-ptbr: último snapshot de cada vídeo e no dia 7 após publicar
WITH ult AS (
  SELECT DISTINCT ON (m.youtube_id) m.* FROM youtube.metricas_video m ORDER BY m.youtube_id, m.data DESC
), d7 AS (
  SELECT DISTINCT ON (m.youtube_id) m.youtube_id, m.views AS views_d7, m.pct_assistido AS pct_d7
  FROM youtube.metricas_video m JOIN youtube.videos v USING (youtube_id)
  WHERE m.data <= v.publicado_em + 7 ORDER BY m.youtube_id, m.data DESC
)
SELECT v.biblia_versao AS versao, v.numero, left(v.titulo, 40) AS titulo, v.publicado_em,
       current_date - v.publicado_em AS dias, round(v.duracao_s / 60.0, 1) AS min,
       u.views, d7.views_d7, u.pct_assistido, d7.pct_d7, u.media_assistida_s, u.inscritos_ganhos
FROM youtube.videos v
JOIN ult u USING (youtube_id) LEFT JOIN d7 USING (youtube_id)
WHERE v.canal_slug = 'historia-ptbr' AND v.biblia_versao IS NOT NULL
ORDER BY v.numero;

-- Resumo por versão (média e mediana; só vídeos com ≥ 7 dias no ar)
WITH ult AS (
  SELECT DISTINCT ON (youtube_id) * FROM youtube.metricas_video ORDER BY youtube_id, data DESC
)
SELECT v.biblia_versao AS versao, count(*) AS videos,
       round(avg(u.views)) AS views_media,
       percentile_cont(0.5) WITHIN GROUP (ORDER BY u.views) AS views_mediana,
       round(avg(u.pct_assistido), 1) AS pct_assistido_medio,
       round(avg(u.media_assistida_s)) AS media_assistida_s
FROM youtube.videos v JOIN ult u USING (youtube_id)
WHERE v.canal_slug = 'historia-ptbr' AND v.biblia_versao IS NOT NULL
  AND v.publicado_em <= current_date - 7
GROUP BY 1 ORDER BY 1;
