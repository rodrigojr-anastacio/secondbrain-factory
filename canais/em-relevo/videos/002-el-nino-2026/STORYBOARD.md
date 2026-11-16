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
## Visual v2, fase 2 (10/11/2026): mistura A/B aprovada pelo Rodrigo

Fonte única: `shared/estilo_v2.json` (lida por `remotion/src/LongoV2.jsx` → `shared/terreno_v2.js`). **A** = satélite (NASA Blue Marble + relevo ETOPO), **B** = relevo editorial (ETOPO nas cores do canal). Regra: A no "mundo real" (Pacífico/mundo, aberturas, zoom em natureza, impacto); B onde há dado, rótulo e número. Troca no corte de câmera ou em crossfade de textura de 1,6–1,8 s com a câmera parada; linhas, fundo, foco e crédito do mapa cruzam junto.

| # | Trecho | Estilo | Troca | Por quê |
|---|---|---|---|---|
| 1 | 0:00.0–0:30.2 | A | início | hook: fumaça sobre a Amazônia em Manaus, chuva em SC, costa do Peru com o relevo de calor (mundo real, impacto) |
| 2 | 0:30.2–1:02.2 | B | crossfade 1.6 s | a pergunta: rótulos FUMAÇA / ÁGUA DEMAIS / MAR QUENTE, fios e a barra das 4 perguntas (câmera parada 0:29.8-0:36.2) |
| 3 | 1:02.2–1:13.6 | A | no corte | abertura do cap. 1 (nuvem): o Pacífico inteiro |
| 4 | 1:13.6–2:07.6 | B | crossfade 1.6 s | explicação: diorama em corte, alísios, circulação de Walker, gangorra (câmera parada 1:02.2-1:15.3) |
| 5 | 2:07.6–3:16.0 | A | no corte | globo, arquivo dos pescadores do Peru, Pacífico real com a região Niño 3.4 |
| 6 | 3:16.0–3:45.5 | B | no corte | régua de montanhas (ONI): dado |
| 7 | 3:45.5–4:12.1 | A | no corte | Pacífico com o véu coral: o planeta inteiro mais quente (impacto) |
| 8 | 4:12.1–5:25.0 | B | no corte | régua RONI + slot do boletim (b19-b21) + prancha do que a ciência diz: dado, números |
| 9 | 5:25.0–5:44.6 | A | no corte | abertura do cap. 3: zoom-out orbital do Pacífico para a América do Sul, jato e ar que desce |
| 10 | 5:44.6–6:19.4 | B | crossfade 1.8 s | Brasil por região: UFs tingidas da previsão nov-jan (câmera parada 5:33.6-5:46.8) |
| 11 | 6:19.4–7:06.4 | A | no corte | Norte: Roraima e o rio Branco, focos no AM, rio Negro em Manaus (zoom em natureza) |
| 12 | 7:06.4–9:02.4 | B | no corte | Nordeste (seca grave por região), Centro-Oeste/Sudeste (tintas, rios), Sul (municípios em coral, pinos, tintas): dado |
| 13 | 9:02.4–9:60.0 | A | no corte | enchente de 1983 (arquivo), enchente de 2024 em Porto Alegre e o mundo com o mar quente (impacto, mundo) |
| 14 | 9:60.0–11:40.5 | B | no corte | cap. 4 até quando: probabilidades por trimestre, relevo de calor encolhendo, La Niña? (dado); cortiça cobre o 3D 11:04-11:40 |
| 15 | 11:40.5–12:09.9 | A | no corte | a resposta: o continente ao entardecer com os 3 pinos do hook (fecho, mundo real) |

Total: 8 trechos A (~4.8 min) e 7 trechos B (~7.3 min; inclui a cortiça 11:04–11:40, que cobre o 3D). Único intervalo abaixo de ~20 s: o A de 1:02–1:14 (abertura do cap. 1, 11 s), mantido porque o cap. abre no corte da nuvem e o diorama de explicação começa logo depois, com a câmera parada para o crossfade.

Outras mudanças do v2: todas as 15 mídias de foto/satélite em quadro grande (1240 px; 1150 px abaixo de número grande; duplas lado a lado com 860 px), crédito dentro da foto; textura do Pacífico estendida para 85°E–50°W × 45°S–65°N (sem faixa escura); "acende Andes" (0:23–0:37) como brilho coral na crista do relevo real (acima de ~2.300 m, a oeste de 63°W); barra das 4 perguntas em grade de 4 colunas iguais com gap de 34 px, texto quebrando dentro do card, ativo cresce 4% pelo centro e o "▶ AGORA" vira etiqueta acima do card.
