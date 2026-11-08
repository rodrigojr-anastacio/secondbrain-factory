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
