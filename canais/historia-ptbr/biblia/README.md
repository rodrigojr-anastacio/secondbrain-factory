# Bíblia: História em minutos (historia-ptbr)

> **⚠️ v3 PROPOSTA (28/11/2026), aguarda aprovação do Rodrigo: o canal muda de "história de país" para "como era viver / você não sobreviveria".** Decisão do Rodrigo (28/11): bonequinhos, Brasil no centro quando fizer sentido, 1 vídeo/semana, 12–15 min, **nome do canal continua "História em minutos"**; série de países encerrada. Método dele: canal-base gringo muito bombado com a **forma** modelada (nunca o texto; detector de similaridade + crivo de ângulo), título/palavra-chave que o nicho demanda e thumbs fortes.
> - **Canal-base:** **Chat History** ("Why You Wouldn't Survive…", 1,15 mi de inscritos, série com mediana ~2 mi, bonequinhos 2D); reserva **Bernard** ("Why It Sucks to Be a…"); referência de contador/título **Fossil** (13,6 mi). Estudo: `../v3-proposta/ANATOMIA-canal-base.md`.
> - **Arquivos v3:** [`roteiro.md`](roteiro.md) (esqueleto de 8 passos em 2ª pessoa, dispositivos nossos: Turista, Despachante do Tempo, cronômetro "VOCÊ DUROU"), [`titulo.md`](titulo.md), [`thumb.md`](thumb.md), seções "v3 PROPOSTA" no fim de [`visual.md`](visual.md) e [`voz.md`](voz.md). Pesquisa pt: `../v3-proposta/PT-TITULOS-DEMANDA.md`; backlog: `../backlog-v3-proposta.md`; amostra: `../v3-proposta/amostra-001-rio-1808/`.
> - **Histórico preservado:** v1 = `roteiro-v1.md` (001–005); v2 = `roteiro-v2.md`, `titulo-v2.md`, `thumb-v2.md` (006–017, países). O texto abaixo desta caixa descreve a série de países (v1/v2) e vale só como histórico; o "O que NÃO fazer aqui" (políticas, capítulos-objeto, identidade do Dossier) continua valendo na v3.
> - **Critério do teste (decisão de portfólio, 28/11):** 4 vídeos até 10/01/2027; passa se 1 fizer ≥ 3 mil views em 7 d com CTR ≥ 4% no lançamento e a mediana ≥ 800 em 7 d; senão encerra. `biblia_versao = 'v3'` nos vídeos novos.

**Canal-modelo:** History in Minutes (UCYjRQ6T2BxBnJtPytI9OnNg), com Genius History como 2º modelo. Idioma pt-BR. Configuração técnica (voz, gerador, `estilo_prompt`) em `../canal.yaml`.
**O que é deste canal:** a história INTEIRA de um país ou império contada como **narrativa contínua**: um fio condutor, eras ligadas por causa → consequência ("mas… então…"), loops "guarde isso" pagos lá na frente, bonequinhos de cabeça redonda em cartoon chapado e um narrador que *conta* (não lista).
**Arquivos (v2, histórico):** [`roteiro-v2.md`](roteiro-v2.md) · [`titulo-v2.md`](titulo-v2.md) · [`thumb-v2.md`](thumb-v2.md) · [`visual.md`](visual.md) · [`voz.md`](voz.md). Esta bíblia **prevalece** sobre `conhecimento/` (só regras gerais).
**O que NÃO fazer aqui:**
- **Políticas do YouTube (14/11/2026, `conhecimento/politicas-youtube.md`):** bonequinhos sugerem a morte sem corpo em destaque, sangue ou ferimento; nenhuma foto real de morto. Título, descrição e tags sem morte/morreu/morto/assassinado/assassinato (e equivalentes no idioma do canal) nem "chocante/perturbador/massacre"; `youtube.txt` sem menção a IA.
- **Capítulos-objeto** do Archive in Minutes ("O Cilindro.", "O Moinho.", fichas soltas, título de 1–2 palavras falado). Foi o erro do 003 v1 (04/11/2026): "não tem cara de história, falta conexão entre as partes" (Rodrigo).
- Hook seco de anedota em 10 s + "Esta é a história INTEIRA de X" + capítulos curtos: é o molde do `dossie-es`.
- Graphic novel em tinta, rostos realistas, pasta parda/sello rojo/máquina de escrever: identidade do `dossie-es`. Pintura a óleo romântica: identidade do `lotr-fr`.
- Organizações e serviços secretos (Gestapo, KGB, Mossad…) como tema: são do `dossie-es`.

## Versões da bíblia de roteiro (comparativo de desempenho)
- **v1** ([`roteiro-v1.md`](roteiro-v1.md), congelada em 07/11/2026): **001 Egito, 002 Índia, 003 Irã, 004 China, 005 Brasil**.
- **v2** ([`roteiro-v2.md`](roteiro-v2.md), aprovada pelo Rodrigo em 07/11/2026): **006 em diante**. As 12 regras vêm de `pesquisa/roteiro-historia-2026-11/RELATORIO.md`; checklist medido por `../tools/checklist_roteiro_v2.py`.
- **Rastreio:** coluna `youtube.videos.biblia_versao` (001–005 = `'v1'`; a skill `roteiro` grava `'v2'` ao escrever o 006+). Título-pergunta em teste nos v2: `titulo-v2.md`.

### Como comparar
Métricas que contam (todas de `youtube.metricas_video`, coletadas pela rotina diária): **views no dia 7**, **% assistido** (`pct_assistido`) e **duração média assistida** (`media_assistida_s`); retenção aos 30/60 s vem da curva (`tools/report.py historia-ptbr --retencao <youtube_id>`), CTR só pelo Studio (pedir ao Rodrigo). Compare só vídeos com ≥ 7 dias no ar e **pelo menos 3 por versão**; o tema pesa mais que o roteiro (RELATORIO.md §3), então olhe também a mediana e anote o tema. O % assistido é o número mais ligado ao roteiro; views ligam mais a título/thumb.
Query pronta (também em [`../tools/comparar_biblia_v1_v2.sql`](../tools/comparar_biblia_v1_v2.sql): `psql -d vida -f canais/historia-ptbr/tools/comparar_biblia_v1_v2.sql`):
```sql
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
```
O arquivo `.sql` tem ainda a visão vídeo a vídeo (views e % assistido no último snapshot e no dia 7). Ponto de partida em 07/11/2026 (4 dias no ar): Egito 91 views / 41,1% assistido; Índia 59 / 25,8%.
