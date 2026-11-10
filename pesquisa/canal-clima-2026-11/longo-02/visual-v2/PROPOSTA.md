# Em Relevo 002: visual v2, fase 1 (amostras), 10/11/2026

**Para ver:** `comparativo.jpg` (linhas: atual, A, B, C; colunas: Pacífico 1:10, Brasil 5:40, Manaus 0:11), `foto-grande.jpg` e `foto-grande-dupla.jpg`, `clipe-estilo-B.mp4` (18 s, 5:20–5:38: zoom-out do Pacífico para a América do Sul).

## Os 3 estilos (os três com relevo 3D real do NOAA ETOPO 2022, batimetria no mar e foco por vinheta)
| | Base | Cara | Bom para | Ponto fraco |
|---|---|---|---|---|
| **A · satélite real** | NASA Blue Marble + sombreado do ETOPO, mar azul por profundidade | HistóriAtenta: realista, "documentário" | zoom regional (rios e floresta de verdade), Pacífico | escuro na Amazônia; as tintas coloridas das UFs e os rótulos competem com a foto |
| **B · relevo editorial** ✅ | relevo sombreado gerado do ETOPO, nas cores do canal (papel → marrom), 28% da cor real (floresta/cerrado), mar navy com batimetria, rios | o nome do canal (Em Relevo) vira a identidade; limpo e bonito | todo o vídeo: as cores do canal (coral, navy, tintas) aparecem bem por cima | menos "uau" que o satélite no zoom de floresta |
| **C · pergaminho** | papel envelhecido com relevo suave, mar verde-azulado de tinta, costa em nanquim | GeoGlobe (modo antigo) | clima de "história" | parece mapa antigo, o que destoa de um canal de clima/dados de hoje |

**Recomendação: B.** É o que mais melhora sem brigar com o que você já aprovou: o coral, o navy, as tintas das UFs, os gráficos e as legendas foram pensados para fundo claro e quente, e no B continuam legíveis. O relevo do nome do canal passa a ser real. O A é a alternativa se você preferir o realismo do HistóriAtenta.

## Fotos maiores (vale para qualquer estilo)
Hoje a foto entra em polaroid de 560 px (29% da largura). No v2 ela ocupa **1240 px (65%)** em quadro 16:9 com Ken Burns lento, sobre o mapa escurecido. A legenda vai numa faixa coral e o crédito em 19 px, dentro da foto. Quando há duas fotos juntas (antes/depois de Boa Vista, 6:20), elas ficam lado a lado com 860 px cada. Celular e monitor mantêm o formato atual. O pino no mapa vira um anel pulsando.

## Tempo de render (medido: 1080p, swangle, concurrency 2, como no `shared/render.sh`; números em `tempos.txt`)
| Trecho | atual | A | B | C |
|---|---|---|---|---|
| Brasil inteiro (5:30) | 0,46 s/quadro | ~1,05* | 1,05 | ~1,10* |
| Pacífico (1:10) | 0,51 | ~0,58* | 0,58 | ~0,60* |

\*Na malha cheia, A, B e C mediram o mesmo tempo (2,39 / 2,40 / 2,52 s/quadro). A malha mais leve foi medida só no B, então os valores de A e C saem dessa proporção. A malha foi reduzida para 0,35 da original porque os vértices custam caro no SwiftShader e o relevo fino já vem sombreado na textura.

**Vídeo inteiro: ~9 h** em qualquer dos estilos (o render aprovado levou ~7 h), em partes de menos de 10 min com o mesmo `render.sh`. O acréscimo vem quase todo das cenas do Brasil (~54% do vídeo). O Pacífico, o globo e a cortiça quase não mudam.

## O que fica igual
Áudio, roteiro, timeline (`cues.json`), câmera, transições, SFX, gráficos, legendas, cortiça, CTA, pinos, nuvens, setas e relevo de calor. O `out/video.mp4` continua valendo até a aprovação.

## Como foi feito (em cópia; o render atual não é tocado)
- `shared/terreno_v2.js` (novo): planos deslocados pelo ETOPO, shader de foco, máscara das tintas drapeada no relevo, fronteiras e municípios em linhas drapeadas.
- `shared/cena3d_v2.js`: cópia do `cena3d.js` que, com `estilo`, esconde a mesa e a maquete de papel e põe o terreno no lugar. Sem `estilo`, fica idêntica.
- `remotion/src/LongoV2.jsx`: cópia do `Longo.jsx` com as props `estilo` (A/B/C), `fotos` ("grande") e o crédito do mapa. Composição `LongoV2` no `Root.jsx`; a `Longo` não mudou.
- `visual-v2/codigo/`: `baixa_bases.py`, `gera_texturas.py`, `still_v2.sh`, `mede_tempo.sh`, `comparativo.py`.

## Pendências para a fase 2 (depois da sua escolha)
- A textura do Pacífico termina em 45°N: em alguns enquadramentos aparece uma faixa escura no topo (ver `estilo-*-1.jpg`). Basta baixar até 65°N.
- A crista de papel dos Andes saiu (o relevo real substitui). O "acende Andes" (`cues.andes`) precisa virar brilho no terreno.
- Conferir no vídeo inteiro as cenas com placas sobre o mapa (municípios em coral, regiões translúcidas, régua de montanhas e diorama sobre a mesa, agora escura).
- Render completo (~9 h), QA e entrega no Drive.
