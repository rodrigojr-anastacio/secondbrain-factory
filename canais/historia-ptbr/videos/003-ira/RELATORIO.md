# RELATÓRIO v2 · historia-ptbr/003 · "A história INTEIRA do Irã em 18 minutos" (youtube.videos id 5)

Job: `~/workspace/referencias/BRIEF-historia-003-v2-fase2.md` (05/11/2026), com as decisões do Rodrigo da fase 1. Orquestrador: Claude Code (Opus), numa sessão `claude -p`. Nada foi publicado nem enviado ao Telegram. O relatório da v1 está em `RELATORIO-v1.md`, a entrega v1 em `entrega-v1/` e a mídia v1 em `v1-midia/` (fora do git).

## Entrega (`entrega/`)
- `video.mp4`: **18:01**, 1080p30, H.264/AAC, −15,2 LUFS, pico −4,2 dBFS. 0 telas pretas e nenhum silêncio > 1,5 s.
- `legendas.srt`.
- `thumb-1-coroa-turbante.jpg` (principal), `thumb-2-persia-roma.jpg` e `thumb-3-petroleo-cia.jpg`: 1280×720, de 202 a 272 KB.
- `pacote.md`: título, descrição, 12 capítulos, fontes, tags e checklist (com a medição do teste do hook).

## O que foi feito, por decisão
1. **Roteiro** (`roteiro.py` v2, fonte única):
   - Molde HiM da `ESTRUTURA-ROTEIRO.md`, com hook + 10 eras + fecho, 90 blocos e **2.282 palavras**.
   - Títulos-frase só na placa; fio da língua e do paraíso; fio do turbante contra a coroa.
   - **Hook = a anedota do cavalo de Dario** (TEXTO_A do `amostras-voz/ab.py`, reescrito "contado"). As 3 primeiras frases: *"Pérsia, quinhentos e vinte e dois antes de Cristo. Seis nobres têm um problema: quem vai governar o maior império do mundo? A solução é… estranha."* Seguem "Essa é a história inteira do Irã…", a promessa em lista e "Guarde esse cavalo. Ele volta no final."
   - O cavalo é retomado 3 vezes:
     - era 2: "aquele rei escolhido pelo cavalo. Lembra? Dario.";
     - era 3: "Inclusive o cavalo de Dario, contado por um grego.";
     - **fecho**: "E o cavalo? … o Irã escolheu um rei pelo relincho de um cavalo… Quem escolhe quem governa o Irã? Desde aquele cavalo, essa pergunta nunca teve uma resposta tranquila." Isso liga Dario a Mojtaba, "um filho escolhido numa sala de clérigos". O fecho volta depois ao jardim de Ferdowsi.
   - O caixão continua como clímax da era 4.
   - Medidas do texto:
     - 182 frases, com 12,5 palavras por frase em média;
     - 16 perguntas;
     - nenhuma sequência de 3 frases abrindo com data.
   - Fatos novos (Heródoto III.83–87 e outros) estão em `SOURCES.md` §v2.
2. **Voz:** Fish **drama-3**, clone `48613fc6…`, 1 chamada por bloco (técnica B2), velocidade 1,0, temperature e top_p no padrão, gaps de 0,35/0,9/1,5 s no `build.py`.
   - **Os 60 s iniciais medidos antes do resto:**
     - repetição melódica **0,09** (meta ≤ 0,12);
     - queda no fim da frase −2,94 st;
     - faixa p10–p90 de 11,0 st;
     - F0 mediano de 103 Hz.
   - O hook inteiro + o 1º bloco (106 s) mediram 0,15, 133 ppm e Whisper 97,6%.
   - **Cobrança confirmada no drama-3** pelo crédito do Fish:
     - 48,68132 → 48,66826 = US$ 0,01306 = 1.306 bytes × US$ 10/M;
     - 48,66826 → 48,55041 = US$ 0,11785 = 11.785 bytes × US$ 10/M.
     - No s2.1-pro, seriam 0,0196 e 0,1768.
   - **Whisper por bloco (`qa/voz_blocos.json`):**
     - bruto: média 96,3%, mínimo 81,1%;
     - todos os blocos abaixo de 95% eram grafia de nome persa ou de "xá" ("cha", "canats", "Nasser", "Mostaba"), ou número em algarismo;
     - com a chave fonética (`v2-voz/qa_fonetico.py`): **mínimo 96,0%, média 99,5%**, 0 tags faladas.
   - O drama-3 é agora o padrão do canal (`canal.yaml`: `modelo: drama-3`, `modo: bloco`) e do `tools/tts_fish.py`, que ganhou preço promocional por data, cache por bloco e leitura de crédito antes e depois.
3. **Imagens:** `google/nano-banana-2.1/edit` + 3 refs gpt-image-2 do canal (Egito I041 e I120, Índia I041), 1K reescalado para 1536×864, `thinking_level: minimal`.
   - **Lote-prova de 6 cenas** (`qa/v2-lote-prova*.jpg`):
     - cenários, mapa (limpo, sem letras, sem moldura) e multidões **aprovados**;
     - **reprovados os personagens com nome** (Dario, Ciro, o clérigo), que saíam com rosto barbado semi-realista.
   - **Correção:**
     - instrução de referência reforçada ("every person… round-white-head… beards and turbans are flat shapes… never realistic faces");
     - descrições dos personagens reescritas como "round-white-head cartoon king…";
     - na 3ª tomada, o clérigo e Ciro saíram bonequinhos.
   - Lote inteiro: 206 imagens, 0 falhas, conferidas em 6 pranchas (`qa/v2-prancha-1..6.jpg`).
   - Achados nas pranchas:
     - 2 refeitas por letras (I059 "BEAKER" num cartaz, I199 letreiros);
     - 0 pretas, 0 molduras;
     - 9 mapas sem letra, com rótulos no código (`src/labels.jsx`, conferidos em stills `qa/v2-stills/`).
   - Ficou de resíduo menor: "CONTRACT" num pergaminho (I160, palavra real e pequena) e letreiros miúdos ao fundo em I194/I195.
4. **Thumbs:** padrão COROA × TURBANTE (conflito cara a cara, os dois bonequinhos com raiva, raio no meio, datas em pílula no topo, 2 palavras embaixo). Base nano-banana com refs, 2 takes por conceito, texto em PIL (`v2-thumbs/compose_v2.py`):
   - 1 (principal) COROA × TURBANTE "1891 · 1979": refinada; agora o clérigo também é bonequinho, e não rosto semi-realista;
   - 2 PÉRSIA × ROMA "260 d.C.": Shapur × Valeriano acorrentado;
   - 3 PETRÓLEO × CIA "1953": Mossadegh com a torneira de petróleo × agente de chapéu e óculos escuros com o maço de dinheiro.
   - Todas legíveis a 320 px (`v2-thumbs/prancha-celular.jpg`).
5. **Recarga do fal** (pedido do Rodrigo): lançada em `financas.lancamentos` id 49 (fal.ai, US$ 100, R$ 588,28, pré-pago).
   - **Saldo real (API `account/billing`) US$ 100,47 × banco US$ 104,24:** diferença de US$ 3,77 de consumo não lançado.
   - Lancei um ajuste em `financas.consumo` id 78 (sem vídeo), e o banco bateu com o painel.

## Custo direto da fase 2 (financas.consumo, ref_id 5, notas "v2…")
| Etapa | Itens | US$ |
|---|---|---|
| Voz drama-3: hook (medição) + vídeo inteiro + 1 bloco regerado | Fish, 13.195 bytes | 0,13 |
| Lote-prova de imagens (6 + 3 + 2 tomadas) | fal | 0,58 |
| Lote inteiro (206) | fal | 9,52 |
| Imagens refeitas por letras (2) | fal | 0,09 |
| Bases das thumbs (6) | fal | 0,28 |
| **Total** | | **US$ 10,59** (teto US$ 14) ≈ R$ 62,3 |
- O preço real do nano-banana-2.1/edit com 3 refs foi de **US$ 0,046/img** com `thinking_level: minimal` e US$ 0,058 com o padrão (`medium`), contra US$ 0,044 na bancada. O custo foi medido pela **API de uso por endpoint** do fal.
- A fase 1 tinha custado US$ 0,99. A v1 inteira, US$ 11,92.

## Falhas da esteira (o que quebrou, o improviso, a correção)
1. **O nano-banana desenha rosto realista quando o prompt descreve rosto** ("long square curled beard", "thick dark eyebrows"). As refs sozinhas não seguram os bonequinhos nos personagens com nome. Custou 2 rodadas de prova (US$ 0,23).
   - Correção (já aplicada): `ref_instrucao` no `canal.yaml` com a regra "todo personagem = cabeça redonda branca", e descrição de personagem sempre como "round-white-head cartoon …, simple flat beard shape". Está registrado na `biblia/visual.md`.
2. **O custo do fal medido pelo saldo estava contaminado.** O job `dossie-002` gastava no fal ao mesmo tempo: no lote 1, o saldo caiu US$ 8,76, e o meu uso foi de US$ 3,23. O `img_fal.py` antigo também registrava preço fixo.
   - Correção (aplicada no `tools/img_fal.py`): custo real pela API `v1/models/usage` **por endpoint**, com o saldo como plano B. Também: modelos `/edit` com `refs` do `canal.yaml`, reescala para o tamanho do canal, imagem preta/vazia = falha, `--so`, `--teto` e `--notas`.
   - O mesmo vale para o Fish: o crédito caiu US$ 0,17 a mais por outro job depois da minha geração. A confirmação do modelo só é confiável medindo logo antes e logo depois.
3. **Armadilhas de ferramenta encontradas no caminho:**
   - (a) O `canal.yaml` do canal **não era YAML válido** ("…: são do dossie-es" sem aspas). As tools caíam em fallback ou quebravam. Corrigido.
   - (b) O `tools/qa_voz_blocos.py` do vídeo **acumula** o JSON antigo (misturou 102 blocos da v1 com os 90 da v2) e reprova nome persa e "xá". Isolei a v1 e criei o `v2-voz/qa_fonetico.py`.
   - (c) O render passa de 10 min por comando: foi feito em 5 partes com o novo `tools/render_partes.sh` (só vídeo por faixa de frames + concat sem reencode + mix em AAC; ~20 fps em 2 vCPU).
4. **Duração e hook acima da meta da bíblia:**
   - o drama-3 fala ~125–133 ppm, e 2.282 palavras deram 18:01, contra o alvo de 15–17;
   - o hook do cavalo + promessa ocupa 1:31, no teto (o hook do HiM Irã também tem 1:32).
   - Para o próximo vídeo no drama-3: ~1.950–2.050 palavras para 15–16 min, ou testar `prosody.speed` 1,05.

## Para o Rodrigo
- Assistir e ouvir (`entrega/video.mp4`): o drama-3 no vídeo inteiro e o hook do cavalo.
- **Teste do hook:** depois de publicar, anote a retenção aos 30 s e aos 60 s (Studio) na `biblia/roteiro.md`.
- Publicar é decisão sua; o checklist está no `pacote.md`. Reconfirmar a frase "não há acordo de paz" (N083) na véspera.
- A promoção do drama-3 (US$ 10/M) termina em 12/11 17:00 UTC. Depois, o custo da voz de um vídeo sobe de ~US$ 0,13 para ~US$ 0,65.
