# RELATÓRIO: longo 01 do canal de clima (pt-BR), 08/11/2026

**Entrega:** `out/video.mp4` (11:19, 1080p30, −14,5 LUFS), `out/legendas.srt`, `out/thumb-1..3.jpg`, `out/contact-sheet.jpg` + os .md desta pasta. Drive: `gdrive:Youtube/Testes/clima-longo-01/`.
**Título sugerido:** "7 tornados em 6 dias: o que está acontecendo no Sul do Brasil?"
**Custo em dinheiro:** US$ 0 (`financas.consumo` id 137). **Render:** 2 h 48 min (41 partes de 500 quadros, ~0,49 s/quadro; o quadro de cortiça sem 3D sai a 0,08 s/quadro).

## O que foi feito
| Etapa | Como | Arquivos |
|---|---|---|
| Pesquisa de fatos | subagente Opus, 7 blocos, divergências marcadas | `pesquisa/FATOS.md`, `SOURCES.md` |
| Trechos reais | subagente: 61 candidatos (yt-dlp via WARP), 33 usados, TV descartada | `pesquisa/CLIPES.md`, `shared/clipes.py` |
| Material livre | satélite GOES-19/MODIS e SST (NASA GIBS), fotos do Commons com licença conferida, trilha Kevin MacLeod, SFX | `pesquisa/MATERIAL-LIVRE.md` |
| Roteiro | estrutura do brief; hook do piloto intacto | `ROTEIRO.md`, `shared/roteiro.py` |
| Voz | Kokoro `pf_dora` em 2 marchas (183 → 165 pal/min), perguntas com rampa de pitch | `shared/gera_voz.py`, `shared/monta_audio.py` |
| Storyboard | em código, amarrado às palavras do Whisper; 10 transições de cinema | `STORYBOARD.md`, `shared/build_cues.py` |
| Cena 3D | mapa do piloto ampliado até a Amazônia e os Andes; supercélula didática; satélite animado | `shared/cena3d.js`, `shared/prep_geo.py` |
| Camadas 2D | polaroid/monitor/celular, gráficos (barras, ONI, escala F, Brasil × EUA, meses), cortiça | `remotion/src/Longo.jsx` |
| Áudio | trilha com ducking, toc de madeira (pino), tum suave (número), whooshes/impactos nas transições | `shared/mix_audio.py` |
| QA | 0 pretas, 0 silêncios, Whisper 95,5%, 41% de tela real | `QA.md` |
| Thumbs | compostas no código: mapa do vídeo + quadro real + 2–3 palavras | `remotion/src/Thumb.jsx`, `out/thumb-*.jpg` |

## Decisões e correções relevantes
- **Fatos que caíram na checagem:** o "hook do avião" do RELATORIO do canal (o avião estava parado na pista; não há "70 nós" nem "paredes de vidro") e o "F4 de Piraí do Sul" (o Simepar classificou F3). "2º maior corredor do mundo" foi dito como "considerada por pesquisadores". San Justo fica a ~300 km da fronteira gaúcha (medido no mapa), não 350.
- **Datas oficiais:** Erval Grande/Itatiba/Barra do Rio Azul em 04/11 (o Climatempo diz 03/11). Só Maringá tem classificação F (F2).
- **Pixabay bloqueou download automatizado:** trilha de Kevin MacLeod (CC BY 4.0, crédito na descrição) e SFX do Commons ou sintetizados.
- **Rodrigo pediu trecho sem pedir autorização** (08/11): isso diverge do RELATORIO do canal, que recomendava autorização por escrito. Seguido o brief; crédito na tela e na descrição.

## Aprendizados (Hipóteses para a futura bíblia do canal; o canal ainda não existe)
- Render 3D por partes de 500 quadros fica em 4–5 min por comando nesta VPS; 12 min ≈ 2 h 50 min. Trechos sem 3D (quadro de cortiça com `cobre3d`) renderizam ~6× mais rápido: dá para usar como respiro de render.
- As fontes OFL do projeto (Anton, Plex Mono) não têm ✓ ✗ ▶ □ ⚠ ◀: ícones precisam ser SVG.
- Setas 3D grossas (raio da escala do continente) atravessam a câmera quando ela desce para um plano fechado: cada seta precisa de `t2` antes do próximo close.
- Kokoro: `speed` muda pouco o ritmo percebido; o que mais "acalma" é a pausa controlada entre frases (gerar frase por frase e juntar com silêncio medido).
- Kokoro + loudnorm de uma passada não chega a −14 LUFS (pico alto): precisa de compressor + limitador antes.

## Pontos para o Rodrigo conferir (tempos conferidos na `out/legendas.srt`)
| Tempo | O quê |
|---|---|
| 0:00–0:49 | hook na velocidade do piloto; 0:34–0:40 as 3 perguntas com a nova entonação |
| 0:50–1:21 | passagem para a marcha mais calma (transição em 2 blocos) |
| 0:50 | 1ª transição de cinema (atravessa a nuvem) e trilha/SFX novos (toc de madeira nos pinos) |
| 1:34–2:10 | Chapecó: satélite animado, câmeras do Portal Chapecó, manchete do avião |
| 3:25 | corte seco para o "arquivo" + carimbo "NÃO." |
| 5:47–6:30 | supercélula 3D explicada |
| 6:59 | El Niño (temperatura do mar + gráfico desde 1950) |
| 10:09–10:50 | quadro de cortiça "O que fazer" |
| 11:11 | CTA final |

## v2 (08/11/2026): voz ElevenLabs v3 + texto sem "caixinhas"
**Entrega:** `out/video-v2.mp4` (10:22, 1080p30, −14,1 LUFS), `out/legendas-v2.srt`, `out/contact-sheet-v2.jpg`, `QA-v2.md`, `PUBLICAR.md` com os capítulos novos. Drive: `gdrive:Youtube/Testes/clima-longo-01/v2/`. Thumbs sem mudança (nenhum texto citava "caixinha").
**Brief:** `~/workspace/referencias/BRIEF-clima-longo-01-v2.md`.

| Etapa | Como | Arquivos |
|---|---|---|
| Texto | b05–b07 reescritos (pergunta → "Isso nos leva às seguintes perguntas." → 3 perguntas → "Mas antes…"); b25, b37 e b42 sem "caixinha"; abas "PERGUNTA 1/3, 2/3, 3/3" | `shared/roteiro.py` (`fala` limpa + `fala_tts` com tags) |
| Voz | ElevenLabs `eleven_v3`, voz Fernanda, stability 0,0 / similarity 0,8, um request por bloco, `mp3_44100_128`; tags `[serious]`, `[curious]`, `[intrigued]` | `shared/gera_voz_eleven.py`; brutos em `audio/eleven-brutos/` (fora do git, com `log.json` dos textos) |
| Velocidade | atempo: hook b01–b06 1,3×, b07 1,25×, resto 1,2× | `shared/monta_audio_v2.py` |
| Conferência | Whisper por bloco (números normalizados), tag falada, "?" nas perguntas; 7 blocos com retake | `shared/normaliza_pt.py`, `shared/compara_takes.py`, `work/confere_voz_v2.txt` |
| Sincronia | tempos de frase e palavra vêm do Whisper de cada bloco; `build_cues.py` com âncoras ajustadas para a grafia nova do Whisper ("Shanxerê", "Humidade", "F -4"…) | `shared/tempos.json`, `shared/whisper.json`, `shared/cues.json` |
| Render | 38 partes de 500 quadros, uma por vez (211–340 s cada; ~2 h 40 min) | `shared/render.sh` (junta → `out/video-v2.mp4`) |

**Palavras por minuto:** hook (b01–b06) **144**; passagem (b07) 201; resto **173** (v1: 183 e 165).
**Créditos ElevenLabs:** 61 requests, **12.234 caracteres enviados** (10.060 do texto final + 2.174 dos retakes). O contador do plano foi de 1.087 para **5.983 de 38.634** (subiu 4.896: o v3 contou menos de 1 crédito por caractere). `financas.consumo` id 140, custo 0 (assinatura no `financas.lancamentos` id 51).

### Aprendizados (Hipóteses para a futura bíblia do canal)
- **v3 + tags:** `[curious]` antes da pergunta resolve a entonação na maior parte dos casos (10/10 com "?" no Whisper, contra 6/10 da Kokoro com rampa de pitch), mas 1 de cada ~8 blocos sai com palavra trocada ou inventada ("Santa Augusto", "arrasou", "Exposure"). Conferir com Whisper por bloco e refazer só o bloco é barato (~200 caracteres).
- **Whisper para conferir número:** compare com os números normalizados (`normaliza_pt.py`); senão "250 km" vs "duzentos e cinquenta quilômetros" derruba a nota sem erro de fala.
- **Hook com muitas perguntas fica lento no v3**, mesmo com atempo maior: as pausas dramáticas comem o ganho. Para hook corrido, atempo ~1,4 ou menos tags `[serious]` no hook.
- O que não depende da voz (cues, cena 3D, mix) foi re-sincronizado só re-rodando `build_cues.py` → `mix_audio.py` → render: amarrar tudo a palavra falada (não a segundos fixos) fez a troca de voz custar só ~10 âncoras ajustadas.

### Tempos para o Rodrigo ouvir (conferidos na `out/legendas-v2.srt` e no Whisper do vídeo final)
| Tempo | O quê |
|---|---|
| 0:29 | "Então... o que está acontecendo no Sul do Brasil? Por que tantos eventos…" |
| 0:37–0:46 | "Isso nos leva às seguintes perguntas." + as 3 perguntas (0:39, 0:41, 0:44) |
| 3:13 | "Isso é inédito?" |
| 4:36 | "Então, por que isso acontece justamente aqui?" (PERGUNTA 1/3) |
| 7:00 | "E o aquecimento global?" |
| 7:13–7:17 | "E a pergunta que todo mundo no Sul está fazendo: isso vai voltar a acontecer?" (PERGUNTA 2/3) |
| 8:09–8:13 | "Agora, a pergunta mais difícil: até onde isso pode chegar?" (PERGUNTA 3/3) |
| 9:56 | "Então, o que está acontecendo no Sul?" |
