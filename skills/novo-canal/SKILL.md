---
name: novo-canal
description: Use quando o Rodrigo quiser avaliar ou abrir um canal novo na fábrica do YouTube (a partir de um canal de referência achado no garimpo ou de uma ideia de nicho) - mapa de concorrência por idioma, anatomia do formato com vídeos assistidos, oportunidade e riscos com decisão INVESTIR/TESTAR/DESCARTAR e, se não descartar, o blueprint do canal (canal.yaml, estilo, backlog de 20 temas, identidade, roteiro do piloto, conceitos de thumb) com teste de estilo de até US$ 3.
---

# novo-canal: do achado ao canal pronto para o piloto

Raiz do repo: `~/workspace/fabrica-youtube`. Python: `tools/.venv/bin/python`.
Procedimento completo: **`playbooks/novo-canal.md`** (etapas 1–6). Exemplo real: `pesquisa/archive-in-minutes/LEVANTAMENTO.md` → `canais/dossie-ptbr/`.

## Antes de agir
1. Leia `MAPA.md`, `AGENTS.md`, `playbooks/garimpo-tendencias.md` (tabela de RPM e regras de cota) e `conhecimento/` inteiro.
2. Confira se o nicho já foi avaliado: `psql -d vida -c "SELECT titulo, formula, decisao, notas FROM youtube.garimpo_canais WHERE decisao IS NOT NULL"` e `ls pesquisa/`.
3. Em `claude -p`: **nada em segundo plano** (subagentes e comandos em primeiro plano). Grave os dados brutos cedo para poder retomar.

## Passos (resumo do playbook)
1. **Concorrência** (subagente `tendencias`): lista completa de vídeos da referência + até ~15 buscas por tema × idioma → `pesquisa/<slug>/dados.json`; tabelas de fórmula exata, **clones** e mesmo nicho.
2. **Anatomia:** `tools/watch.py` em ≥ 6 vídeos de ≥ 3 canais (hits e flops); visão em thumb/hook_sheet/video_sheet; mosaico de thumbs em `pesquisa/<slug>/thumbs/`.
3. **Oportunidade:** idioma, saturação (nº de clones e mediana deles), RPM, projeção em faixa, diferenciação, riscos de política, decisão com **critério numérico**; `youtube.garimpo_canais`; `pesquisa/<slug>/LEVANTAMENTO.md` com resumo executivo no topo.
4. **Blueprint:** linhas em `youtube.canais` (status `em preparação`) e `youtube.videos` (piloto); `canais/<slug>/` com `canal.yaml`, `estilo.md`, `backlog.md` (20 temas), `identidade.md` (3 nomes com handle conferido), `videos/001-<tema>/` (BRIEF, SCRIPT, SOURCES, THUMBS).
5. **Teste de estilo** (≤ US$ 3, `--video <id>`): 5 cenas × 3–4 modelos, grade, visão, resolução → `canais/<slug>/testes/ESTILO.md` e modelo no `canal.yaml`.
6. **Entrega:** resposta curta com as decisões pendentes do Rodrigo; `git add` só dos seus caminhos; commit e push.

## Critérios de pronto (avaliar)
- ≥ 30 canais mapeados com link e views/mês; clones contados; pelo menos en + pt-BR + es cobertos.
- ≥ 6 vídeos assistidos de ≥ 3 canais, com hook literal citado; observado × inferido marcado em todo o relatório.
- Decisão INVESTIR/TESTAR/DESCARTAR com idioma, 20 temas com evidência (ou Hipótese) e critério numérico de revisão.
- Blueprint completo, com handles conferidos, piloto com roteiro completo e fontes, e 3 conceitos de thumb.
- Gasto ≤ US$ 3, todo em `financas.consumo` com `ref_id` do piloto. Nenhuma voz, render, canal criado ou mensagem enviada.

## Loop de melhoria
1. **Avaliar:** confira cada critério acima; marque o que faltou.
2. **Corrigir:** no máximo 2 rodadas (ex.: assistir mais um flop, refazer o teste de estilo com prompt de mapa corrigido).
3. **Registrar:** padrão novo de título, hook, thumb ou roteiro vai para `conhecimento/` com data e fonte (ou fica na seção "Sugestões" do LEVANTAMENTO se outro job estiver nesses arquivos). Melhoria de procedimento vai para `playbooks/novo-canal.md`.
4. **Commitar:** `git commit -m "novo-canal <slug>: levantamento (<decisão>) + blueprint"`.
