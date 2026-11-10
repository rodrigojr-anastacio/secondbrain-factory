# Satélite e dados: longo-02 (El Niño 2026)

Levantado em 09/11/2026. Custo zero. Scripts em `work/sat-scripts/` (fora do git: `work/` e `dl/` estão no `.gitignore`).
Licenças: NASA GIBS / MODIS / VIIRS / GOES / NOAA OISST / CPC = **domínio público** (governo dos EUA; sem logos, sem sugerir endosso). HLS Sentinel-2 (S30) = **dados Copernicus modificados**: exige o aviso "Contém dados Copernicus Sentinel modificados [2025]" / "[2026]". Monitor de Secas = ANA (dado público do governo brasileiro; citar a fonte).

## 1. Grade de anomalia do Pacífico (peça principal): `shared/sst_pacifico.json`
- **Fonte trocada (melhor que a sugerida):** NOAA **OISST v2.1** (NCEI), anomalia **diária** a 0,25° em relação a 1991-2020, lida em ASCII pelo OPeNDAP da NOAA PSL (`https://psl.noaa.gov/thredds/dodsC/Datasets/noaa.oisst.v2.highres/sst.day.anom.2026.nc.ascii?anom[t][lat][lon]`). É o mesmo produto-base que o CPC usa, com valores numéricos de verdade.
- **Por que não o GIBS MUR:** o colormap oficial (`colormaps/v1.3/GHRSST_Sea_Surface_Temperature_Anomalies.xml`, compartilhado pelas camadas MUR e MUR25; a URL `<LAYER>.xml` dá 404) **satura em +3,0 °C** (faixa `[3.0,+INF)`) e em −3,0. A Niño 1+2 está em +5,6 e o máximo da caixa passa de +7 °C, então o "relevo" sairia achatado no topo.
- Formato: `lon0=100, lat0=-30, passo=1, nx=191 (100°E…290°E = 70°W), ny=61 (−30…+30)`, linhas de lat −30 para +30, lon crescente, valores com 0,1, `null` = terra (< 50 % de oceano na célula). Cada célula é a média dos 16 pontos de 0,25° dentro de [x−0,5; x+0,5).
- **Datas (24):** semanais (quartas) de 2026-06-03 a 2026-11-04 + **2026-11-08** (último dia disponível, fora do passo). Cada grade é o **valor diário daquele dia** (não média semanal).
- Máximo da caixa: +4,7 (03/06) → +7,3 (30/09) → +8,0 °C (08/11), na costa do Peru/Equador.

### Validação (média ponderada por cos(lat))
| Região | 08/11 (0,25°) | 08/11 (grade 1°) | 04/11 (0,25°) | média diária 01–07/11 | CPC semanal 04NOV2026 (OISST) |
|---|---|---|---|---|---|
| Niño 3.4 (5°S–5°N, 170°W–120°W) | **+3,37** | +3,28 | +3,53 | +3,51 | +3,3 |
| Niño 1+2 (10°S–0, 90°W–80°W) | **+5,40** | +5,31 | +5,78 | +5,61 | +5,6 |
| Niño 3 | +4,25 | | +4,54 | +4,51 | +4,4 |
| Niño 4 | +1,59 | | +1,85 | +1,78 | +1,5 |
Dentro do esperado (Niño 3.4 +2,5 a +3,5; Niño 1+2 ~+5,6). A diferença de ~0,2 no 3.4 vem do CPC semanal usar o OISST semanal de 1°. Números brutos: `dl/dados/oisst/validacao.json`.

## 2. Globo: `remotion/public/sat/globo-anomalia.jpg` (2048×1024, 363 KB) e `shared/sst_global.json`
- Equirretangular lon −180..180, lat 90..−90, OISST **2026-11-08**, desenhado por nós: mar neutro `#C9D6D8` entre −0,5 e +0,5; +0,5 → coral `#E8505B` em +2,0 → vinho `#8E1F2F` em +4,0 (satura); −0,5 → azul `#3D6A9E` em −3,0. Terra `#DCCDB0` e contornos `#9C8662` (Natural Earth 110m `dados/ne110.json`). Gelo marinho/sem dado = mar neutro. PNG sem perda em `dl/sat/globo-anomalia.png`.
- `sst_global.json`: mesma lógica, 1°, `lon0=-179, lat0=-89, nx=360, ny=179` (lon −179…180, lat −89…89), uma data (2026-11-08).
- Crédito: **DADOS: NOAA OISST · ARTE: EM RELEVO**.

## 3. Imagens reais (originais em `dl/sat/`; polaroid JPG ≤ 1600 px e < 500 KB em `remotion/public/sat/`)
Todas via NASA GIBS WMS 1.3.0 EPSG:4326 (`work/sat-scripts/wms.py`).

| Arquivo em `remotion/public/sat/` | Original em `dl/sat/` | Camada | Data/hora UTC | Caixa (lon, lat) | Crédito sugerido |
|---|---|---|---|---|---|
| `manaus-fumaca-2026-10-09-terra.jpg` (**escolhida**) | `manaus/manaus-2026-10-09-MODIS_Terra-zoom.png` (2400×2100) | MODIS_Terra_CorrectedReflectance_TrueColor | 2026-10-09, passagem diurna (~14h UTC, mosaico diário) | −64..−56, −7..0 | NASA · MODIS TERRA (GIBS) |
| `manaus-fumaca-2026-10-09-snpp-larga.jpg` (**escolhida, larga**) | `manaus/manaus-2026-10-09-VIIRS_SNPP-larga.png` (2800×1960) | VIIRS_SNPP_CorrectedReflectance_TrueColor | 2026-10-09 (~17h UTC) | −70..−50, −12..2 | NASA/NOAA · VIIRS SUOMI NPP (GIBS) |
| `manaus-fumaca-2026-10-09-goes-1700z.jpg` | `manaus/manaus-2026-10-09T1700Z-GOES-East_GeoColor.png` (+ `-zoom.png`) | GOES-East_ABI_GeoColor | 2026-10-09 17:00 | −70..−50, −12..2 | NOAA/NASA · GOES-19 (GIBS) |
| `pacifico-anomalia-nasa-2026-11-08.jpg` | `sst-anom-nasa-mur25-pacifico-2026-11-08.png` (2200×1200; também `…-mur-…` 1 km) | GHRSST_L4_MUR25_Sea_Surface_Temperature_Anomalies | 2026-11-08 (diário) | −180..−70, −30..30 | NASA JPL · MUR SST (GIBS) |
| `boavista-rio-branco-2025-09-21.jpg` | `boavista/boavista-2025-09-21-HLS_S30.png` (1200×960) | HLS_S30_Nadir_BRDF_Adjusted_Reflectance (Sentinel-2) | 2025-09-21 | −60,80..−60,55, 2,72..2,92 | NASA HLS · CONTÉM DADOS COPERNICUS SENTINEL MODIFICADOS [2025] |
| `boavista-rio-branco-2026-09-16.jpg` | `boavista/boavista-2026-09-16-HLS_S30.png` | idem | 2026-09-16 | idem | NASA HLS · CONTÉM DADOS COPERNICUS SENTINEL MODIFICADOS [2026] |
| `sul-tempestade-2026-11-04-terra.jpg` | `sul/sul-2026-11-04-MODIS_Terra.png` (2400×1920) | MODIS_Terra_CorrectedReflectance_TrueColor | 2026-11-04 (~13h30 UTC) | −60..−45, −34..−22 | NASA · MODIS TERRA (GIBS) |
| `sul-tempestade-2026-11-04-goes-1700z.jpg` | `sul/sul-2026-11-04T1700Z-GOES-East_GeoColor.png` | GOES-East_ABI_GeoColor | 2026-11-04 17:00 | −60..−45, −34..−22 | NOAA/NASA · GOES-19 (GIBS) |

O que cada uma mostra (conferido no Read):
- **Manaus Terra:** véu de fumaça cinza-azulado cobrindo a metade sul, rios Negro/Solimões/Amazonas e Madeira visíveis por baixo; Manaus fica no encontro das águas (centro da imagem). Brilho de sol (sunglint) no Rio Negro e no lago de Balbina (mancha branca no alto): não é nuvem. A larga do VIIRS SNPP mostra a fumaça cobrindo do Madeira ao Purus, sem faixa sem dado. GOES GeoColor tem a fumaça mais fraca (melhor só para animação).
- **Pacífico NASA:** língua vinho (anomalia ≥ +3 °C, saturada) do centro do Pacífico até a costa do Peru/Equador; terra em preto. Sem legenda embutida (a paleta da NASA vai de roxo/azul = frio a vinho = ≥ +3 °C).
- **Boa Vista (set/2025 × set/2026):** 2025 com canal de água largo e contínuo; 2026 com rio estreito e grandes bancos de areia claros no leito. Em 2026 há poucas nuvens pequenas no canto NE (não cobrem o rio). Cenas de céu limpo alternativas: 2025-09-26 S30 e 2026-09-21 S30 (em `dl/sat/boavista/`). Resolução nativa 30 m.
- **Sul 04/11:** grande complexo de nuvens de tempestade sobre RS/SC/PR e Uruguai (Terra); GOES 17:00 UTC mostra o mesmo sistema à tarde.
- Outras candidatas brutas (MODIS Aqua, VIIRS NOAA-20/21) em `dl/sat/manaus/` e `dl/sat/sul/`; Aqua e Terra largas têm faixa preta entre órbitas; VIIRS NOAA-21 e SNPP do Sul em 04/11 vieram vazias.

## 4. CPC/NOAA (`dl/dados/`, baixados em 09/11/2026)
Arquivos: `oni.ascii.txt`, `RONI.ascii.txt`, `wksst9120.for`, `ensodisc.html` + `ensodisc.txt` (texto), `roni-strengths.html` + `.txt` + `roni-strengths-probs-2026-10.png` (gráfico oficial). (`ensodisc.shtml`, `nino-semanal-wksst9120.txt`, `sstoi-mensal-nino.txt` e `soi` já estavam lá, de outro processo.)
- **ONI ASO 2026 = +2,46** (JAS +2,16; JJA +1,80). **RONI ASO 2026 = +1,97** (JAS +1,69).
- Picos históricos do **ONI**: 1982-83 **+2,14** (DJF 1983; NDJ 1982 +2,12) · 1997-98 **+2,37** (NDJ) · 2015-16 **+2,59** (NDJ) · 2023-24 **+1,99** (NDJ). Atenção: o ONI da 2026 (+2,46) já passa 1982-83 e 1997-98 e fica abaixo só de 2015-16.
- Picos do **RONI**: 1982-83 **+2,40** (DJF 1983) · 1997-98 **+2,28** (NDJ) · 2015-16 **+2,25** (NDJ) · 2023-24 **+1,42** (OND).
- Semana de 04/11/2026 (OISST, `wksst9120.for`): **Niño 1+2 +5,6** (27,0 °C) · Niño 3 +4,4 · **Niño 3.4 +3,3** (30,1 °C) · Niño 4 +1,5.
- Boletim vigente = **8 de outubro de 2026** (o próximo sai em **12/11/2026**). Em outubro: Niño 3.4 +2,1, Niño 3 +3,0, Niño 1+2 +3,9 (médias mensais de setembro); "strong-to-very strong El Niño likely through JFM 2027 (> 83 %)".
- **Chance de evento histórico (RONI trimestral ≥ +2,5)**, texto do boletim: **SON 54 %, OND 83 %, NDJ 70 %**. A tabela de força não tem coluna ≥ 2,5 (só até "≥ 2,0").
- **Muito forte (RONI ≥ +2,0)**, tabela de out/2026: SON 100 %, OND 100 %, NDJ 96 %, DJF 81 %, JFM 46 %, FMA 6 %, MAM 0.
- **Neutro:** AMJ 2027 **54 %**, MJJ 2027 **70 %** (MAM 15 %, FMA 2 %).
- Crédito: **DADOS: NOAA CPC**.

## 5. Monitor de Secas (ANA): conseguiu
- Shapefiles oficiais do Brasil, públicos no S3 da ANA (achados no JS do site): `https://ana-monitor-secas-files.s3.sa-east-1.amazonaws.com/uploads/mapas/agosto2026.zip` e `setembro2026.zip` (+ mapas PNG oficiais `146_agosto2026.png`, `147_setembro2026.png`), salvos em `dl/dados/monitor-secas/`.
- Convertidos (leitor de shapefile em Python puro, Douglas-Peucker 0,02°, WGS84) para `dados/monitor-secas-2026-08.json` e `dados/monitor-secas-2026-09.json` (~85 KB cada). Uma Feature MultiPolygon por categoria, `properties = {categoria, valor, mes}`: `SI` (valor 0, área sem seca no mapa; o rótulo "si" vem do dbf, interpretação nossa), `S0` (1), `S1` (2), `S2` (3). **Não há S3 nem S4** em ago/set 2026. Desenhe na ordem SI → S0 → S1 → S2.
- Leitura: em setembro, o S2 cresce no interior do Nordeste (BA/PE/PI) e aparece um núcleo novo no Amazonas central; **Roraima (Boa Vista) tem S2 nos dois meses**; Centro-Sul quase todo sem seca.
- Crédito: **FONTE: MONITOR DE SECAS · ANA**.

## O que não funcionou
- `colormaps/v1.3/<LAYER>.xml` dá 404: o colormap certo é `GHRSST_Sea_Surface_Temperature_Anomalies.xml` (achado no WMTS GetCapabilities), e ele satura em ±3 °C. Por isso a grade veio do OISST/PSL.
- ERDDAP da NOAA: não tentado (timeout conhecido).
- VIIRS NOAA-21 e SNPP sem cobertura do Sul em 04/11/2026; MODIS Aqua/Terra na caixa larga de Manaus têm faixas sem dado entre órbitas.
