# Padrão ouro de título + thumb: relatório (17/11/2026)

## Resumo (15 linhas)
1. Corpus: 28 canais, 739 vídeos longos (top 20–25 por views em 2 anos + 10 recentes; 10 anos para OverSimplified/LEMMiNO/Barely Sociable), com ×mediana real, mosaicos normal e 160×90 por canal. Custo US$ 0 (yt-dlp via WARP + `videos.list`/`channels.list`/`playlistItems`; < 400 unidades de cota de 10 mil/dia, 0 `search.list`).
2. Método com link (MrBeast, Paddy Galloway, Ed Lawrence, vidIQ 4 mi de vídeos, Eden 507 mil, Thomas Frank, YouTube Help): `FONTES-METODO.md`.
3. Achado central: **normalizada por canal, nenhuma estrutura de título ganha sozinha** (índice 0,94–1,07). O que faz o hit é **sujeito concreto + o que está em jogo**, com tema-ímã ("Beat Ronaldo" 2,80× × "Beat Professional Athlete" 0,67×, mesmo formato).
4. Título: 30–50 caracteres (hits 39 × flops 46 nos gerais; 38,5 × 53 no dossiê), sem parênteses (O Mundo 0,26× × 1,25×) e sem aposto; lacuna com conflito/perda, não pergunta de aula nem sim/não.
5. Thumb: 1 foco, desfecho pendente (62 de 80 nos gerais), emoção sem precisar de rosto, texto de 0–3 palavras que **completa** o título (79% nos gerais; os nossos moldes HiM/AiM repetem 100%), legível e diferente na grade a 160×90.
6. Para canais sem rosto, o que se transfere: personagem com emoção em duelo (OverSimplified, Magnates), objeto/alvo vermelho (Fern, LEMMiNO), uma região em alerta sobre relevo claro (RealLifeLore 10/10), veredito curto (Kurzgesagt).
7. `PADRAO-OURO.md` = 5 regras de título + 5 de thumb + o par, com exemplo e números; `RUBRICA.md` = 10 critérios 0–10 (aprova com ≥ 75, nenhum < 6, T2/H1/P1 ≥ 7) + teste da grade com 11 concorrentes.
8. Auditoria (21 vídeos no ar): média **57,9/100**; só **1 de 21** passa (historia-ptbr Roma, 84). historia-ptbr 65,0 · Em Relevo 54,8 · dossie-es 51,4.
9. Defeito recorrente: **título e thumb não formam uma pergunta só** (P1): a SIGLA do dossie-es repete o título em 8 de 8; a pegada HiM repete o nome do país; e o título é rótulo/fórmula sem lacuna (T2).
10. CTR real: historia-ptbr 2,0–9,6% (Egito 5,9% em 5.858 impr.) já está na faixa normal do YouTube (2–10%); dossie-es 2,7–3,9%; Em Relevo 1,5–2,7% é o mais abaixo. Impressões baixas: tudo por vídeo é Hipótese.
11. Antes × depois: 6 propostas (2 por canal) com nota prevista 76–84, mais a troca mínima urgente do Em Relevo 003 (`ANTES-DEPOIS.md`).
12. Urgente: Em Relevo 003 está no ar com "matou" no título e "500 MIL" na thumb (viola a política da fábrica); o `youtube.txt` da França (historia-ptbr 008) tem "matou" no título B (não está no ar).
13. Proposta de encaixe (não aplicada): rubrica no `CRIVO.md`, passo "teste da ideia" + regras de título/thumb no `SKILL.md`, grade obrigatória na `thumbnail`, seções novas em `conhecimento/`, e ajustes por bíblia (`PROPOSTA-ENCAIXE.md`).
14. Mudanças de identidade que pedem decisão: thumb do dossie-es sem a SIGLA gigante (sigla na aba); pegada HiM no máximo 1 de 3; Em Relevo testa relevo claro + 1 alerta.
15. Nada em skills, bíblias, `conhecimento/`, fila, backlog ou vídeos foi alterado; só esta pasta.

## Arquivos
| Arquivo | O que é |
|---|---|
| `PADRAO-OURO.md` | o padrão, curto e operacional (5 + 5 regras, o par, gerais × nicho sem rosto, leitura do nosso CTR) |
| `RUBRICA.md` | checklist pontuável para o crivo, com âncoras 10/7/3/0 e exemplos reais |
| `AUDITORIA.md` | ficha de cada um dos 21 vídeos no ar + resumo por canal |
| `ANTES-DEPOIS.md` | 2 propostas por canal ativo (+ Alemanha em 1 linha e a troca urgente do Em Relevo 003) |
| `PROPOSTA-ENCAIXE.md` | o que mudaria em skills, `conhecimento/` e bíblias (não aplicado) |
| `FONTES-METODO.md` | regras de método com link e tipo de evidência (oficial, medido, especialista) |
| `ANALISE-geral.md`, `ANALISE-historia-dossie.md`, `ANALISE-geografia.md` | análise do corpus por grupo (estruturas, tamanho, thumbs, hit × flop) |
| `corpus.csv` (+ `corpus/<canal>.csv/.json`, `corpus/nossos.csv`) | 739 vídeos dos grandes + os nossos no ar com CTR |
| `mosaicos/<canal>.jpg` e `-160.jpg` | mosaicos por canal (todos < 2 MB) — **fora do git** (`*.jpg` ignorado); ficam no disco nesta pasta |
| `grades/<canal>-<NNN>-160/320.jpg` + `-refs.json` | teste da grade de cada vídeo nosso (jpg fora do git; json no git) |
| `thumbs/` | thumbs baixadas (164 MB, fora do git) |
| `scripts/corpus.py`, `nossos.py`, `grade.py` | coleta reproduzível (custo zero) |

## Canais do corpus
- **Gerais:** MrBeast, Ryan Trahan, Mark Rober, Veritasium, Kurzgesagt, Johnny Harris, MagnatesMedia, Yes Theory.
- **História:** OverSimplified, History Matters, Kings and Generals, History in Minutes, CountryCorns, Nerdologia (pt), Brasil Paralelo (pt; só thumb, título distorcido por lives), Atlas del Tiempo (es), Academia Play (es).
- **Dossiê:** Archive in Minutes, Fern, LEMMiNO, Barely Sociable. (Spies in Minutes descartado: 13 inscritos.)
- **Geografia/Terra:** RealLifeLore, Wendover, Geography Now (mediana distorcida por lives: só padrão visual), O Mundo e Tudo ao Redor (pt), VisualPolitik (es), Ciência Todo Dia (pt).

## Ressalvas
- O "top" é escolhido por views, então ×med > 1 é esperado: as análises comparam estruturas **dentro** do canal e hit × flop do mesmo canal.
- Vídeos de novembro dos canais pequenos têm poucos dias (×med baixo por idade); as análises usaram views/dia ou ≥ 15 dias onde importava.
- Não temos o CTR dos outros canais: ×med mistura CTR, tema e alcance.
- Archive in Minutes "Cuban Missile Crisis": a thumb baixada é a do GULAG (troca no canal ou erro de coleta); fora da análise título × thumb.
- Lacuna honesta: não há fonte de peso sobre mapa/objeto/número em thumb de canal educacional; fica **Hipótese** e se mede no placar `youtube.padrao_thumb_placar`.

## O que precisa de aprovação do Rodrigo
1. Rubrica de 100 pontos dentro do crivo da `embalagem` (e as regras novas de título/thumb).
2. Thumb nunca repete a sigla/nome do título (muda o layout-assinatura do dossie-es e a pegada HiM do historia-ptbr).
3. Em Relevo: teste do relevo claro + 1 região em alerta.
4. Cada antes × depois (7 linhas em `ANTES-DEPOIS.md`), um a um; o Em Relevo 003 é o mais urgente.
