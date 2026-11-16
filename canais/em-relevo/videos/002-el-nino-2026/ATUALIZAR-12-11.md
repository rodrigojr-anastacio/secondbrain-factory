# ATUALIZAR em 12/11/2026 (boletim da NOAA/CPC, ~11h de Brasília)

> **Visual v2 (10/11/2026):** o vídeo no ar/Drive agora é o render `LongoV2` (mistura satélite A + relevo editorial B, fotos grandes). Para o boletim, use **`shared/render_v2.sh`** (passo 4 abaixo), não o `shared/render.sh` antigo (que renderiza o visual v1). O slot b19–b21 = blocos 64–78 de `work/partes_v2/plano.json` (quadros 7566–9251), todos no estilo B.

O boletim mensal do CPC sai na quinta, **12/11**: https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso_advisory/ensodisc.shtml
O vídeo foi produzido com o boletim vigente (**08/10/2026**). Só os blocos **b19, b20 e b21** dependem do boletim novo. Eles ficam num **slot de duração fixa** (`shared/slot.json`, criado na 1ª montagem com a ElevenLabs), com partes de render só deles. Trocar esses blocos **não mexe** em nada antes ou depois.

## O que conferir no boletim de 12/11
| Item | Hoje (boletim de 08/10) | Onde aparece |
|---|---|---|
| Status | El Niño Advisory · "strong-to-very strong likely through JFM 2027 (>83%)" | b20 (fala), b21 |
| Chance de evento histórico (RONI ≥ 2,5, o maior desde 1950) | 54% SON · **83% OND · 70% NDJ** | b20 fala + mostrador (`graficos.mostrador.de/ate`) |
| RONI do último trimestre | ASO = +1,97 ≈ **2,0** (o boletim novo deve trazer SON parcial ou o mesmo ASO) | b19 fala + número na tela + montanha 2026 |
| Data do boletim na tela | "BOLETIM DE 08/10/2026" | fonte do mostrador, barra de fontes (`fontes`, entrada do slot) |
| "No último boletim" | refere-se a 08/10 | b20 fala |

Também conferir (não muda o slot, só se quiser): probabilidades por trimestre do capítulo 4 (b40–b41: muito forte 100/96/81/46%; neutro AMJ 54%, MJJ 70%). Se mudarem, é só trocar os números em `build_cues.py` (gráfico `prob`) e re-renderizar as partes desse trecho (a fala não cita esses números).

## Cenários e texto exato
Os textos abaixo têm quase o mesmo tamanho do original, para caber na janela. Trocar em `shared/roteiro.py` (função `b(...)` do bloco, campo de fala e de tela).

### A) MANTÉM (chance de recorde ainda entre ~60% e ~85%, RONI ≈ 2,0)
- **b19:** sem mudança (se o RONI novo for 2,1, troque "dois graus" → "dois graus e um décimo" e na tela "2 graus" → "2,1 graus").
- **b20 fala:** "No último boletim, a própria NOAA calculou entre **[X] e [Y]** por cento de chance…" com os números novos de OND/NDJ (ou NDJ/DJF). Tela igual.
- **b21:** sem mudança.
- **Tela:** mostrador `de`/`ate` = X/Y; fonte "NOAA/CPC · BOLETIM DE 12/11/2026"; número do b19 se o RONI mudar.

### B) SOBE (chance de recorde > 85% ou RONI confirmado ≥ 2,2)
- **b19 última frase:** "Mas ainda não é o maior da história." → "E já encosta no recorde."
- **b20 fala:** "Pode virar? / **Está perto.** / No boletim desta semana, a própria NOAA calculou **[X]** por cento de chance de ele se tornar o mais forte desde mil novecentos e cinquenta, quando as medições começaram. / E os vinte e sete modelos…" (resto igual).
- **b21 última frase:** "Se vai virar recorde, a resposta vem nas próximas semanas." → "E tudo indica que vai virar recorde neste verão."
- **Tela:** mostrador `de`=`ate`=X (um número só); carimbo continua "MUITO FORTE".

### C) CAI (chance de recorde < 50% ou pico antecipado; o CPC de 09/11 já disse que o calor sob a superfície "diminuiu levemente" desde meados de outubro)
- **b19 última frase:** "Mas ainda não é o maior da história." → "Mas não deve ser o maior da história."
- **b20 fala:** "Pode virar? / **Ficou mais difícil.** / No boletim desta semana, a própria NOAA baixou para **[X]** por cento a chance de ele se tornar o mais forte desde mil novecentos e cinquenta. / Mas os modelos ainda apontam para um El Niño muito forte até fevereiro."
- **b21 última frase:** → "E, mesmo sem recorde, muito forte já é bastante."
- **b47 (fora do slot):** "Pode virar o maior desde mil novecentos e cinquenta." continua verdadeiro com chance menor; **não precisa mudar**. Se a chance cair abaixo de 20%, troque por "Pode até não bater o recorde." — isso muda b47 (fora do slot), e aí é preciso re-renderizar também as partes do final (b47–b48).
- **Tela:** mostrador `de`=`ate`=X; esconder o gráfico `modelos` só se os modelos também caírem.

O título e as 3 thumbs valem nos 3 cenários (são perguntas).

## Passo a passo (≈ 1 h 15 min, quase tudo render)
```bash
cd ~/workspace/fabrica-youtube/pesquisa/canal-clima-2026-11/longo-02
# 1. editar shared/roteiro.py (b19–b21) e, se preciso, os números do slot em shared/build_cues.py (mostrador, fontes)
python3 shared/roteiro.py
# 2. voz só dos 3 blocos (~700 caracteres) e montagem com o slot fixo
python3 shared/gera_voz_eleven.py b19 b20 b21
~/workspace/fabrica-youtube/tools/.venv/bin/python shared/monta_audio_v2.py     # encaixa no slot (atempo extra se passar)
# 3. conferir que os tempos fora do slot não mudaram (diff em work/confere_voz_eleven.txt) e regenerar cues, mix, srt
python3 shared/build_cues.py && ~/tts/venv-kokoro/bin/python shared/mix_audio.py && python3 shared/gera_srt.py
# 4. re-render só do slot no VISUAL V2 (mistura A/B + fotos grandes; o slot é todo estilo B) + junção
#    são 15 blocos (~20–40 min de render, conforme a carga da VPS); cada "continua" roda < 10 min: repita até aparecer "faltam 0 de 185 blocos"
REBUNDLE=1 bash shared/render_v2.sh slot
bash shared/render_v2.sh continua 420     # repetir até "faltam 0"
bash shared/render_v2.sh junta
# 5. QA rápido do trecho e entrega
bash tools/qa.sh out/video.mp4 out/contact-sheet.jpg
rclone copy out/video.mp4 "gdrive:Youtube/Em Relevo/002-el-nino/" && rclone copy out/legendas.srt "gdrive:Youtube/Em Relevo/002-el-nino/"
```
Confira na `out/legendas.srt` o tempo do b20 antes de pedir para o Rodrigo ouvir.
