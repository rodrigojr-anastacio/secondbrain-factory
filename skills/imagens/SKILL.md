---
name: imagens
description: Use para gerar as imagens das cenas de um vídeo da fábrica do YouTube a partir do cenas.json com tools/img_openai.py (medium) ou tools/img_fal.py, em um único processo por pasta, com saldo conferido antes, custo atribuído ao vídeo e zero imagens faltando ou duplicadas.
---

# imagens: cenas.json → imagens/*.jpg

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`. Python: `tools/.venv/bin/python`.
Procedimento-base: `playbooks/produzir-video.md` §3 (parágrafo "Imagens") e §4. Modelo recomendado: **sonnet** (etapa `imagens` ou `producao`).

## Antes de agir
0. **Primeiro a bíblia do canal** (caixinha): `canais/<slug>/biblia/README.md` (canal-modelo e "o que NÃO fazer aqui") e `biblia/visual.md` (motor aprovado, identidade das imagens, armadilhas do canal). A bíblia **prevalece** sobre `conhecimento/` (só regras gerais). Nunca aplique padrão de outro canal.
1. Leia o bloco `visual` de `canais/<slug>/canal.yaml` (`gerador`, `modelo`, `qualidade`, `tamanho`, `estilo_prompt`). **Não troque de motor** sem amostra aprovada no estilo da bíblia: trocar o motor muda a identidade do canal (`conhecimento/anti-padroes.md` §3b).
2. Leia `conhecimento/anti-padroes.md` (nada de `low`; nada de 2 processos na mesma pasta; saldo; fidelidade) e `conhecimento/thumbnails/README.md` se for gerar a base da thumb.
3. Leia `$V/BRIEF.md` (teto) e `$V/cenas.json` (nº de imagens).
4. Saldo: `psql -d vida -c "SELECT * FROM financas.saldo_pre_pago"`. Custo previsto = nº de imagens que faltam × US$ 0,055 (`medium`). Se o saldo não cobrir (o da OpenAI pode estar negativo por recarga não lançada), **pergunte ao Rodrigo** antes de gastar: dinheiro é decisão dele.

## Passos
1. **Um processo só**, em primeiro plano (timeout alto; em `claude -p`, processo em segundo plano morre no fim do turno), da raiz do repo:
   ```bash
   mkdir -p $V/logs
   tools/.venv/bin/python tools/img_openai.py <slug> $V/cenas.json $V/imagens --video <id> --qualidade medium --paralelo 8 \
     2>&1 | tee $V/logs/img.log
   ```
   Lote grande: divida o `cenas.json` em partes de ~60 imagens (~8 min cada, cabe no timeout de 10 min de um comando); a tool pula ids que já existem.
   Alternativa (canal com `gerador: fal`): `tools/.venv/bin/python tools/img_fal.py <slug> $V/cenas.json $V/imagens --video <id> --paralelo 8`.
2. As tools travam a pasta (`$V/imagens/.img.lock`; 2º processo sai com código 3) e pulam ids já existentes. **Não** lance outro processo "para acelerar".
3. Conte no fim: `ls $V/imagens | wc -l` (o custo sai no fim do processo; 204 imagens ≈ 25 min).
4. Se aparecer `insufficient_quota`/"no credits": pare o processo, escreva `$V/BLOQUEIO.md` e cubra as faltas com reuso no storyboard. Se o processo morrer antes do fim, lance o custo do lote à mão em `financas.consumo`.

## Critérios de pronto (avaliar)
- 0 imagens faltando: todo `id` de `cenas.json` tem arquivo em `$V/imagens/` (compare as listas com um one-liner Python).
- 0 gerações duplicadas (nº de chamadas pagas no log = nº de imagens novas).
- Custo em `financas.consumo` (`ref_id=<id>`) ≤ teto do BRIEF.
- Amostra visual (contact sheet de ~12 imagens com `ffmpeg ... -vf tile`, não imagem por imagem): **a identidade da `biblia/visual.md`** (ex.: bonequinhos de cabeça redonda no historia-ptbr; graphic novel com rostos adultos no dossie-es; pintura a óleo no lotr-fr), nenhum texto/letra gerado pela IA, lugares nomeados fiéis.
- **Políticas (`conhecimento/politicas-youtube.md`):** nenhuma imagem com corpo em destaque, sangue, ferimento ou sofrimento explícito (a morte é só sugerida); prompts sem esses termos. Se a IA devolver algo apelativo, refaça.
- Relatório em `$V/ETAPA2.md` (imagens, custo, falhas, reusos de cobertura).

## Loop de melhoria
1. **Avaliar:** faltantes, duplicadas, custo × teto e a amostra visual.
2. **Corrigir:** até 2 rodadas: reescreva no `roteiro.py` o prompt das cenas reprovadas, apague só esses arquivos e rode o mesmo comando de novo (pula o que existe). Resto = pendência.
3. **Registrar:** prompt e estilo do canal em **`canais/<slug>/biblia/visual.md`**; preço real, incidente de saldo e armadilha de ferramenta (vale para todos) em `conhecimento/anti-padroes.md`. Sempre com **data e fonte**; sem dado = **Hipótese**.
4. **Commitar:** `git add $V/ETAPA2.md $V/cenas.json $V/roteiro.py` (+ conhecimento; imagens ficam fora do git) e
   `git commit -m "<canal>/<NNN>: imagens (I geradas, US$ X, 0 faltando)"`.
