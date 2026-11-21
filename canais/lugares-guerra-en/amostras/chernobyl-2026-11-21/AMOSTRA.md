# AMOSTRA fase 1: Chernobyl, "o relógio de 67 h" (Clearance Required), 21/11/2026

Abertura do vídeo (bloco 0 da `PROPOSTA.md`, com a plantação de C e B) em **46 s**, 1920×1080 30 fps, para o Rodrigo avaliar linguagem, ritmo, voz e áudio de época **antes** do vídeo inteiro. Não é vídeo de produção: `youtube.videos` id **54** (status `ideia`) existe só para o custo.

- `out/amostra.mp4` (1080p, 115 MB, -14,9 LUFS, pico -1,4 dBTP) · `out/amostra-720p.mp4` (7,2 MB, para o chat) · `out/frames.jpg` (grade de 12 quadros) · `out/legendas.srt`
- Drive: `Youtube/Clearance Required/chernobyl-amostra/`
- Código: `src/Amostra.jsx` (componentes), `tools/prep.py` (mídia, mapa, mix, `src/timeline.json`), `tools/tts_voz.py` (Fish com outra voz, para o TASS)
- Faixa "cinema" 2,35:1: **não usei** (16:9 cheio; a régua e o contador já ocupam o topo).

## Segundo a segundo
| Tempo | Tela | Áudio |
|---|---|---|
| 0:00–0:09 | Tela quase preta com grão, rótulo da linha (despacho → bombeiros da usina, Ivankov, Polesskoye), **forma de onda** ciano, selo **ARCHIVE AUDIO**, legenda russo + inglês | **Real:** chamadas do despacho dos bombeiros ("Explosion at the main building, units 3 and 4." / "Are there people there?" / "Yes."), estática de rádio na entrada |
| 0:09–0:10 | **Glitch de sinal** (faixas deslocadas, separação ciano/ferrugem, ruído) | estática; trilha em silêncio |
| 0:10–0:11 | "26.04.1986 — 01:23:40" **datilografado** no centro | máquina de escrever + tique do relógio |
| 0:11–0:15 | Mural entra: página do **INSAG-7, Tabela I-I**; câmera mergulha na linha **01:23:40 EPS-5 button was pressed** e o grifo amarelo passa. Nascem a **régua de horas** (26–28/04, marcos AZ-5 · BUSES · FORSMARK · TASS) e o **contador duplo** (decorrido + hora local), parado em 00:00:00 / 01:23:40 | N1 "At 1:23 and 40 seconds, the night shift pressed the emergency shutdown button." · drone entra |
| 0:15–0:18 | Polaroid da sala de controle do bloco 4 (hoje) cai com fita; **glitch** em "blew apart" | N2 "Seconds later, Reactor Four blew apart." · tum surdo (sem explosão de filme) |
| 0:18–0:25 | **Satélite KH-9 de 1984**, push-in lento; círculos desenhados na usina ("CHERNOBYL NPP · UNIT 4") e em Pripyat ("~49,000 PEOPLE"). **O contador dispara**: 00:00:00 → | N3 "Between that button and the moment Moscow told the world, 67 hours and 36 minutes went by." · pulso grave + tique |
| 0:25–0:29 | Cartão datilografado com o texto do anúncio (ônibus às 14:00, "for the first while"), carimbo **TEMPORARY** em "Temporarily" | N4 "In those hours, a whole city was told to leave. Temporarily." · carimbo |
| 0:29–0:32 | Selo ARCHIVE AUDIO, onda, legenda com **TEMPORARY** em amarelo; o contador passa de 36 h (27/04 ~14:00) | **Real:** rádio de Pripyat, "…провести временную эвакуацию…"; trilha quase muda |
| 0:32–0:36 | **Mapa 2D da Europa**, a pluma amarela vai de Chernobyl a **Forsmark**; polaroid Anefo (medição na Holanda, 01/05/1986). Contador chega a ~56 h (28/04 ~09:00) | N5 "The first alarm outside the Soviet Union went off in Sweden." |
| 0:36–0:42 | Contador **para em 67:36:20 / MON 28 APR 21:00:00**. Teletipo **ТАСС** datilografa o texto russo; selo **RECONSTRUCTION · SYNTHETIC AUDIO** + "TEXT: TASS, 28 APRIL 1986, 21:00 MOSCOW · READ IN ENGLISH"; legenda | **Recriado:** TASS lido em inglês por voz sintética, com filtro de rádio, sem imitar o locutor do Vremya |
| 0:42–0:46 | Zoom-out revela o **mural inteiro**; o contador cresce para o centro: "67:36:20 · FROM THE BUTTON TO THE BULLETIN"; fade | N6 "And every one of those hours left a paper trail." |

## Real × recriado
| Item | Status | Selo na tela |
|---|---|---|
| Chamadas do despacho dos bombeiros (70 s; usei 0:04,8–0:13,1) | **Real** (Commons, PD-UA-exempt; conteúdo confirmado pelo INSAG-7 §II-2.3.4; cópia online mais antiga de 2013). Só passa-faixa e nível, sem "melhorar" | ARCHIVE AUDIO |
| Anúncio da rádio de Pripyat (usei 0:55–0:58) | **Real** (Commons, PD-UA-exempt; voz de Nina Melnik, pripyat.com desde 2005) | ARCHIVE AUDIO |
| Boletim TASS de 28/04, 21:00 | **Recriado**: texto literal (PD), voz sintética Fish "news reporter" (`05aff7ff…`), em inglês | RECONSTRUCTION · SYNTHETIC AUDIO |
| Narração | Voz sintética do canal (Fish "Narrator" Max N, `0327fdb5…`, s2.1-pro, por frase) | (declarar na descrição) |
| Cartão "27.04.1986 · PRIPYAT CITY RADIO" e teletipo ТАСС | Grafismo nosso com **texto literal** da fonte | QUOTED / "TEXT AS PRINTED IN PRAVDA" |
| Mapa da Europa e trajeto da pluma | Grafismo nosso | SCHEMATIC · PATH APPROXIMATE |

## Fontes, licenças e créditos usados (todos na tela, canto inferior esquerdo, Plex Mono 20 px, legível a 1080p)
| Material | Origem | Licença | Crédito na tela |
|---|---|---|---|
| Despacho dos bombeiros | [Commons: Records_of_telephone_conversations…ogg](https://commons.wikimedia.org/wiki/File:Records_of_telephone_conversations_in_the_night_of_the_Chernobyl_disaster.ogg) | PD-UA-exempt | Audio: fire-service dispatch calls, 26 Apr 1986 · via pripyat.com / Wikimedia Commons |
| Rádio de Pripyat | [Commons: Pripyat_1986.ogg](https://commons.wikimedia.org/wiki/File:Pripyat_1986.ogg) | PD-UA-exempt | Audio: Pripyat city radio, 27 Apr 1986 · via pripyat.com / Wikimedia Commons |
| INSAG-7, p. 55 (Tabela I-I) | [IAEA Pub913e_web.pdf](https://www-pub.iaea.org/MTCD/publications/PDF/Pub913e_web.pdf) | termo da IAEA: uso comercial com crédito | Document: IAEA, INSAG-7 (1992), Table I-I · Source: IAEA |
| Sala de controle do bloco 4 (2025) | [Commons](https://commons.wikimedia.org/wiki/File:Physics_student_inside_the_Control_Room_of_Unit_4_at_Chernobyl_NPP.jpg) (recorte só dos painéis) | CC0 | Photo: Bibric02 / Wikimedia Commons (CC0), 2025 |
| KH-9, 29/01/1984 | [Commons: Припять 1984.jpg](https://commons.wikimedia.org/wiki/File:Припять_1984.jpg) (USGS EarthExplorer) | PD-USGov-USGS | Satellite: KH-9 Hexagon, 29 Jan 1984 · U.S. Geological Survey (declassified) |
| RIVM, Holanda, 01/05/1986 | [Commons: Anefo 933-6456](https://commons.wikimedia.org/wiki/File:Onderzoek_naar_veranderde_Radioactiviteit_door_RIVM_na_nucleaire_ramp_in_Sovjet_,_Bestanddeelnr_933-6456.jpg) | CC0 (Nationaal Archief) | Photo: Rob Croes / Anefo, Nationaal Archief (CC0) |
| Mapa | Natural Earth 50m | PD | Map: Natural Earth |
| Texto TASS | tass.ru (via ruwiki), UPI 28/04/1986, Pravda 29/04 | notícia/ato oficial (PD) | Synthetic voice reading the TASS text of 28 Apr 1986 · not the original broadcast |
| Máquina de escrever (SFX) | "WWS Typewriter", Work With Sounds / Konrad Gutkowski, Commons | CC BY 4.0 | só na descrição (como no Em Relevo) |
| Trilha (drone + pulso), estática, tique, papel, carimbo, tum | sintetizados em `tools/prep.py` (numpy) | nossos | — |
Nenhuma imagem com dono entrou (a regra nova permite com crédito, mas não precisou): nada de HBO, Getty/AP/Reuters, Kostin, vítimas ou hospital.

## Custo
| Item | US$ |
|---|---|
| Fish: narração (407 bytes) + TASS (109 bytes), s2.1-pro | 0,008 |
| Runpod: 1ª tentativa (A4000, 299 s, reprovada num quadro quase preto) + render final (4090, 182 s) | 0,059 |
| **Total** (registrado em `financas.consumo`, vídeo 54) | **≈ 0,07** (teto 3,00) |

## QA
- 1920×1080, 30 fps, H.264 + AAC, 46,0 s (1380 quadros conferidos pelo `render_runpod.sh`; SSIM 480p mín. 0,943).
- Loudness -14,9 LUFS, pico -1,4 dBTP (o mix saiu a -0,6 e passei um limitador antes de remuxar).
- Nenhuma tela preta ≥ 0,2 s fora do fade final (blackdetect vazio).
- Legenda × áudio: tempos das legendas tirados do Whisper (word timestamps) do despacho e do anúncio, e do silêncio entre as 2 frases do TASS; as 6 frases da narração conferidas no Whisper (texto idêntico).
- Render: a 1ª rodada reprovou o quadro 1374 (fade para o preto, SSIM 0,943 estável nas 2 rodadas, imagem correta conferida); refeito com `LIMIAR_MP4=0.93`.

## O que melhorar no vídeo inteiro
1. **Transcrição do despacho revisada de ouvido** por quem fala russo antes de legendar o trecho longo (bloco 4); aqui usei só as 3 falas que o Whisper e o `MATERIAL.md` concordam.
2. **Retrato rasgado** e **painel de medidores** (P2) não entraram: não há retrato livre de operador. No vídeo, o rasgo serve para então × agora (KH-9 1984 × Sentinel hoje).
3. **Documentos originais** que ainda faltam baixar no navegador: ordem dos 1.125 ônibus (Wilson 208406), CIA de 29/04, Pravda de 29/04. O cartão datilografado e o teletipo são grafismo com texto literal: no vídeo, trocar pelos scans quando houver.
4. O mural pede **mais densidade no zoom-out** (no vídeo inteiro ele acumula ~40 itens; aqui são 7).
5. Ritmo: o contador correndo 67 h em 17 s funciona como gancho; no vídeo a granularidade muda por bloco (minuto, segundo, hora), como na `PROPOSTA.md`.
6. O bloco 0 cita "Moscow told the world" (condição do crivo para o par A) e planta B (Suécia). A ordem dos ônibus (par C) ficou só no cartão; no vídeo ela é dita no bloco 0.
7. Trilha sintetizada serve para a amostra; no vídeo, avaliar uma cama CC0 com mais textura.
8. Voz do TASS: "news reporter" do Fish com filtro de rádio. Se soar falsa demais, testar uma voz mais neutra ou só a cartela com texto.
