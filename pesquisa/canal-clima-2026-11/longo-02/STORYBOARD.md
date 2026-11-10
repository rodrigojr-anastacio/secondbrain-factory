# STORYBOARD: Em Relevo, vídeo 2 (Super El Niño 2026)

Storyboard em código: `shared/build_cues.py` → `shared/cues.json` (cada evento amarrado à palavra falada no Whisper ou ao início da frase). Cena 3D em `shared/cena3d.js`; camadas 2D em `remotion/src/Longo.jsx`. Tempos da versão final (ElevenLabs).

## Mudança pedida pelo Rodrigo (09/11)
Mapa 3D como base, mesclado com imagens reais: 12 fotos de chão com licença livre (Commons/Agência Senado/governos/NOAA) + 5 imagens de satélite (NASA GIBS/HLS), todas com crédito na tela (polaroid ou quadro de cortiça) e na descrição. Zero TV, zero vídeo de terceiros.

## Peças novas (além das do vídeo 1)
| Peça | Onde | Dado |
|---|---|---|
| Maquete do Pacífico (outra mesa, lon 95°E–295°E) | cap. 1, 2, 4 | Natural Earth |
| Relevo de calor (malha com altura = anomalia, 24 datas animadas de 03/06 a 08/11) | hook (costa do Peru), cap. 2, 4, resposta | NOAA OISST v2.1 |
| Diorama em corte do oceano (gangorra: termoclina e nível do mar mudam do normal para El Niño) | cap. 1 (b09–b11) | didático (NOAA PMEL) |
| Circulação de Walker (setas e nuvens que migram) | b10–b12 | didático |
| Globo com a anomalia | b12, b38 | NOAA OISST |
| Régua de montanhas (ONI → RONI, 2026 cresce ao vivo; linhas de recorde e "histórico") | b17, b19–b21 (slot) | NOAA/CPC |
| Termômetro Niño 3.4, mostrador 70–83%, 27 modelos, barras por trimestre, ano seguinte | b14, b20, b40–b42 | NOAA/CPC, IRI |
| UFs tingidas (previsão nov–jan), Monitor de Secas S2 ago→set, focos (ilustrativos), réguas de rio, pluviômetro, reservatórios, fumaça, chuva | cap. 3 e hook | Painel El Niño, ANA, Inpe, INMET |

## Slot [ATUALIZAR 12/11]
b19–b21 ocupam uma janela fixa (`shared/slot.json`) com partes de render só deles (`shared/render.sh slot`). Ver `ATUALIZAR-12-11.md`.

| # | Tempo | Transição | SFX |
|---|---|---|---|
| T1 | 1:02.0 | push-in que atravessa uma nuvem: do continente para a maquete do Pacífico inteiro | whoosh longo |
| T2 | 2:07.6 | whip pan: da maquete do Pacífico para o globo, que gira até o Brasil | swish + whoosh curto |
| T3 | 2:13.9 | corte seco para o 'arquivo' (sépia): pescadores do Peru no século 19 | impacto grave |
| T4 | 2:49.1 | rack focus: o termômetro desfoca e entra o Pacífico real | whoosh médio |
| T5 | 3:15.9 | whip pan: do Pacífico para a régua de montanhas de papel | swish + whoosh curto |
| T6 | 3:45.4 | whip pan: de volta ao Pacífico, que ganha um véu coral (o planeta mais quente) | swish + whoosh curto |
| T7 | 4:12.1 | whip pan: de volta à régua; as montanhas se redesenham com o termômetro novo (RONI) | swish + whoosh curto |
| T8 | 5:07.8 | rack focus: da régua para o Pacífico de hoje, com a prancha do que a ciência diz | whoosh médio |
| T9 | 5:24.7 | zoom-out orbital: do Pacífico para a América do Sul inteira | whoosh longo |
| T10 | 6:19.1 | whip pan vertical: do Brasil inteiro para Roraima | swish + whoosh curto |
| T11 | 7:06.2 | whip pan para o semiárido | swish + whoosh curto |
| T12 | 7:29.8 | whip pan para o Centro-Sul | swish + whoosh curto |
| T13 | 8:05.8 | a luz escurece (céu de chuva) enquanto a câmera desce para o Sul | whoosh médio baixo |
| T14 | 9:02.4 | corte seco no impacto para o 'arquivo' (sépia): a enchente de 1983 | impacto grave |
| T15 | 9:21.9 | corte seco de volta ao mapa colorido: a enchente de 2024 | impacto grave |
| T16 | 9:38.8 | zoom-out orbital até o globo inteiro, com o mar quente | whoosh longo |
| T17 | 9:59.9 | match cut: o globo vira o disco do calendário | impacto suave + whoosh |
| T18 | 10:52.3 | whip pan de volta ao Brasil | swish + whoosh curto |
| T19 | 11:04.2 | corte para o quadro de cortiça (o 3D sai de cena) | impacto grave |
| T20 | 11:40.5 | zoom-out: o quadro encolhe e revela o continente ao entardecer | whoosh longo |

| Tempo | Tipo | Quadro | Legenda na tela | Crédito na tela |
|---|---|---|---|---|
| 0:02.1–0:10.2 | imagem | pol (dir) | MANAUS · 09/10/2026 · VISTA DO ESPAÇO | IMAGEM: NASA MODIS TERRA (GIBS) · DOMÍNIO PÚBLICO |
| 0:24.2–0:28.0 | imagem | pol (esq) | PACÍFICO · TEMPERATURA DO MAR ACIMA DO NORMAL · 08/11/2026 | IMAGEM: NASA JPL (MUR, GIBS) · DOMÍNIO PÚBLICO |
| 2:15.1–2:22.2 | imagem | pol (dir) | CABO BLANCO (PERU) · PESCA ARTESANAL · OUT/2024 | FOTO: PRODUCE PERÚ · DOMÍNIO PÚBLICO |
| 3:12.3–3:15.9 | imagem | pol (dir) | NORTE DO PERU · CHUVAS DO EL NIÑO COSTEIRO · MAR/2023 | FOTO: MINISTERIO DE DEFENSA DEL PERÚ · CC BY 2.0 |
| 6:20.7–6:30.7 | imagem | pol (esq) | RIO BRANCO · BOA VISTA · 21/09/2025 | IMAGEM: NASA HLS · CONTÉM DADOS COPERNICUS SENTINEL MODIFICADOS [2025] |
| 6:21.7–6:30.7 | imagem | pol (dir) | RIO BRANCO · BOA VISTA · 16/09/2026 | IMAGEM: NASA HLS · CONTÉM DADOS COPERNICUS SENTINEL MODIFICADOS [2026] |
| 6:32.2–6:40.2 | imagem | pol (dir) | APUÍ (AM) · BRIGADISTAS · AGO/2020 | FOTO: BRUNO KELLY/AMAZÔNIA REAL · CC BY 2.0 |
| 6:44.8–6:49.0 | imagem | pol (dir) | MANAUS · A SECA DO RIO NEGRO · 2023 | FOTO: TIAGO DA MOTA E SILVA · CC BY-SA 4.0 |
| 7:15.6–7:29.3 | imagem | pol (esq) | SANTA QUITÉRIA (CE) · AÇUDE SECO · FEV/2016 (EL NIÑO 2015-16) | FOTO: PORTO NETO · CC BY-SA 4.0 |
| 8:10.4–8:16.3 | imagem | pol (dir) | MUÇUM (RS) · ENCHENTE DO TAQUARI · SET/2023 | FOTO: CADU GOMES/VPR · CC BY 2.0 |
| 8:27.0–8:34.2 | imagem | pol (dir) | SUL DO BRASIL · 04/11/2026 · TEMPESTADES | IMAGEM: NASA MODIS TERRA (GIBS) · DOMÍNIO PÚBLICO |
| 8:45.6–8:52.3 | imagem | pol (dir) | ASSISTA: 7 TORNADOS EM 6 DIAS | EM RELEVO · O VÍDEO ANTERIOR |
| 9:22.7–9:31.5 | imagem | pol (dir) | GRANDE PORTO ALEGRE · ENCHENTE · MAI/2024 | FOTO: RICARDO STUCKERT/PR · CC BY-SA 2.0 |
| 9:31.8–9:38.6 | imagem | pol (esq) | GRANDE PORTO ALEGRE · AEROPORTO ALAGADO · MAI/2024 | FOTO: RICARDO STUCKERT/PR · CC BY-SA 2.0 |
| 9:41.4–9:51.8 | imagem | pol (esq) | MAR QUENTE: CORAL BRANQUEADO · FLÓRIDA (EUA) · JUL/2023 | FOTO: NOAA · DOMÍNIO PÚBLICO |
| 11:17.4–11:40.9 | foto | polaroid no quadro de cortiça | RIO DO SUL (SC) · ENCHENTE · OUT/2023 | FOTO: PARZEUS · WIKIMEDIA COMMONS · CC BY-SA 4.0 |
| 11:22.1–11:40.9 | foto | polaroid no quadro de cortiça | BRASÍLIA · FUMAÇA · SET/2024 | FOTO: LEOPOLDO SILVA/AGÊNCIA SENADO · CC BY 2.0 |