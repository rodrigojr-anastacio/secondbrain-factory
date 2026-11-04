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
0. **Estude a referência pela transcrição completa** (não só o hook): `tools/.venv/bin/python tools/transcrever.py <ID> $V/ref/<nome>.txt en`, em 2–3 vídeos de History in Minutes / Archive in Minutes do tema ou da fórmula. Anote: tempo até a promessa do título, títulos de capítulo, onde a anedota é paga, loops e fecho. (Estudo de 04/11/2026 em `conhecimento/hooks.md` e `roteiros.md`.)
1. **Estrutura** (`conhecimento/roteiros.md`, padrão desde o 003):
   - **hook ≤ 35 s**: anedota humana concreta com desfecho em ≤ 10 s → promessa do título + pergunta → 1 loop;
   - **13–16 capítulos-objeto** com título de 1–2 palavras **falado** na narração ("O Moinho."), ~1 por minuto, `cap("N. O Moinho")`;
   - cada capítulo fecha puxando o próximo (de preferência com a frase que é o título do próximo); re-hook a cada ≤ 90 s; CTA de inscrição no meio, colado num re-hook;
   - anedota do hook paga entre 1/4 e 1/2 do vídeo; **fecho volta à imagem do começo** + aforismo de 2 frases + pergunta para os comentários.
   Defina o **fio condutor** e os **loops "guarde isso"** e onde cada um é pago.
2. **Hook** (`conhecimento/hooks.md`): data + lugar + pessoa + ação + desfecho seco. O "paradoxo → prova em rajada → virada" vira recurso de mini-hook nos capítulos. Modele a técnica da referência; **nunca traduza nem copie** o texto.
3. **Escreva no `roteiro.py`** (nunca nos arquivos gerados): um bloco `N...` = um arquivo de áudio (2–4 frases); marque `IDEIA` nos blocos que abrem ideia nova (vira `"ideia": true`, usado nas pausas do `build.py`).
   **Escreva para a fala** (A/B de 04/11/2026, `canais/historia-ptbr/videos/003-ira/amostras-voz/LEIA.md`): presente do indicativo; frases de 4–14 palavras; vírgula onde se respira; "…" só na virada; números por extenso; **sem `[break]`** (o `tts_fish.py --por-frase` já põe 0,32 s entre frases); `[long-break]` só antes de revelação; tag de tom simples (`[curious]`, `[amazed]`, `[serious]`, `[warm]`) só onde a emoção muda, ~1 a cada 2–3 blocos; nada de tags de direção ("[serious, calm]", "[low voice]"), que deixaram as frases mais iguais no teste.
   **Texto na tela:** nos planos, `"chave|prompt@@NOME"` vira rótulo (nome, lugar, data curta, até ~28 caracteres) em ~1 de cada 2 planos; `card="559 a.C."` para datas; mapas sem texto + rótulos em `src/labels.jsx`. Não ponha rótulo no 1º plano de capítulo (a placa do capítulo ocupa a base).
4. **Fatos:** cada número/data com fonte em `SOURCES.md`; estimativa dita como estimativa; fato não confirmado como `[PENDENTE]` com versão alternativa (não trave).
5. **Gere e valide:** `cd $V && python3 roteiro.py` (gera `SCRIPT.md`, `blocos.json` e, se o storyboard já estiver no arquivo, `cenas.json`/`STORYBOARD.md`/`storyboard.json`).
6. Conte as palavras: `python3 -c "import json,re;b=json.load(open('blocos.json'));print(sum(len(re.sub(r'\[[^]]*\]','',x['texto']).split()) for x in b))"`.
7. Atualize o status: `psql -d vida -c "UPDATE youtube.videos SET status='roteiro', atualizado_em=now() WHERE id=<id>"`.

## Critérios de pronto (avaliar)
- Hook ≤ 35 s, com anedota de desfecho em ≤ 10 s e loop aberto; 13–16 capítulos-objeto falados; fecho circular.
- Tamanho: com a voz por frase, ~144 ppm; historia-ptbr em ~15 min ≈ **2.050–2.150 palavras** (até o 002, sem a voz por frase: ~2.250–2.300 para 17 min; 2.620 deram 19:27 na Índia).
- `python3 roteiro.py` mostra `cortes_1o_min` ≥ 18 e `rotulos` ≈ metade dos planos.
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
