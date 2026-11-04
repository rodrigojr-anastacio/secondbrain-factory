# BRIEF: piloto "A HISTÓRIA COMPLETA do Egito" (canal História em minutos)

Pedido do Rodrigo, repassado pelo manager (Claude). Você (Hermes) orquestra e confere; o Claude Code implementa.
Antes de começar, leia: `~/workspace/fabrica-youtube/AGENTS.md`, `playbooks/produzir-video.md`, `canais/historia-ptbr/canal.yaml` e `canais/historia-ptbr/estilo.md`.

- **Pasta:** `~/workspace/fabrica-youtube/canais/historia-ptbr/videos/001-egito/`
- **id no banco:** `youtube.videos.id = 3`. Use `--video 3` em todas as gerações pagas e atualize o `status` a cada etapa (roteiro → producao → qa → pronto).

## Objetivo
Modelar **100%** o vídeo de referência **"The ENTIRE History of Egypt in 17 Minutes"** (History in Minutes, 417 mil views) para o português do Brasil. O canal ainda não tem vídeos dessa série: este é o primeiro.

Material de referência já baixado em `ref/`:
- `ref/VQPzrVMHWlg/` (Egito): `hook.txt` com a transcrição dos primeiros 90 s, `hook_sheet.jpg`, `video_sheet.jpg` e `thumb.jpg`.
- `ref/XO1-4FH1X1I/` (Irã, 918 mil views, do mesmo dono): `info.json` com os capítulos, útil como modelo de estrutura.

**Modele a estrutura, o ritmo e o estilo. Escreva o roteiro com texto próprio; nunca traduza o original.**

## 1. Título e thumbnail
- **Título:** `A HISTÓRIA COMPLETA do Egito em N minutos`, com N igual à duração final, arredondada.
- **Thumbnail** (igual à fórmula da referência): ilustração panorâmica do Egito no estilo do canal à esquerda (pirâmides, Esfinge, Nilo, cidade), com o lado direito livre e, nele, **EGITO** em serifa preta grande e **5000 a.C. – 2026** embaixo, em fonte sem serifa e negrito. Gere a ilustração em qualidade **medium** e componha o texto no código, nunca pela IA. Use como base `canais/historia-ptbr/testes/estilo/gpt-image-2/T5-thumb-giza.jpg`, aprovada pelo Rodrigo, ou gere uma nova parecida.

## 2. Roteiro (`SCRIPT.md` + `SOURCES.md`)
- **Meta:** 15–17 minutos, com ~2.300–2.500 palavras em pt-BR natural, frases curtas e ritmo de narração.
- **Hook (0–40 s):** abra com uma **reformulação que choca** (algo como "o Egito não é um país com um rio; é um rio com um país em volta") e uma **comparação de escala de tempo** que impressiona (como "Cleópatra viveu mais perto de nós do que dos construtores da Grande Pirâmide"). Termine com a pergunta que segura o espectador. Escreva com palavras próprias, inspirado na técnica de `ref/VQPzrVMHWlg/hook.txt`.
- **Corpo:** 6–8 capítulos cronológicos, da pré-história ao Egito de 2026. Por exemplo: o Nilo e as origens → a unificação → as pirâmides e o Antigo Império → o Médio e o Novo Império → as dominações (persas, gregos e ptolomeus, romanos) → o Egito árabe, mameluco e otomano → os britânicos e Suez → o Egito moderno. Em cada um: o que mudou, por quê e uma curiosidade marcante.
- **Fecho:** uma ligação com o presente e uma pergunta para os comentários.
- Fatos com fonte, e datas aproximadas ditas como aproximadas. Marque `[PENDENTE]` com uma versão alternativa e **não trave por isso**.

## Fórmula de hook (sintetizada de 6 vídeos de referência; os hooks reais estão em ref/*/hook.txt)
Vídeos: Egito (VQPzrVMHWlg, 417 mil views), Irã (XO1-4FH1X1I, 918 mil), Roma (kHCamT4zfH4, 364 mil), Jerusalém (zMn0RYC6U6w, 161 mil), China (wuhnBi8jNl0, 1,17 milhão), Império Britânico (cqGJ5ZRLAvs, 222 mil).
1. **Frase 1 = paradoxo ou contraste extremo**, dito como fato: "A China morreu mais vezes que qualquer país da Terra." · "Uma vila de lama na beira de um rio que acabou dona de todo o Mediterrâneo." · "Todo império cometeu o mesmo erro fatal." · "O Egito não é um país com um rio…"
2. **Prova em rajada:** 2–4 números ou fatos curtos e impossíveis em sequência ("destruída 2 vezes, sitiada 23, atacada 52, conquistada 44…") ou uma comparação de escala de tempo.
3. **A virada:** "Mas com X, algo impossível aconteceu." · "E aqui está a parte mais louca."
4. **A pergunta central**, que sustenta o vídeo inteiro: "Então como o Egito sobreviveu a…?" · "Como um bando de foras da lei construiu um império que se recusou a morrer por 2 mil anos?"
5. **(Opcional) A promessa do percurso:** "Nos próximos N minutos, 5 mil anos de história."
6. **Entrada imediata no corpo** com uma curiosidade estranha e concreta, sem enrolação ("Nossa história começa em…" e um fato bizarro, como os reis Shang perguntando aos avós mortos).
- Tudo em **até ~40 s**, com frases curtas, linguagem falada e sem "olá, pessoal" nem vinheta.
- Mantenha o tom ao longo do vídeo: cada capítulo abre com um mini-hook (contraste ou curiosidade) e fecha puxando para o próximo.
- Duração: as referências vão de 8 a 25 min (a da China tem 25 min e 1,17 milhão de views). Para o piloto, mantenha 15–17 min.

## 3. Voz
Use `tools/tts_fish.py historia-ptbr <blocos.json> <pasta> --video 3`: clone do Rodrigo, velocidade 1.0 e `s2.1-pro`. Tags com **moderação** (veja o `estilo.md`).

## 4. Visual (igual à referência)
- **Estilo:** o do `canal.yaml` (bonequinhos de cabeça redonda, traço grosso, cores chapadas). Os testes aprovados estão em `canais/historia-ptbr/testes/estilo/gpt-image-2/`.
- **Ritmo:** um plano novo a cada **2–4 s**, com zoom, pan e movimento leves. Sem legenda gravada no vídeo (a legenda vai só no `.srt`). Mapas ilustrados no mesmo estilo e cartões de data (ex.: "3100 a.C.") feitos no código, com fonte serifada.
- **Reuso de imagens, para cortar custo:**
  - Os **3 primeiros minutos** (hook e início) usam 100% de imagens inéditas.
  - Depois disso, até ~40% dos planos podem vir de **reenquadramento** da mesma imagem (aberto, zoom num detalhe, pan) ou de **imagens-âncora** que voltam de propósito (panorama, mapa do Nilo).
  - Nunca use o mesmo enquadramento duas vezes em menos de 60 s, e a imagem precisa sempre bater com o que está sendo narrado.
  - Meta: **cerca de 150–180 imagens únicas**.
- **Geração:** `tools/img_openai.py historia-ptbr <cenas.json> <pasta> --video 3`, em qualidade `low` (o padrão do canal). Em `cenas.json`, cada cena tem `id` e `prompt` descrevendo só o conteúdo; o estilo é adicionado sozinho.
- **Teto de custo de imagens: US$ 10 neste vídeo** (confira em `financas.consumo`). Se for passar disso, pare e pergunte ao Rodrigo.

## 5. Storyboard
Antes de gerar as imagens, monte `STORYBOARD.md`: para cada plano, o tempo, o trecho da narração, o id da imagem (nova ou reuso) e o movimento. Gere as imagens a partir dele.

## 6. QA e entrega
- Siga o QA de `playbooks/produzir-video.md`. Em especial: a duração, um contact sheet de ~20 frames e o ritmo (confira com `watch.py`, mirando ~14–20 cortes por minuto), além de voz limpa e nenhuma imagem desconexa da narração.
- Em `out/`: `video.mp4` (1080p30), `video-telegram.mp4` (até 45 MB), `thumbnail.jpg` (JPG com menos de 2 MB), `legendas.srt`, `youtube.txt` (título, descrição com capítulos em ordem crescente começando em 0:00 e tags) e `QA.md`.
- Atualize `youtube.videos` (id 3) com `status='pronto'`, o título final e `duracao_s`.
- **Resposta final:** um relatório curto (título, duração, nº de imagens únicas, custo total de `financas.custo_por_video` e pendências) e as linhas `MEDIA:` do `video-telegram.mp4` e do `thumbnail.jpg`.

## Autonomia
Você tem liberdade para contornar problemas e entregar. Não pare por pendências menores; registre-as. Só pare se for estourar o teto de custo (US$ 10 em imagens) ou se aparecer algo que só o Rodrigo decide. Não tente mandar mensagens de marco (em cron não há envio): a resposta final é entregue automaticamente.
