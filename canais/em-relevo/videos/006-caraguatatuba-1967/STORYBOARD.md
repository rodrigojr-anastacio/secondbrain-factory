# Storyboard: Em Relevo 006 (Caraguatatuba 1967 × São Sebastião 2023: por que a Serra do Mar desaba sobre o litoral)

Etapa 1 (17/11/2026). Fonte: `shared/storyboard.py` → `shared/storyboard.json`, `shared/cenas.json` e a tabela completa em `work/storyboard-tabela.md` (regenere com `python3 shared/storyboard.py`). Duração estimada **~9:55** (A 212 s · B 340 s · doc 43 s); 43 blocos; 7 mídias reais distintas (`pesquisa/FOTOS.md`); **zero imagem de IA**; custo de imagem US$ 0.

## Linguagem visual (a do 005, visual v2)
- **A = satélite** (SRTM do litoral norte via Terrain Tiles z12 + cor natural) para lugar e impacto; **B = relevo editorial** (navy) para dado e rótulo; **doc** = papel claro (carta de Olga Cruz; ficha do pluviômetro de 1967 desenhada em código).
- Ritmo 2–4 s por evento visual; cada mídia tem `gatilho` = palavra falada (o `build_cues.py` amarra ao Whisper). Câmera sempre em movimento; troca A↔B só no corte ou crossfade parado.
- Legenda só LUGAR · DATA; créditos só na descrição. Esquema fora de escala leva "ILUSTRATIVO" (exagero vertical, corte da casca, pontos de cicatriz, fratura do bloco).

## Assinatura e fio condutor
1. **O degrau** (b03, b05–b06, b09, b12, b20–b21, b35, b39 e a Thumb A): bloco 3D do relevo real **cortado de lado**, face do corte em terra, régua vertical 0 → 700 m e horizontal < 6 km. No hook, **dois blocos lado a lado** (Barra do Sahy × Morro do Cruzeiro) — perfis de `dados/perfis.json` (`shared/perfil_escarpa.py`).
2. **As 3 fichas da receita** (PAREDE · CHUVA · CASCA): acendem no b06 com os números, pulsam quando cada capítulo prova o seu ingrediente, voltam com os números de 2023 no b35 e formam a resposta no b38.

## Peças novas (prioridade; simplifique de baixo para cima se faltar tempo)
1. **Bloco 3D cortado** (degrau) com réguas — base de 8 blocos e da Thumb A. Simplificação: perfil 2D extrudado com textura de satélite.
2. **Colunas de pluviômetro** do CEMADEN no mapa (b01, b02, b13, b17, b19): componente de colunas do 004/005.
3. **Antes × depois Landsat** em cortina (b34) com estiramento comum (`004/tools/landsat_par.py`).
4. **Camada IMERG** (b15): `dados/nasa/litoral-2023-camada.png` sobre o relevo (mesmo mecanismo de máscara do `terreno_v2.js`).
5. **Corte da casca** (b20–b22): faixa marrom 1–2,5 m sobre rocha cinza, escorregamento em bloco; mostrador de coesão.
6. **Mapa de declividade da bacia** (b10, b27) calculado do SRTM (classes > 40%), e **carta do SGB** recortada (b32, b40).
7. Linha do tempo de 4 fases (b29), régua de largura do rio e de lama (b30), fichas e cards: componentes existentes.

## Mídias por bloco (resumo; detalhe em `shared/storyboard.json`)
| Bloco | Mídia | Legenda na tela |
|---|---|---|
| b02, b07, b36 | satelite/nasa-eo-landsat8-…-depois-2023-02-26.jpg | SÃO SEBASTIÃO · LANDSAT 8 · 26 FEV 2023 |
| b33, b34 | satelite/nasa-eo-landsat9-…-antes-2022-10-29.jpg + depois (cortina) | ANTES · 29 OUT 2022 / DEPOIS · 26 FEV 2023 |
| b05 | video/serra-do-mar-vista-da-tamoios-caraguatatuba.jpg | SERRA DO MAR · CARAGUATATUBA |
| b07, b23 | doc/cruz1975-fig7-carta-declividade-santo-antonio.png | CARTA DE DECLIVIDADES · OLGA CRUZ · 1975 |
| b25 | video/ubatuba-encosta-arrancada-estrada-2023-02-19.jpg | UBATUBA (SP) · 19 FEV 2023 |
| b32 | doc/sgb-carta-suscetibilidade-caraguatatuba.pdf (camada) | CARTA DE SUSCETIBILIDADE · SERVIÇO GEOLÓGICO DO BRASIL |
| b37 | video/sao-sebastiao-encosta-aereo-2023-02-23.jpg (fundo esmaecido) | SÃO SEBASTIÃO · 23 FEV 2023 |

## Sensibilidade
Sem foto de vítima, resgate com rosto ou TV; números de vítimas só em card sóbrio navy sem ícone (b31, b37); 1967 sem foto (não há licença livre). Nenhum "morte" em tela de título/capítulo.
