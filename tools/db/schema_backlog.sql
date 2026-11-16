-- Backlog vivo + calendário de publicação + produção noturna (14/11/2026, decisão do Rodrigo).
-- Idempotente. Aplicar: psql -d vida -f tools/db/schema_backlog.sql
-- Quem grava: tools/rotinas/backlog.py (importar/agendar/sync/md), tools/rotinas/noturna.py (pauta da noite,
-- vigia, resumo da manhã) e a rotina `backlog` (reordenação seg/qui depois do garimpo).

-- Fonte da verdade dos temas de cada canal. O backlog.md do canal é só espelho (seção gerada).
CREATE TABLE IF NOT EXISTS youtube.backlog (
    id               serial PRIMARY KEY,
    canal_slug       text NOT NULL REFERENCES youtube.canais(slug),
    tema             text NOT NULL,
    slug             text NOT NULL,                 -- vira o NNN-<slug> da pasta
    angulo           text,                          -- fio/hook candidato ([I, conferir])
    titulo_candidato text,                          -- ponto de partida; a embalagem + crivo decidem
    evidencias       jsonb NOT NULL DEFAULT '[]',   -- [{tipo, fonte, link, numero, data}]
    demanda          numeric(4,1),                  -- 1–10
    encaixe          numeric(4,1),                  -- 1–10 (bíblia do canal)
    urgencia         numeric(4,1),                  -- 1–10 (janela de tendência; evergreen 3–4)
    nota             numeric(4,1),                  -- (demanda × encaixe × urgência)^(1/3)
    janela_ate       date,                          -- depois disso o tema perdeu a janela (null = evergreen)
    riscos           text,
    status           text NOT NULL DEFAULT 'proposto'
                     CHECK (status IN ('proposto','agendado','em_producao','pronto','publicado','descartado')),
    data_prevista    date,                          -- NOITE DE PRODUÇÃO prevista (sáb/dom/seg/ter 20:00) desde 16/11/2026;
                                                   -- antes era a data de publicação (itens antigos/publicados guardam isso)
    video_id         int REFERENCES youtube.videos(id),
    pasta            text,                          -- pasta do vídeo (relativa ao repo), quando existir
    fonte            text,                          -- arquivo da pesquisa que trouxe o tema
    motivo           text,                          -- motivo da última mudança
    mudou_em         timestamptz NOT NULL DEFAULT now(),
    criado_em        timestamptz NOT NULL DEFAULT now(),
    historico        jsonb NOT NULL DEFAULT '[]',   -- [{em, de, para, motivo}]
    UNIQUE (canal_slug, slug)
);
CREATE INDEX IF NOT EXISTS backlog_canal_status_idx ON youtube.backlog (canal_slug, status);
CREATE INDEX IF NOT EXISTS backlog_data_idx ON youtube.backlog (data_prevista);
-- Dias fixos de produção (16/11/2026, Rodrigo): produção desacoplada da publicação. Quem escolhe o dia de ir ao ar é o
-- Rodrigo; a fábrica só sugere a janela pela noite de produção: sáb → dom ou seg; dom → seg ou qua; seg → qua ou sex;
-- ter → sex ou sáb. Coluna gerada (nunca grave nela); a mesma tabela está em backlog.JANELA.
ALTER TABLE youtube.backlog ADD COLUMN IF NOT EXISTS janela_publicacao text GENERATED ALWAYS AS (
    CASE WHEN status IN ('agendado','em_producao','pronto') THEN
        CASE extract(isodow FROM data_prevista)::int WHEN 6 THEN 'dom ou seg' WHEN 7 THEN 'seg ou qua'
                                                      WHEN 1 THEN 'qua ou sex' WHEN 2 THEN 'sex ou sáb' END
    END) STORED;

-- Fim de semana alternado (sábado numa semana, domingo na outra): registra qual dia valeu em cada semana.
-- APOSENTADA em 16/11/2026 (dias fixos de produção; a publicação é escolha do Rodrigo). Mantida só como histórico.
CREATE TABLE IF NOT EXISTS youtube.calendario_semanas (
    semana_ini date PRIMARY KEY,                    -- segunda-feira
    dia_fds    text NOT NULL CHECK (dia_fds IN ('sab','dom')),
    obs        text,
    criado_em  timestamptz NOT NULL DEFAULT now()
);

-- Uma linha por canal por noite de produção (e por tentativa: 2 = substituto após embalagem reprovada).
CREATE TABLE IF NOT EXISTS youtube.producao_noturna (
    id               serial PRIMARY KEY,
    noite            date NOT NULL,                 -- data da noite (20:00)
    canal_slug       text NOT NULL REFERENCES youtube.canais(slug),
    tentativa        int NOT NULL DEFAULT 1,
    backlog_id       int REFERENCES youtube.backlog(id),
    video_id         int REFERENCES youtube.videos(id),
    data_publicacao  date,                          -- até 15/11/2026: publicação prevista; desde 16/11 NULL (janela = pela noite)
    job_e1           text,
    job_e2           text,
    status           text NOT NULL DEFAULT 'enfileirado'
                     CHECK (status IN ('enfileirado','pronto','embalagem_reprovada','bloqueado','falhou','adiado','cancelado')),
    entrega          text CHECK (entrega IN ('pendente','entregue','sem_espaco','erro')),
    entregue_em      timestamptz,
    avisado_em       timestamptz,                   -- aviso de "sem espaço" já mandado (1×)
    obs              text,
    criado_em        timestamptz NOT NULL DEFAULT now(),
    atualizado_em    timestamptz NOT NULL DEFAULT now(),
    UNIQUE (noite, canal_slug, tentativa)
);

-- Pré-voo de cada noite (saldo fal/Fish/Runpod, Max semanal, Drive, disco) e o que foi cortado.
CREATE TABLE IF NOT EXISTS youtube.noites (
    noite        date PRIMARY KEY,
    preflight    jsonb NOT NULL DEFAULT '{}',
    cortes       jsonb NOT NULL DEFAULT '[]',       -- [{canal, motivo}]
    resumo_manha text,
    manha_em     timestamptz,
    criado_em    timestamptz NOT NULL DEFAULT now()
);
