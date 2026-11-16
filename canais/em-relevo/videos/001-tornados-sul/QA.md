# QA: longo 01 do canal de clima (08/11/2026)

Método: skill `qa` (sem bíblia de canal: o canal ainda não existe; o julgamento é contra o brief, o piloto aprovado e `pesquisa/estilo-mapa-relevo-3d/PADRAO.md`). Saídas em `qa/` (fora do vídeo): `qa.txt`, `transcricao.json`, `voz_diff.txt`; contact sheet em `out/contact-sheet.jpg`.

## Critérios objetivos
| Item | Medido | OK? |
|---|---|---|
| Duração | **11:19** (meta ~12 min; brief "~12") | ✅ (-41 s) |
| Formato | 1920×1080, 30 fps, H.264 + AAC 48 kHz | ✅ |
| Loudness | **−14,5 LUFS**, pico −1,3 dBTP, LRA 1,8 (compressor + limitador + loudnorm na junção) | ✅ |
| Telas pretas ≥ 0,2 s | **0** | ✅ |
| Silêncios > 1,5 s | **0** | ✅ |
| Cortes no 1º minuto | **0** (scene > 0,3) | ✅ por desenho: câmera contínua dentro dos blocos, como o piloto; as 10 transições de cinema ficam entre blocos |
| Whisper (small) × roteiro, vídeo final | **95,5%** ponderado; pior bloco b25 (0,77: "por que" → "porque", bloco de 2 frases) | ✅ |
| Perguntas com entonação | 6 de 10 transcritas com "?" pelo Whisper | ⚠️ melhorou, não é perfeito (ver pendências) |
| Legenda `.srt` | 246 cartões tirados das palavras do Whisper; conferidos 0:34 ("Por que isso está acontecendo?"), 5:47 ("Uma tempestade comum sobe e chove.") e 11:11 ("Manda este vídeo…") | ✅ |
| Capítulos | 11, em ordem desde 0:00 (`PUBLICAR.md`) | ✅ |
| Thumbs | 3 JPG 1280×720 (76–120 KB), texto de 2–3 palavras legível a 320 px | ✅ |
| Material real na tela | **41%** do tempo (277 s de 679 s): 33 trechos de vídeo + 14 imagens + 3 folhas de satélite no mapa | ✅ (brief: ~40%, 25–35 trechos) |
| Zero TV/emissora | nenhum trecho de emissora; logos de patrocinador/rádio cortados | ✅ |
| Crédito na tela | todo trecho/imagem tem legenda + crédito no quadro; descrição lista autor e URL | ✅ |
| Custo em dinheiro | **US$ 0** (`financas.consumo` id 137) | ✅ |

## Conferência visual (stills em `work/stills/`, contact sheet)
- Hook igual ao piloto (pinos, fio vermelho, polaroids, contador 3 → 7, pergunta, caixinhas).
- Supercélula 3D: corrigida na 1ª rodada (a seta do jato atravessava a câmera e a nuvem estava no chão). Agora: vento baixo laranja, vento alto azul, rolo listrado deitado → em pé, torre girando, mesociclone, descida fria, funil tocando o chão (5:48–6:30).
- Ícones ✓ ✗ ▶ □ ⚠ ◀ apareciam como "tofu" (as fontes não têm os glifos): trocados por SVG antes do render.
- Legenda de um trecho saiu com placeholder ("10H3X"): corrigida antes do render daquele trecho.
- Contact sheet sem quadro quebrado, sem sobreposição grave; o quadro de cortiça (10:09–10:50) renderiza sem o 3D (mais rápido).

## Pendências (para o Rodrigo decidir)
1. **Perguntas:** 4 das 10 ainda soam pouco interrogativas para o Whisper ("Isso é inédito?" 3:28, "Por que isso acontece aqui?" 5:05, "E o aquecimento global?" 7:39, "Até que proporção isso pode chegar?" 8:58). Ouvir; se incomodar, dá para reforçar a rampa de pitch só nessas frases (mesma duração) e refazer a junção do áudio, sem re-render do vídeo. Trocar de voz mudaria os tempos e exigiria re-render.
2. **Trilha e SFX não foram ouvidos por ninguém** (o job não tem ouvido): trilha Kevin MacLeod a −21 dB com ducking de 55% sob a voz; toc de madeira real (Commons) nos pinos; "tum" abafado a −30 dB nos números. Se algum som incomodar, ajusta-se em `shared/mix_audio.py` e refaz só a junção (`shared/render.sh junta`, ~1 min).
3. Algumas passagens têm mapa "vazio" por 2–4 s (ex.: 2:55 madrugada antes do satélite; 9:53 antes do funil). Aceitável no ritmo, mas é o ponto mais fraco do anti-monotonia.
4. Trechos de origem menos clara (Rádio Amigo do Povo, drone de Jolvani Bueno): ver `FONTES-E-LICENCAS.md`.
5. Reconferir El Niño (NOAA/CPC 12/11) e a contagem de tornados antes de publicar.
