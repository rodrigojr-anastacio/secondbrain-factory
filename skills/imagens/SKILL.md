---
name: imagens
description: Use para gerar as imagens das cenas de um vídeo da fábrica do YouTube a partir do cenas.json com tools/img_codex.py (Codex, fallback Gemini), tools/img_gemini.py, tools/img_fal.py ou tools/img_openai.py, conforme o canal.yaml, em um único processo por pasta, com saldo conferido antes, custo atribuído ao vídeo e zero imagens faltando ou duplicadas.
---

# imagens: cenas.json → imagens/*.jpg

Raiz do repo: `~/workspace/fabrica-youtube`. Pasta do vídeo: `$V = canais/<slug>/videos/NNN-slug/`. Python: `tools/.venv/bin/python`.
Procedimento-base: `playbooks/produzir-video.md` §3 (parágrafo "Imagens") e §4. Modelo recomendado: **sonnet** (etapa `imagens` ou `producao`).

## Antes de agir
0. **Primeiro a bíblia do canal** (caixinha): `canais/<slug>/biblia/README.md` (canal-modelo e "o que NÃO fazer aqui") e `biblia/visual.md` (motor aprovado, identidade das imagens, armadilhas do canal). A bíblia **prevalece** sobre `conhecimento/` (só regras gerais). Nunca aplique padrão de outro canal.
1. Leia o bloco `visual` de `canais/<slug>/canal.yaml` (`gerador`, `modelo`, `qualidade`, `tamanho`, `estilo_prompt`). **Não troque de motor** sem amostra aprovada no estilo da bíblia: trocar o motor muda a identidade do canal (`conhecimento/anti-padroes.md` §3b).
2. Leia `conhecimento/anti-padroes.md` (nada de `low`; nada de 2 processos na mesma pasta; saldo; fidelidade) e `conhecimento/thumbnails/README.md` se for gerar a base da thumb.
3. Leia `$V/BRIEF.md` (teto) e `$V/cenas.json` (nº de imagens).
4. Saldo (com `gerador: codex`, só para a reserva do fallback: "Google Gemini API" desde 23/11/2026, ~US$ 0,05/img): `psql -d vida -c "SELECT * FROM financas.saldo_pre_pago"`. Custo previsto = nº de imagens que faltam × US$ 0,055 (`medium`). Se o saldo não cobrir (o da OpenAI pode estar negativo por recarga não lançada), **pergunte ao Rodrigo** antes de gastar: dinheiro é decisão dele.

## Passos
1. **Um processo só**, em primeiro plano (timeout alto; em `claude -p`, processo em segundo plano morre no fim do turno), da raiz do repo:
   ```bash
   mkdir -p $V/logs
   tools/.venv/bin/python tools/img_openai.py <slug> $V/cenas.json $V/imagens --video <id> --qualidade medium --paralelo 8 \
     2>&1 | tee $V/logs/img.log
   ```
   Lote grande: divida o `cenas.json` em partes de ~60 imagens (~8 min cada, cabe no timeout de 10 min de um comando); a tool pula ids que já existem.
   Alternativa (canal com `gerador: fal`): `tools/.venv/bin/python tools/img_fal.py <slug> $V/cenas.json $V/imagens --video <id> --paralelo 8`.
   **Canal com `gerador: codex` (`historia-ptbr` desde 14/11/2026; `dossie-es` desde 23/11/2026, teste no MKUltra):** Codex CLI do ChatGPT Plus, US$ 0, com fallback automático pelo `visual.gerador_fallback` (`gemini` nos dois canais desde 23/11/2026, porque a fal ficou sem saldo; `fal` ainda funciona):
   ```bash
   tools/.venv/bin/python tools/img_codex.py <slug> $V/cenas.json $V/imagens --video <id> --paralelo 3 --teto <teto do BRIEF> \
     2>&1 | tee -a $V/logs/img.log
   ```
   ~45–65 s por imagem, ~18–20 s efetivos com 3 em paralelo: **lotes de ~25 cenas por comando** (`--so`; rode de novo até 0 faltando, ele pula o que existe). Não passe de `--paralelo 3`. Falha/recusa/imagem preta ou com moldura → só aquela imagem vai para o fallback (`img_gemini.py` ou `img_fal.py`), **só se saldo − custo ≥ folga** (`FOLGA_GEMINI`/`FOLGA_FAL`; sem saldo fica faltando, sai 1; o custo é registrado pela tool do fallback, notas "fallback codex"; o `--teto` vale para ele). **Limite de cota do Codex (24/11/2026): espera o reset, não paga.** O lote para, o reset vem do próprio 429 e a tool sai com **código 4** (`CODEX_AGUARDAR até HH:MM`) sem chamar o fallback. Em job da fila: grave `ETAPA2-PENDENTE.md` (cenas faltando + reset), commit + push e **encerre o turno**, sem placeholder e sem loop de `sleep`. A fila põe o job em `pausado_codex` e o retoma no reset. O mesmo código 4 sai quando o **portão da noite** está fechado (o vídeo é o 2º da noite e o Dossier ainda não terminou as imagens). Ao completar todas as cenas do `cenas.json` do vídeo, a tool avisa a noite ("pode seguir"). `--ignorar-portao` e `--fallback-no-limite` só para teste/manual. Regra completa em `tools/rotinas/README.md` (Fábrica noturna) e `tools/codex_janela.py`. Log por imagem em `$V/imagens/codex_log.jsonl`; acompanhamento em `tools/codex_uso.sh`. No relatório da etapa, informe **imagens Codex × fallback** e a cota 5 h/semanal que o fim do comando imprime. Armadilhas do Codex: `conhecimento/anti-padroes.md` §3c. Outros canais não usam o Codex.
   **Limite de imagem ≠ % do plano (Hipótese, 24/11/2026; confirmar com 3 noites medidas em `tools/codex_uso.sh`):** o 429 é `usage_limit_reached` do `imagegen_premium`, janela de **24 h** contada da 1ª imagem (`limit_window_minutes: 1440`), e chegou com 270, 250 e 196 imagens (16, 22 e 23/11), quando o painel mostrava só 9–36% do 5 h. 1 vídeo ≈ 190–205 imagens, ou seja, cabe ~1 vídeo por janela. Por isso a fábrica noturna gera as imagens **um vídeo de cada vez** (Dossier → História).
   **Concorrência entre vídeos (23/11/2026):** dois jobs na mesma noite (historia + dossie) dividem **3 vagas globais** de `codex exec` (flock em `~/cache/img_codex/vaga-N.lock`, `IMG_CODEX_SLOTS`): nunca passam de 3 chamadas juntas no Plus (rajada maior acusou limite em 22/11 com 9% da janela), cada lote anda na metade da velocidade e a vaga cai sozinha se o processo morrer. Como esperar vaga alonga o comando, o `img_codex.py` tem **`--prazo-min 6`** (padrão): depois de 6 min não começa imagem nova, termina as que estão rodando e sai com código 1 e a lista do que falta (sem mandar ao fallback). Isso é normal: **rode o mesmo comando de novo** até 0 faltando. Se a cota de imagem acabar (429), a tool espera o reset (código 4; acima).
   **`tools/img_gemini.py` (23/11/2026)**, também direto (ex.: refazer imagens que o Codex errou, se o Codex estiver sem cota): mesmo contrato do `img_fal.py`: `tools/.venv/bin/python tools/img_gemini.py <slug> $V/cenas.json $V/imagens --video <id> --paralelo 4 --teto <US$> [--so …]`. Modelo `visual.modelo_gemini` (padrão `gemini-nano-banana-2.1`, modo padrão 1K, nunca Batch), `estilo_prompt` + `refs`/`ref_instrucao` do canal, 16:9 salvo em 1536×864, trava a pasta e pula prontas. Custo real pelo `usageMetadata` (~US$ 0,05/img) em `financas.consumo` (fornecedor "Google Gemini API", `ref_id` do vídeo). Bloqueio (IMAGE_SAFETY) → 1 nova tentativa sem "resembling <Nome>", depois fica faltando (refaça pelo Codex ou cubra com reuso). **No storyboard, evite "resembling <nome real>" em cenas que podem cair no Gemini**: descreva a pessoa (idade, cabelo, roupa) e use o nome só no contexto.
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
