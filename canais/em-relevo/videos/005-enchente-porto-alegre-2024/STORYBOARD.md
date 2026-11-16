# Storyboard: Em Relevo 005 (enchente de maio/2024: por que a chuva da serra alagou Porto Alegre)

Etapa 1 (15/11/2026). Fonte: `shared/storyboard.py` → `shared/storyboard.json`, `shared/cenas.json` e a tabela completa em `work/storyboard-tabela.md` (regenere com `python3 shared/storyboard.py`). Duração estimada **~10:00–10:25** (A 290 s · B 300 s · arquivo 34 s); 15 fotos/satélites distintos; **zero imagem de IA**; custo de imagem US$ 0.

## Linguagem visual (mesma do longo-03/04, visual v2/LongoV3)
- **A = satélite** (Blue Marble + relevo ETOPO/SRTM) para lugar e impacto; **B = relevo editorial** para dado e rótulo; **arquivo** = papel sépia (1941 e o debate sobre a falha).
- Ritmo 2–4 s por evento visual; cada mídia tem `gatilho` = palavra falada onde entra (o `build_cues.py` da etapa 2 amarra ao Whisper).
- Legenda na tela só LUGAR · DATA (créditos só na descrição). Foto de outro ano sempre com o ano real (muro 2016, barra de Rio Grande 2023, Cais Mauá 2026, Arroio do Meio jun/2024 "depois da cheia").

## Assinatura e fio condutor
1. **Árvore de rios** (b05, b06, b14, b15, b19, b35, b38 e a thumb): hidrografia real da Região Hidrográfica do Guaíba (ANA/IBGE; base hidrográfica ottocodificada da ANA ou rios do IBGE 1:250 mil) em **ciano brilhante `#3FD8FF`** sobre relevo escuro; os 5 rios principais grossos (Jacuí, Taquari-Antas, Caí, Sinos, Gravataí), afluentes finos como textura; tudo converge num ponto brilhante em frente a Porto Alegre. O resto do RS escurece quando a bacia acende. **É a mesma imagem da thumb** (crivo r2: 5 rios grossos).
2. **A gota** (b01 → b02 → b06 → b11 → b13 → b22 → b33 → reprise b35–b36): partícula luminosa que nasce no pluviômetro de Caxias e é seguida pela câmera até o centro de Porto Alegre. Sem corte seco: a gota é a desculpa de cada movimento de câmera.

## Peças novas (em ordem de prioridade; se faltar tempo, simplifique de baixo para cima)
1. **Árvore de rios convergindo** (acima). Simplificação: só os 5 rios principais, sem afluentes.
2. **Régua do Guaíba** com marca fantasma de 1941 (b02, b24, b31): reaproveitar a régua do longo-04 (Iguaçu) com 5,35 M e 4,76 M; e a do Taquari em Lajeado (b12: 33,7 M × 29,92 M).
3. **Maquete do sistema de proteção** (b26–b31): orla de Porto Alegre em relevo editorial, muro da Mauá (cinza claro), diques (linha), 14 comportas (pontos amarelos), 23 casas de bombas (cubos que apagam: 19 de 23). Corte esquemático do sistema no b27. Simplificação: mapa 2D da cidade com ícones.
4. **Calendário de picos** (b18, b24): 2–6 de maio com o pico de cada rio pulsando e as ondas empilhando no Guaíba; e maio inteiro com os picos da Lagoa dos Patos (16 e 27/05). Simplificação: linha do tempo 2D.
5. **Perfil de relevo serra → capital** (b11): corte 3D de ~800 m até o nível do mar com exagero vertical.
6. **Frente fria parada + bloqueio** (b07): faixa de nuvens e cúpula translúcida, sem número (esquema).
7. Pluviômetros/colunas de chuva (b01, b04, b09) e contadores: componentes existentes.

## Mapa de mídias por bloco (resumo; detalhe em `shared/storyboard.json`)
| Bloco | Mídia | Legenda na tela |
|---|---|---|
| b02 | satelite/nasa-landsat8-porto-alegre-alagado-2024-05-08.jpg (2 s antes do 3D) | PORTO ALEGRE · LANDSAT 8 · 8 MAI 2024 |
| b03 | centro-historico-rodoviaria-cais-mauah-alagados-aereo-2024-05-05.jpg | CENTRO HISTÓRICO · PORTO ALEGRE · 5 MAI 2024 |
| b03 | rodoviaria-viaduto-cais-maua-alagados-aereo-2024-05-05.jpg | RODOVIÁRIA · PORTO ALEGRE · 5 MAI 2024 |
| b03 | aeroporto-salgado-filho-pista-alagada-aereo-2024-05-05.jpg | AEROPORTO SALGADO FILHO · 5 MAI 2024 |
| b12 | arroio-do-meio-navegantes-destruicao-aereo-2024-06-06.jpg | ARROIO DO MEIO · VALE DO TAQUARI · JUN 2024 |
| b16 | satelite/hls-sentinel2-porto-alegre-guaiba-antes-2024-04-01.jpg | GUAÍBA · SENTINEL-2 · 1 ABR 2024 |
| b20 | satelite/nasa-modis-sul-do-rs-durante-2024-05-06.jpg | LAGOA DOS PATOS · MODIS · 6 MAI 2024 |
| b21 | rio-grande-fragata-f44-canal-da-barra-molhes-2023-08-15.jpg | CANAL DA BARRA · RIO GRANDE · 2023 |
| b24 | pelotas-bairros-alagados-aereo-2024-05-18.jpg | PELOTAS · 18 MAI 2024 |
| b25 | mercado-publico-fachada-alagado-enchente-1941-05.jpg (800 px, formato carte, sem zoom) | MERCADO PÚBLICO · MAIO DE 1941 |
| b26 | muro-da-maua-grafite-dia-normal-2016-04-23.jpg | MURO DA MAUÁ · DIA NORMAL · 2016 |
| b27 | comporta-cais-maua-fechamento-2024-05-02.jpg | COMPORTA DO CAIS MAUÁ · 2 MAI 2024 |
| b33 | mercado-publico-ilhado-aereo-2024-05-05.jpg | MERCADO PÚBLICO · 5 MAI 2024 |
| b33 | centro-historico-edificios-historicos-alagados-aereo-2024-05-05.jpg | CENTRO HISTÓRICO · 5 MAI 2024 |
| b39 | cais-maua-galpao-marcas-da-enchente-2026-03-12.jpg | CAIS MAUÁ · MARCAS DA ENCHENTE · 2026 |

Reservas (em `dl/fotos/video/`, licenças em `pesquisa/FOTOS.md`): viaduto/panorâmica/ruas do centro 05/05, Cais Mauá 02/05, aeroporto + Canoas 05/05, ponte/freeway e rodovias 05/05 (Stuckert), Mercado 1941 (aérea), Gasômetro 2023, Ponte de Pedra 2025, fachada com marca d'água; satélites HLS 06/05 e 08/05, MODIS 20/04, FwDET 06/05, Copernicus 06/05. Um antes × depois real cabe no b16/b19 (HLS 01/04 × 06/05, mesma janela) se sobrar tempo.

## Licenças (atenção da etapa 2)
- **Série da Prefeitura de Porto Alegre (PMPA) no Commons:** licença "Attribution" (não CC). Uso com crédito "Fotógrafo/PMPA" na descrição; registrar em `FONTES-E-LICENCAS.md`. Se o Rodrigo preferir zero risco, troque por Stuckert (CC BY-SA 2.0) e satélite.
- Fotos de 1941: domínio público com aviso, 800 px e marca d'água de site: usar pequena (carte) e recortar a marca; se a marca não sair, tirar do vídeo e fazer o 1941 só com tipografia + régua.
- Satélite: NASA (domínio público, "NASA Earth Observatory"/"NASA Worldview"), HLS/Sentinel-2 ("Contains modified Copernicus Sentinel data 2024").

## Sensibilidade
- Nenhuma foto de vítima, de resgate com rosto ou de TV. Todas as fotos são aéreas de cidade/infraestrutura; Arroio do Meio sem pessoas visíveis.
- O número de mortes aparece uma vez (b03), em card navy sóbrio com fonte e data do balanço; nunca na thumb, título, descrição ou tags.
- b31 deixa claro que a água **não** passou por cima do muro (atribuído aos relatos técnicos); b32 mostra as três explicações sem tomar partido.
- b38: selo "NÃO É PREVISÃO".
