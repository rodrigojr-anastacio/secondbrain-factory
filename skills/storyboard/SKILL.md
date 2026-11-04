---
name: storyboard
description: Use depois do roteiro de um vídeo da fábrica do YouTube para planejar os planos visuais - gera STORYBOARD.md, storyboard.json e cenas.json (prompts só de conteúdo) no roteiro.py, com ritmo de 2-4 s por plano, reuso planejado e fidelidade a lugares e personagens, dentro do teto de imagens.
---

# storyboard: STORYBOARD.md, storyboard.json, cenas.json

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`.
Procedimento-base: `playbooks/produzir-video.md` §4. Modelo recomendado: **opus** (etapa `storyboard` ou `roteiro-storyboard`).

## Antes de agir
0. **Primeiro a bíblia do canal** (caixinha): `canais/<slug>/biblia/README.md` (canal-modelo e "o que NÃO fazer aqui") e `biblia/visual.md` (imagens, ritmo, reuso, texto na tela) e `biblia/roteiro.md` (capítulos). A bíblia **prevalece** sobre `conhecimento/` (só regras gerais). Nunca aplique padrão de outro canal.
1. Leia `$V/BRIEF.md` (teto de custo → nº máximo de imagens), `$V/SCRIPT.md` e `$V/blocos.json`.
2. Leia o bloco `visual` de `canais/<slug>/canal.yaml` (o `estilo_prompt` é aplicado pela tool: **não** repita estilo nos prompts).
3. Leia `conhecimento/anti-padroes.md` (reuso, fidelidade, lugar real × fictício, código desenhando cidade, frames de filme): regras gerais.
4. Modelo: o storyboard do `roteiro.py` do **vídeo anterior do mesmo canal** (nunca de outro canal).

## Passos
1. No `roteiro.py`, para cada bloco, defina os planos: imagem nova (`cenas.json`: `id` + prompt de conteúdo), reuso de uma imagem anterior (com enquadramento/movimento diferente) ou card de texto/mapa composto no código.
2. **Ritmo e reuso: os números da `biblia/visual.md` do canal** (ex.: historia-ptbr ~20/min no início e ~17 depois, reuso ~40% depois de 3:00; dossie-es 18–20/min e ~35%). Regra geral: nunca o mesmo enquadramento em < 60 s e 0% de reuso nos primeiros 3:00.
3. **Fidelidade:** cena que nomeia lugar ou personagem mostra **aquele** lugar/personagem; nada de lugar real no lugar de fictício; nada de frames de filme/série; nada de texto pedido à IA (texto só no código).
4. Gere: `cd $V && python3 roteiro.py` (valida as regras de reuso) → `STORYBOARD.md`, `storyboard.json`, `cenas.json`.
5. Calcule o custo previsto: nº de imagens novas × preço do motor do canal (`canal.yaml` → `visual`; preços reais em `conhecimento/anti-padroes.md`) + thumb; compare com o teto do BRIEF.

## Critérios de pronto (avaliar)
- Ritmo e reuso dentro do que a `biblia/visual.md` define; nenhum plano > 4 s sem movimento.
- Reuso 0% antes de 3:00; nenhum enquadramento repetido em < 60 s (a validação do `roteiro.py` passa).
- Toda cena com nome próprio tem prompt específico e fiel; prompts sem estilo e sem texto.
- Nada da lista "O que NÃO fazer aqui" da bíblia (ex.: rostos realistas no historia-ptbr; bonequinhos no dossie-es).
- Nº de imagens × preço ≤ teto do BRIEF.
- Anote em `$V/ETAPA1.md`: nº de planos, imagens novas, % de reuso, custo previsto.

## Loop de melhoria
1. **Avaliar:** rode a validação, conte planos/min, % de reuso e custo previsto contra os critérios.
2. **Corrigir:** até 2 rodadas (aumentar reuso depois de 3:00, partir planos longos, reescrever prompt infiel). Resto = pendência no `ETAPA1.md`.
3. **Registrar:** aprendizado vai para **`canais/<slug>/biblia/visual.md`** (do canal deste vídeo) com **data e fonte**; só sobe para `conhecimento/` o que for **comprovadamente geral** (ferramenta, custo, processo); sem dado = **Hipótese**.
4. **Commitar:** `git add $V/roteiro.py $V/STORYBOARD.md $V/storyboard.json $V/cenas.json $V/ETAPA1.md` e
   `git commit -m "<canal>/<NNN>: storyboard (P planos, I imagens, reuso R%)"`.
