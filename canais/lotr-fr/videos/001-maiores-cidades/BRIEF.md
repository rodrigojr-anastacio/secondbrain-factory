# BRIEF — vídeo de 8 min: « Quelles étaient les plus grandes villes de la Terre du Milieu ? »

Pedido do Rodrigo, repassado pelo manager (Claude). Você (Hermes) orquestra e confere; o Claude Code (skill `claude-code`) implementa.
Siga o ~/workspace/AGENTS.md: delegue em etapas, sem trabalho braçal seu, sem pesquisa extra além do necessário.

## Entrega
- Vídeo 16:9, 1920×1080, 30 fps, **7:30–8:30 min**, narração em **francês**.
- Pasta do projeto: `~/workspace/lotr-cidades` (novo projeto Remotion; pode copiar o setup e componentes de `~/workspace/lotr-pilot`, sem alterar o lotr-pilot).
- Saídas em `out/`: `cidades-fr.mp4` (qualidade final), `cidades-fr-telegram.mp4` (≤ 45 MB, para enviar no Telegram), `cidades-fr.srt`, `thumbnail.png`, `description.txt` (descrição YouTube + créditos das imagens), `QA.md`.

## Modelo de referência
Modelado no vídeo de maior sucesso recente do canal Darth Gandalf: "What were Middle-earth's largest cities?" (76K views em 11 dias, 9:58). NÃO traduzir nem copiar o texto dele; usar a mesma estrutura com roteiro próprio.

Estrutura:
1. **Hook (0–45 s):** comece pelo familiar (Minas Tirith, Khazad-dûm, Osgiliath, Umbar…) → virada ("só as vemos na pior fase delas") → pergunta ("qual foi a maior?") → credibilidade ("Tolkien quase não dá números; vamos estimar com o que o texto permite") → **loop aberto**: "e qual foi a maior de toda Arda, eu revelo no final".
2. **Corpo cronológico:** a "coroa" de maior cidade passa de uma cidade para outra ao longo das Eras (Primeira Era: Brithombar/Eglarest, cidades anãs, Nargothrond, Menegroth, Gondolin; Segunda Era: Khazad-dûm, cidades numenorianas na Terra-média como Pelargir e Umbar; Terceira Era: Osgiliath, Minas Anor/Tirith, Umbar, Pelargir…). Para cada troca: por que cresceu, por que caiu.
3. **Payoff no final:** a resposta para Arda inteira (ex.: Númenor/Armenelos, com o dado de Tolkien sobre a população da ilha, se a fonte confirmar).
4. **Fecho:** pergunta para os comentários.

Roteiro: ~1.150–1.250 palavras em francês natural (público francófono), frases curtas, ritmo de narração. Nomes no padrão das traduções francesas (Daniel Lauzon quando possível). Fatos só com fonte (Silmarillion, Contos Inacabados, Apêndices, HoME, Cartas); onde for estimativa, dizer que é estimativa. Gerar `SOURCES.md`.

## Voz
Kokoro, voz **`ff_siwis`** (aprovada pelo Rodrigo), local na VPS: `~/tts/venv-kokoro/bin/python`, `KPipeline(lang_code="f", repo_id="hexgrad/Kokoro-82M")`, `voice="ff_siwis"`, 24 kHz. Exemplo em `~/tts/gen_kokoro.py`. Gerar por parágrafo (facilita sincronia e ajuste). Não usar Piper nem Edge TTS.

## Visual (motion — estilo que o Rodrigo vem testando)
Base: o estilo da v3 do lotr-pilot (pergaminho, mapa animado com rotas e marcadores, tipografia serifada). Corrigir os problemas apontados na v3:
- **Sem texto redundante:** não repetir a frase da narração em título grande + legenda ao mesmo tempo. Legenda embaixo; na tela, no máximo palavras-chave (nome da cidade, Era, número estimado).
- **Sem ícones vetoriais chapados** (barquinhos, silhuetas, livro desenhado). Use ilustrações com Ken Burns/parallax e o mapa animado.
- **Nada de sobreposição** de legenda com caixas/legendas do mapa; camadas nunca semitransparentes se misturando.
- Créditos das imagens: pequeno, discreto no canto ("Art by X"), e lista completa em `description.txt`.
- Troca de visual a cada ~4–8 s; um "placar" recorrente mostrando a cidade que detém a coroa ajuda a costurar o vídeo.
- Música de fundo leve com ducking sob a voz (pode reaproveitar `music_bed_v3.wav` do lotr-pilot ou gerar trilha original).

## Imagens
O Rodrigo **autorizou buscar imagens no Google** (ilustrações/fan art das cidades, mapas). Dê crédito ao artista quando identificável. **Não usar frames dos filmes/séries** (Content ID). Preferir ilustrações de qualidade em boa resolução.

## Fluxo
1. Briefing completo ao Claude Code para a etapa 1: roteiro FR + SOURCES.md + storyboard (cena, tempo, visual, texto na tela). **Você confere** fatos e o hook contra este brief.
2. Etapa 2 (Claude Code): imagens, narração Kokoro, implementação Remotion e render. Rode em background com timeout longo; acompanhe sem ficar relendo arquivos.
3. **QA antes de entregar (você):** duração 7:30–8:30; contact sheet de ~20 frames + 4 frames-chave — sem texto cortado/sobreposto, sem tela vazia, sem frame de filme; áudio sem cortes/clipping e voz sempre acima da música; legenda sincronizada; créditos na descrição. Se algo falhar, devolva ao Claude Code com a correção exata (máx. 2 rodadas). Registre em `QA.md`.
4. Entrega: resumo curto (título sugerido, duração, o que conferiu, pendências) + o `cidades-fr-telegram.mp4` e a thumbnail.

## Autonomia e comunicação
- Você tem **liberdade para contornar problemas e entregar**. Não pare nem cancele: corrija, use alternativas e siga. Pendências menores vão para o relatório final, não bloqueiam.
- Etapa 1 já existe (`SCRIPT_FR.md`, `SOURCES.md`) e está aprovada pelo manager: use o texto de repli onde houver `[PENDENTE]` (ex.: P18b sem número). O storyboard pode ser feito junto da etapa 2.
- Não tente mandar mensagens de marco (em cron não há envio); sua resposta final é entregue no Telegram automaticamente.
