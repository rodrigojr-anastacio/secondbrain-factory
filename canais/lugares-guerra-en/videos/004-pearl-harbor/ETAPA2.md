# ETAPA 2 PRONTA — 004-pearl-harbor (15–16/11/2026, Sonnet)

**youtube.videos id 42 → `pronto`.** Vídeo 15:06 (905,8 s), 1920×1080 30 fps, −15,0 LUFS (pico −2,7 dBFS), 0 telas pretas, 0 silêncios > 1,5 s, 19 cortes no 1º min (foto/arquivo; abaixo da meta de 21, aceito). Entrega em `entrega/` (video.mp4, thumb-A/B/C, thumbnail.jpg, legendas.srt, pacote/youtube.txt + checklist-publicacao.txt).

**Custo da etapa 2: ≈ US$ 0,83** (teto 4): Fish 0,214 · Runpod 0,441 (3 renders completos: o 1º, o do timecode e testes) · fal 0,119 (3 bases) · pré-QA 0,056.

## Promessa paga (conferida na `out/legendas.srt`)
- Frase-âncora "never patched / left there on purpose": **0:17–0:21**; "não chega perto da parede": 0:21–0:27.
- **Pergunta de T1 literal: 0:28** ("So why are there still bullet holes at Pearl Harbor?").
- "De quem é a parede" (working headquarters / PACAF): **0:36**; "a few miles from the dock": 0:43.
- Motivo oficial ("constant reminder"): **5:17** (janela 4:00–6:00 ok).
- Thumb final = conceito aprovado (parede art déco com 6 crateras ciano + sombra de avião + "ON PURPOSE" + RESTRICTED); A = T1, B = T2, C = "What's Still Behind the Gate at Hickam Field?".

## O que mudou em relação à etapa 1
1. **Distância corrigida:** coordenadas (Wikipedia) dão 2,6–2,9 mi (> 2,5) → "about two miles" virou **"a few miles"** no SCRIPT, `roteiro.py` (B02b, B17c), mapa `porto` e FATOS F81. `split_blocos.py` + `roteiro.py` rodados de novo antes da voz.
2. `roteiro.py` não exportava `tin/tout/vel` dos Filmes para o `storyboard.json` (build quebrava): corrigido.
3. **Mapas:** o Natural Earth 50m não tem o porto → `porto` e `memorial` saem **esquemáticos sem terra** (selo SCHEMATIC · POSITIONS APPROXIMATE); `oahu` com a ilha (escala 0,3°). QG da PACAF em vermelho no `memorial`.
4. **Timecode RTC** nos filmes NARA 76169 (P071, P131, P169): recorte de 12% no rodapé (`Filme`, `componentes.jsx`); vídeo re-renderizado inteiro.

## Voz
Fish Narrator s2.1-pro por frase, 71 blocos, 14,3 min, US$ 0,214. Whisper: média 99,2%, mínimo 90,4% no B06c (só "8.40/9.45" normalizado pelo Whisper; áudio dito certo "eight forty / nine forty-five"). Nomes (Hale Makai, Hickam, Higa, Kahuku, P.O.W. M.I.A.) conferidos sem falha.

## Pré-QA
200 stills (1 por plano) + 9 grades; `PREQA-visual.md`: 0 bloqueante, 5 médios (recortes de zoom/foto de vitrine e selos sobre documento: falsos positivos/estilo, anotados). Olho: grade 1, mapas e contact sheet conferidos; achado real = timecode RTC (corrigido).

## Render
Runpod em 4 partes (limite de 10 min por comando em primeiro plano) com `MUDO=1` + mix no fim (`volume=1.2dB` para chegar a −15 LUFS). Provas SSIM ≥ 0,999; nenhuma máquina reprovada.

## Para o Rodrigo conferir (tempo da legendas.srt)
Parede do hook 0:01; despacho "NOT DRILL" (B05b); bandeira 1941 × hoje (B11c); formulário NHL lido (B09b, ~5:50). Publicação planejada: qua 18/11.

## Pendências
- Cortes no 1º min: 19 (< 21); sem efeito na promessa.
- Pacote sem menção a IA (padrão 14/11); declarar "Uso de IA = Sim" no Studio (checklist).
