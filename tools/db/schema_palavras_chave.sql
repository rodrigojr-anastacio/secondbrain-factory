-- Rotina semanal de palavras-chave (tools/keywords.py, quarta 09:30). Idempotente.
-- Uma linha por (data, idioma, termo, origem). Rodar de novo no mesmo dia sobrescreve a linha.
SET search_path = youtube;

CREATE TABLE IF NOT EXISTS palavras_chave (
  id              serial PRIMARY KEY,
  data            date NOT NULL,
  idioma          text NOT NULL,                 -- en | es | pt | fr
  termo           text NOT NULL,                 -- termo do autocomplete ou n-grama de título (dígitos viram "N")
  origem          text NOT NULL,                 -- autocomplete | titulo
  destino         text,                          -- historia-ptbr | dossie-es | lotr-fr | novo-canal
  -- descoberta
  aparicoes       int,                           -- autocomplete: em quantas listas apareceu; titulo: em quantos títulos
  melhor_posicao  int,                           -- autocomplete: melhor posição (1 = 1ª sugestão)
  score_descoberta numeric(10,2),                -- popularidade relativa (autocomplete: posição e aparições; titulo: views/dia)
  -- validação pela YouTube Data API (só os ~20 melhores; NULL = não validado)
  validado        boolean NOT NULL DEFAULT false,
  mediana_top10   bigint,                        -- mediana de views do top-10 (order=viewCount, últimos 12 meses)
  recentes_100k   int,                           -- vídeos com < 90 dias e > 100 mil views no resultado
  no_molde        int,                           -- vídeos do resultado que já usam um molde nosso ("in minutes", "toda la historia"…)
  amostra         int,                           -- vídeos considerados na validação
  exemplos        jsonb,                         -- top 3 vídeos: id, título, canal, views, publicado
  score           numeric(10,2),                 -- score final (ver tools/keywords.py: pontuar())
  tendencia       text,                          -- novo | subindo | estavel | caindo (contra a execução anterior)
  criado_em       timestamptz NOT NULL DEFAULT now(),
  UNIQUE (data, idioma, termo, origem)
);
CREATE INDEX IF NOT EXISTS palavras_chave_termo ON palavras_chave (idioma, termo);
CREATE INDEX IF NOT EXISTS palavras_chave_data ON palavras_chave (data DESC);


-- 2026-11-06 (acréscimo aprovado pelo Rodrigo): idade e tamanho dos canais que dominam cada termo.
-- Calculado sobre os canais do top-10 útil (channels.list, 1 unidade por termo).
ALTER TABLE palavras_chave ADD COLUMN IF NOT EXISTS canais_top10        int;           -- canais distintos no top-10
ALTER TABLE palavras_chave ADD COLUMN IF NOT EXISTS n_canais_novos      int;           -- canais com < 90 dias (até 06/11/2026: < 12 meses)
ALTER TABLE palavras_chave ADD COLUMN IF NOT EXISTS idade_mediana_meses numeric(6,1);  -- idade mediana dos canais
ALTER TABLE palavras_chave ADD COLUMN IF NOT EXISTS inscritos_mediana   bigint;        -- inscritos medianos dos canais
ALTER TABLE palavras_chave ADD COLUMN IF NOT EXISTS vpi_novos           numeric(10,2); -- mediana de views/inscritos dos vídeos de canais novos
ALTER TABLE palavras_chave ADD COLUMN IF NOT EXISTS porta_aberta        boolean;       -- canal < 90 dias no top-10 com bom desempenho

-- Última execução, melhores primeiro (depois dos ALTERs, para o * pegar as colunas novas)
CREATE OR REPLACE VIEW palavras_chave_ultima AS
SELECT * FROM palavras_chave
WHERE data = (SELECT max(data) FROM palavras_chave)
ORDER BY validado DESC, score DESC NULLS LAST;
