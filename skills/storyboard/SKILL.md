---
name: storyboard
description: Use depois do roteiro de um vídeo da fábrica do YouTube para planejar os planos visuais - gera STORYBOARD.md, storyboard.json e cenas.json (prompts só de conteúdo) no roteiro.py, com ritmo de 2-4 s por plano, reuso planejado e fidelidade a lugares e personagens, dentro do teto de imagens.
---

# storyboard: STORYBOARD.md, storyboard.json, cenas.json

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`.
Procedimento-base: `playbooks/produzir-video.md` §4. Modelo recomendado: **opus** (etapa `storyboard` ou `roteiro-storyboard`).

## Antes de agir
1. Leia `$V/BRIEF.md` (teto de custo → nº máximo de imagens), `$V/SCRIPT.md` e `$V/blocos.json`.
2. Leia `canais/<slug>/estilo.md` e o bloco `visual` de `canais/<slug>/canal.yaml` (o `estilo_prompt` é aplicado pela tool: **não** repita estilo nos prompts).
3. Leia `conhecimento/anti-padroes.md` (reuso, fidelidade, lugar real × fictício, código desenhando cidade, frames de filme) e `conhecimento/roteiros.md` (ritmo).
4. Modelo: o storyboard dentro de `canais/historia-ptbr/videos/002-india/roteiro.py` e o `STORYBOARD.md` dele.

## Passos
1. No `roteiro.py`, para cada bloco, defina os planos: imagem nova (`cenas.json`: `id` + prompt de conteúdo), reuso de uma imagem anterior (com enquadramento/movimento diferente) ou card de texto/mapa composto no código.
2. **Ritmo:** um plano a cada 2–4 s (~17/min), com Ken Burns/parallax; no 1º minuto, ≥ 23 planos.
3. **Reuso:** 0% nos primeiros 3:00; ~40% depois; nunca o mesmo enquadramento em < 60 s.
4. **Fidelidade:** cena que nomeia lugar ou personagem mostra **aquele** lugar/personagem; nada de lugar real no lugar de fictício; nada de frames de filme/série; nada de texto pedido à IA (texto só no código).
5. Gere: `cd $V && python3 roteiro.py` (valida as regras de reuso) → `STORYBOARD.md`, `storyboard.json`, `cenas.json`.
6. Calcule o custo previsto: nº de imagens novas × US$ 0,055 (`medium`, `img_openai.py`) + thumb `high` ~US$ 0,22; compare com o teto do BRIEF.

## Critérios de pronto (avaliar)
- ~17 planos/min; nenhum plano > 4 s sem movimento.
- Reuso 0% antes de 3:00 e ≤ ~40% depois; nenhum enquadramento repetido em < 60 s (a validação do `roteiro.py` passa).
- Toda cena com nome próprio tem prompt específico e fiel; prompts sem estilo e sem texto.
- Nº de imagens × preço ≤ teto do BRIEF.
- Anote em `$V/ETAPA1.md`: nº de planos, imagens novas, % de reuso, custo previsto.

## Loop de melhoria
1. **Avaliar:** rode a validação, conte planos/min, % de reuso e custo previsto contra os critérios.
2. **Corrigir:** até 2 rodadas (aumentar reuso depois de 3:00, partir planos longos, reescrever prompt infiel). Resto = pendência no `ETAPA1.md`.
3. **Registrar:** regra nova de ritmo, reuso ou prompt que funcionou/falhou em `conhecimento/anti-padroes.md` ou `roteiros.md` (e `estilo.md` do canal) com **data e fonte**; sem dado = **Hipótese**.
4. **Commitar:** `git add $V/roteiro.py $V/STORYBOARD.md $V/storyboard.json $V/cenas.json $V/ETAPA1.md` e
   `git commit -m "<canal>/<NNN>: storyboard (P planos, I imagens, reuso R%)"`.
