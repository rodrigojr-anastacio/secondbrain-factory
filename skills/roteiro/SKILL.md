---
name: roteiro
description: Use para escrever ou revisar o roteiro de um vídeo da fábrica do YouTube a partir do BRIEF.md - edita o roteiro.py (fonte única) e gera SCRIPT.md, blocos.json e SOURCES.md, com hook de até ~45 s, loops pagos, fatos com fonte e tamanho certo para a duração-alvo.
---

# roteiro: roteiro.py → SCRIPT.md, blocos.json, SOURCES.md

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `canais/<slug>/videos/NNN-slug/` (abaixo, `$V`).
Procedimento-base: `playbooks/produzir-video.md` §2. Modelo recomendado: **opus** (etapa `roteiro` ou `roteiro-storyboard` do `tools/claude_run.py`).

## Antes de agir
1. Leia `$V/BRIEF.md` (referência, duração-alvo, loops, teto) e, se houver, `$V/ref/transcricao.txt`.
2. Leia `canais/<slug>/canal.yaml` e `canais/<slug>/estilo.md`.
3. Leia `conhecimento/hooks.md`, `conhecimento/roteiros.md`, `conhecimento/titulos.md` e `conhecimento/anti-padroes.md`.
4. Use como modelo o `roteiro.py` do vídeo anterior do canal (ex.: `canais/historia-ptbr/videos/002-india/roteiro.py`).

## Passos
1. **Estrutura** (`conhecimento/roteiros.md`): hook → capítulos com mini-hook na abertura e gancho no fim → fecho com payoff e pergunta para os comentários. Defina o **fio condutor** e os **loops "guarde isso"** e onde cada um é pago.
2. **Hook** (`conhecimento/hooks.md`): paradoxo/fato que choca → prova em rajada → virada → pergunta central → entrada imediata no corpo. Feche em ~40–45 s. Modele a técnica da referência; **nunca traduza nem copie** o texto.
3. **Escreva no `roteiro.py`** (nunca nos arquivos gerados): um bloco `P..` = um arquivo de áudio; marque `IDEIA` nos blocos que abrem ideia nova (vira `"ideia": true`, usado nas pausas do `build.py`).
   Direção de voz Fish no texto conforme §3 do playbook (`[break]`, `[long-break]`, `[emphasis]`, tags de tom; no máximo 3 por frase; nunca terminar bloco com frase curta depois de `[break]`).
4. **Fatos:** cada número/data com fonte em `SOURCES.md`; estimativa dita como estimativa; fato não confirmado como `[PENDENTE]` com versão alternativa (não trave).
5. **Gere e valide:** `cd $V && python3 roteiro.py` (gera `SCRIPT.md`, `blocos.json` e, se o storyboard já estiver no arquivo, `cenas.json`/`STORYBOARD.md`/`storyboard.json`).
6. Conte as palavras: `python3 -c "import json,re;b=json.load(open('blocos.json'));print(sum(len(re.sub(r'\[[^]]*\]','',x['texto']).split()) for x in b))"`.
7. Atualize o status: `psql -d vida -c "UPDATE youtube.videos SET status='roteiro', atualizado_em=now() WHERE id=<id>"`.

## Critérios de pronto (avaliar)
- Hook ≤ ~45 s (≈ 100–110 palavras faladas) e com loop aberto.
- Tamanho: ~150 palavras/min de meta; historia-ptbr em ~17 min = **2.250–2.300 palavras** (2.620 deram 19:27 na Índia).
- Todo loop aberto é pago; cada capítulo tem mini-hook.
- Todo fato tem fonte em `SOURCES.md`; `[PENDENTE]` sempre com alternativa.
- `python3 roteiro.py` roda sem erro e `blocos.json` tem `ideia` nos blocos certos.
- Escreva o resumo da etapa em `$V/ETAPA1.md` (palavras, duração estimada, loops, pendências).

## Loop de melhoria
1. **Avaliar:** meça palavras, duração estimada do hook e loops pagos/abertos; compare com `conhecimento/roteiros.md`.
2. **Corrigir:** até 2 rodadas (cortar, reescrever hook, pagar loop). O resto vira pendência no `ETAPA1.md`.
3. **Registrar:** estrutura, loop ou técnica nova vai para `conhecimento/roteiros.md` ou `hooks.md` (e o que for do canal, no `estilo.md`) com **data e fonte**; sem retenção medida = **Hipótese**.
4. **Commitar:** `git add $V/roteiro.py $V/SCRIPT.md $V/SOURCES.md $V/blocos.json $V/ETAPA1.md` (+ conhecimento) e
   `git commit -m "<canal>/<NNN>: roteiro v1 (N palavras, hook X s)"`.
