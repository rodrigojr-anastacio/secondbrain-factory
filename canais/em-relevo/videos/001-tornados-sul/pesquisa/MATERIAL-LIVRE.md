# Material livre para o longo 01 (tornados no Sul, 2–7/11/2026)
Coletado em 08/11/2026, custo zero. Arquivos brutos em `dl/` (fora do git). Legenda: livre = pode usar com o crédito indicado; ⚠ = atenção (ver nota).

## 1. Satélite (NASA GIBS WMS, domínio público NOAA/NASA)
Serviço: `https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi` (WMS 1.3.0, EPSG:4326, PNG). Licença: domínio público (governo dos EUA; GOES = NOAA/NASA, MODIS = NASA, MUR = NASA JPL). Crédito sugerido: "IMAGEM: GOES-19 · NOAA/NASA (GIBS)" ou "NASA GIBS / MODIS Terra". Sem logos, sem sugerir endosso.
Caixa **sul** = lon −66 a −42, lat −38 a −18 (1920×1440). Caixa **larga** = lon −80 a −35, lat −40 a −5 (2400×1867, mostra Amazônia/Andes).
Horários: Maringá 02/11 06:00 UTC e Santo Augusto 07/11 06:00 UTC são **estimados** (não confirmei a hora real; ajustar com a hora oficial se for citar). Chapecó 04/11 13:20 UTC = 10h20 BRT.

| Arquivo (`dl/sat/`) | O que é | Camada GIBS | Data/hora (UTC) |
|---|---|---|---|
| `maringa-Band13_Clean_Infrared-sul.png` | Maringa · IR limpo (Band 13) · caixa sul | GOES-East_ABI_Band13_Clean_Infrared | 2026-11-02 06:00 |
| `maringa-Band13_Clean_Infrared-larga.png` | Maringa · IR limpo (Band 13) · caixa larga | GOES-East_ABI_Band13_Clean_Infrared | 2026-11-02 06:00 |
| `maringa-GeoColor-sul.png` | Maringa · GeoColor · caixa sul | GOES-East_ABI_GeoColor | 2026-11-02 06:00 |
| `maringa-GeoColor-larga.png` | Maringa · GeoColor · caixa larga | GOES-East_ABI_GeoColor | 2026-11-02 06:00 |
| `chapeco-Band13_Clean_Infrared-sul.png` | Chapeco · IR limpo (Band 13) · caixa sul | GOES-East_ABI_Band13_Clean_Infrared | 2026-11-04 13:20 |
| `chapeco-Band13_Clean_Infrared-larga.png` | Chapeco · IR limpo (Band 13) · caixa larga | GOES-East_ABI_Band13_Clean_Infrared | 2026-11-04 13:20 |
| `chapeco-GeoColor-sul.png` | Chapeco · GeoColor · caixa sul | GOES-East_ABI_GeoColor | 2026-11-04 13:20 |
| `chapeco-GeoColor-larga.png` | Chapeco · GeoColor · caixa larga | GOES-East_ABI_GeoColor | 2026-11-04 13:20 |
| `santoaugusto-Band13_Clean_Infrared-sul.png` | Santoaugusto · IR limpo (Band 13) · caixa sul | GOES-East_ABI_Band13_Clean_Infrared | 2026-11-07 06:00 |
| `santoaugusto-Band13_Clean_Infrared-larga.png` | Santoaugusto · IR limpo (Band 13) · caixa larga | GOES-East_ABI_Band13_Clean_Infrared | 2026-11-07 06:00 |
| `santoaugusto-GeoColor-sul.png` | Santoaugusto · GeoColor · caixa sul | GOES-East_ABI_GeoColor | 2026-11-07 06:00 |
| `santoaugusto-GeoColor-larga.png` | Santoaugusto · GeoColor · caixa larga | GOES-East_ABI_GeoColor | 2026-11-07 06:00 |
| `seq04/01.png` … `seq04/13.png` | Sequência IR de 04/11, 13 quadros a cada 30 min, 10:00 a 16:00 UTC (07h a 13h BRT), caixa sul, 1920×1440, para animar a tempestade crescendo | GOES-East_ABI_Band13_Clean_Infrared | 2026-11-04 10:00 … 16:00 |
| `chapeco-AirMass-larga.png`, `chapeco-AirMass-sul.png` | Air Mass (RGB de massa de ar: umidade/vapor, o "rio" vindo da Amazônia aparece em verde/azul-claro) | GOES-East_ABI_Air_Mass | 2026-11-04 13:20 |
| `xanxere-2015-04-20-terra-truecolor.png` (1920×1920, lon −60 a −40, lat −35 a −15), `xanxere-2015-04-20-terra-zoom.png` (2000×1600, lon −56 a −46, lat −32 a −24), `xanxere-2015-04-20-aqua-truecolor.png` | Xanxerê, 20/04/2015: MODIS true color diário (GOES-13 não existe no GIBS). Mostra o sistema de nuvens sobre o Sul no dia do tornado (passagem diurna, ~13h30 local; o tornado foi ~15h30 local, então é o dia, não o instante) | MODIS_Terra/Aqua_CorrectedReflectance_TrueColor | 2015-04-20 |
| `sst-anom-pacifico-americas-2026-11-05.png` (3000×1333, lon −180 a −30, lat −40 a 40); também `…-2026-11-01.png`, `…-2026-10-15.png` e `sst-anom-pacifico-eq-2026-11-05.png` (2200×1200, lon −170 a −60, lat −30 a 30) | Anomalia de temperatura do mar (El Niño): faixa vermelho-escuro no Pacífico equatorial até a costa do Peru/Equador. Land em preto, escala saturada (sem legenda embutida: a legenda da camada MUR25 vai de azul = frio a vinho = muito quente, anomalia ≥ ~+4 °C) | GHRSST_L4_MUR25_Sea_Surface_Temperature_Anomalies (NASA JPL) | 2026-11-05 / 11-01 / 10-15 |

Obs.: GIBS não tem camada de umidade específica (Band 8/9/10) em estoque na versão consultada; usei **Air Mass**. Para gráfico de vapor puro, daria para tentar `GOES-East_ABI_Band13` com paleta diferente ou outra fonte (NOAA STAR, não testada).

## 2. Dados do El Niño (NOAA CPC, domínio público) em `dl/dados/`
| Arquivo | O que é | URL |
|---|---|---|
| `oni.ascii.txt` | ONI trimestral (SEAS, ano, total, anomalia), 1950 até ASO 2026 = **+2,46** (JAS +2,16, JJA +1,80) | https://www.cpc.ncep.noaa.gov/data/indices/oni.ascii.txt |
| `sstoi-mensal-nino.txt` | Mensal Niño 1+2, 3, 4 e 3.4 (SST e anomalia), 1982–out/2026. Niño 3.4 out/2026: **+3,25 °C** (set +2,84, ago +2,52, jul +2,03) | https://www.cpc.ncep.noaa.gov/data/indices/sstoi.indices |
| `nino-semanal-wksst9120.txt` | Semanal Niño 1+2/3/3.4/4 desde 02/09/1981 até 28/10/2026 (Niño 3.4 semana de 28/10: SST 30,2, anomalia **+3,4**) | https://www.cpc.ncep.noaa.gov/data/indices/wksst9120.for |
| `soi` | Índice de Oscilação Sul (SOI) mensal | https://www.cpc.ncep.noaa.gov/data/indices/soi |
| `ensodisc.shtml` | Texto do boletim ENSO do CPC (HTML bruto): "strong-to-very strong El Niño likely through Jan–Mar 2027 (>83%)"; 83% de chance de superar +2,5 °C no trimestre OND | https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso_advisory/ensodisc.shtml |

Nota: o texto do boletim cita Niño-3.4 de +2,1 °C no mês anterior (índice relativo/RONI); as tabelas acima usam o índice tradicional (OISST). Ao citar números, dizer qual índice.

## 3. Fotos (Wikimedia Commons, licença conferida pelos metadados de cada página de arquivo)
Pasta `dl/fotos/` (máx. 1920 px de largura). Crédito mínimo: **autor + "Wikimedia Commons" + licença** (CC BY/BY-SA exigem; domínio público/CC0 não, mas é bom creditar).
Não achei no Commons: fotos de Guaraciaba 2009 e dos tornados do Sul 2023–2026 (Encantado/Muçum tem só **enchente** 2023, não tornado). Tornados do Sul de 2026 ficam sem foto livre: usar satélite e os trechos com autorização.

| Arquivo | O que é | Página no Commons | Autor | Licença | Nota |
|---|---|---|---|---|---|
| `br-xanxere-2015-tornado-rbs.jpg` | 2015-Xanxere-tornado (1366×768 orig.) | https://commons.wikimedia.org/wiki/File:2015-Xanxere-tornado.jpg | Reproduction/RBS TV | CC BY 4.0 | ⚠ Fonte é reprodução de TV (RBS/Globo, g1) marcada CC BY 4.0 no Commons: licença contestável e risco de Content ID. Evitar em tela cheia ou não usar. |
| `br-palmas-pr-1959-destruicao-tornado.jpg` | Pile of destruction Palmas 1959 (960×720 orig.) | https://commons.wikimedia.org/wiki/File:Pile_of_destruction_Palmas_1959.jpg | Reproduction/TV Globo | CC BY 4.0 | ⚠ Reprodução de TV Globo marcada CC BY 4.0: mesmo risco. |
| `br-marechal-candido-rondon-2015-tornado.jpg` | Tornado Marechal Cândido Rondon (750×458 orig.) | https://commons.wikimedia.org/wiki/File:Tornado_Marechal_C%C3%A2ndido_Rondon.jpg | Reproduction/TV Globo | CC BY 4.0 | ⚠ Reprodução de TV Globo marcada CC BY 4.0: mesmo risco. |
| `br-marechal-candido-rondon-2015-demonstracao.png` | Demonstração - Tornado em Marechal Cândido Rondon 2015 (1920×1080 orig.) | https://commons.wikimedia.org/wiki/File:Demonstra%C3%A7%C3%A3o_-_Tornado_em_Marechal_C%C3%A2ndido_Rondon_2015.png | A.O Mapping | CC BY 3.0 |  |
| `br-rio-das-pedras-sp-2025-tornado.jpg` | Tornado Rio das Pedras 2025 01 (4080×3072 orig.) | https://commons.wikimedia.org/wiki/File:Tornado_Rio_das_Pedras_2025_01.jpg | A.O Mapping | CC BY 4.0 |  |
| `br-piracicaba-2025-mesociclone.jpg` | Mesocyclone Piracicaba 28-01-2025 (4096×2304 orig.) | https://commons.wikimedia.org/wiki/File:Mesocyclone_Piracicaba_28-01-2025.jpg | A.O Mapping | CC BY 4.0 |  |
| `br-piracicaba-2026-supercelula.jpg` | Supercell Piracicaba 2026-01-03 10 (4080×3072 orig.) | https://commons.wikimedia.org/wiki/File:Supercell_Piracicaba_2026-01-03_10.jpg | A.O Mapping | CC BY 4.0 |  |
| `br-piracicaba-2026-supercelula-panoramica.jpg` | Supercell Piracicaba 2026-01-03 3 (4080×2296 orig.) | https://commons.wikimedia.org/wiki/File:Supercell_Piracicaba_2026-01-03_3.jpg | A.O Mapping | CC BY 4.0 |  |
| `br-mucum-rs-2023-area-destruida-enchente.jpg` | 10-09-2023 Visita a área destruída pelas enchentes na cidade de Muçum no Rio Grande do Sul. Foto Cadu Gomes VPR (53177977025) (8256×5504 orig.) | https://commons.wikimedia.org/wiki/File:10-09-2023_Visita_a_%C3%A1rea_destru%C3%ADda_pelas_enchentes_na_cidade_de_Mu%C3%A7um_no_Rio_Grande_do_Sul._Foto_Cadu_Gomes_VPR_(53177977025).jpg | Vice-Presidência da República | CC BY 2.0 | Enchente de set/2023, não tornado. Governo federal (Vice-Presidência), CC BY 2.0. |
| `br-mucum-rs-ribeirinhos-enchente-01.jpg` | Ribeirinhos afetados pelas enchentes na região de Muçum 01 (1600×900 orig.) | https://commons.wikimedia.org/wiki/File:Ribeirinhos_afetados_pelas_enchentes_na_regi%C3%A3o_de_Mu%C3%A7um_01.jpg | Mneoqeav | CC BY-SA 4.0 | Enchente, não tornado. CC BY-SA: obra derivada herda a licença (usar sem modificar ou creditar bem). |
| `br-ciclone-extratropical-rs-2023-07-13-satelite-cira.png` | Ciclone extratropical RS 13 jul 2023 (1060×615 orig.) | https://commons.wikimedia.org/wiki/File:Ciclone_extratropical_RS_13_jul_2023.png | CIRA -NOAA | CC0 | Satélite CIRA/NOAA, não é tornado (ciclone de julho/2023). |
| `br-ciclone-bomba-rs-2023-08-18-satelite-cira.png` | Ciclone-bomba RS 18 ago 2023 18h (768×554 orig.) | https://commons.wikimedia.org/wiki/File:Ciclone-bomba_RS_18_ago_2023_18h.png | CIRA - NOAA | Public domain | Satélite CIRA/NOAA (ciclone bomba ago/2023). |
| `br-pelotas-2023-ciclone-estragos-cidade.jpg` | 13.07.2023 - Estrados causados pelo Ciclone extratropical na cidade - Foto Michel Corvello (53045762487) (6240×4160 orig.) | https://commons.wikimedia.org/wiki/File:13.07.2023_-_Estrados_causados_pelo_Ciclone_extratropical_na_cidade_-_Foto_Michel_Corvello_(53045762487).jpg | Prefeitura de Pelotas | Public domain | Estragos do ciclone de jul/2023 em Pelotas (não tornado). |
| `ar-tornado-argentina-ilustrativo.png` | Tornado en Argentina (1915×881 orig.) | https://commons.wikimedia.org/wiki/File:Tornado_en_Argentina.png | Nardonardo305 | CC BY-SA 4.0 | CC BY-SA; imagem ilustrativa, conferir o conteúdo antes de usar. |
| `ar-mesociclone-circulacion-mesoescala.jpg` | Circulación a Mesoescala (3264×2448 orig.) | https://commons.wikimedia.org/wiki/File:Circulaci%C3%B3n_a_Mesoescala.jpg | Supercellofphoto | CC0 | Local exato não conferido (autor argentino de supercélulas). |
| `us-supercelula-chaparral-nws.jpg` | Chaparral Supercell 2 (2560×1920 orig.) | https://commons.wikimedia.org/wiki/File:Chaparral_Supercell_2.JPG | Greg Lundeen (NWS El Paso staff member at the time) | Public domain |  |
| `us-supercelula-corrente-ascendente-sino.jpg` | Supercell with bell-bottom updraft (6960×4640 orig.) | https://commons.wikimedia.org/wiki/File:Supercell_with_bell-bottom_updraft.jpg | Rollingskyphoto | CC BY 4.0 |  |
| `us-mesociclone-ocluso-tornado-noaa.jpg` | Occluded mesocyclone tornado5 - NOAA (1816×1200 orig.) | https://commons.wikimedia.org/wiki/File:Occluded_mesocyclone_tornado5_-_NOAA.jpg | OAR/ERL/National Severe Storms Laboratory (NSSL) | Public domain |  |
| `us-wall-cloud-raios-noaa.jpg` | Wall cloud with lightning - NOAA (1840×1196 orig.) | https://commons.wikimedia.org/wiki/File:Wall_cloud_with_lightning_-_NOAA.jpg | Brad Smull, NOAA Photo Library, NOAA Central Library; OAR/ERL/National Severe Storms Laboratory (NSS | Public domain |  |
| `us-wall-cloud-tail-cloud.jpg` | Wallcloudwithtailcloud (1788×1188 orig.) | https://commons.wikimedia.org/wiki/File:Wallcloudwithtailcloud.jpg | — | Public domain |  |
| `us-tornado-vortex2-nssl0238.jpg` | Nssl0238 - Flickr - NOAA Photo Library (3072×2304 orig.) | https://commons.wikimedia.org/wiki/File:Nssl0238_-_Flickr_-_NOAA_Photo_Library.jpg | John Oakland, CIMSS. Credit: VORTEX II. | Public domain |  |
| `us-tornado-torus-nssl.jpg` | TORUS tornado (2048×1367 orig.) | https://commons.wikimedia.org/wiki/File:TORUS_tornado.jpg | Morgan Schneider | Public domain |  |
| `us-el-reno-2013-tornado-cunha.jpg` | El Reno EF-5 Tornado Wedge (5103×3402 orig.) | https://commons.wikimedia.org/wiki/File:El_Reno_EF-5_Tornado_Wedge.jpg | Daniel Rodriguez | CC BY 2.0 |  |
| `us-moore-2013-tornado.jpg` | May 20, 2013 Moore, Oklahoma tornado (3264×2448 orig.) | https://commons.wikimedia.org/wiki/File:May_20,_2013_Moore,_Oklahoma_tornado.JPG | Ks0stm | CC BY-SA 3.0 | CC BY-SA 3.0. |
| `us-funil-tornado-contraluz-noaa.jpg` | Backlit funnel cloud and tornado - NOAA (1828×1220 orig.) | https://commons.wikimedia.org/wiki/File:Backlit_funnel_cloud_and_tornado_-_NOAA.jpg | — | Public domain |  |
| `us-nuvem-funil-descendo-noaa.jpg` | Funnel cloud approaching the ground - NOAA (1836×1168 orig.) | https://commons.wikimedia.org/wiki/File:Funnel_cloud_approaching_the_ground_-_NOAA.jpg | — | Public domain |  |
| `us-moore-2013-radar-ktlx.png` | 2013 Moore tornado radar KTLX 2013-05-20 2021Z (1076×667 orig.) | https://commons.wikimedia.org/wiki/File:2013_Moore_tornado_radar_KTLX_2013-05-20_2021Z.png | National Weather Service (NWS), Federal Aviation Administration (FAA), and United States Air Force ( | Public domain |  |
| `us-moore-2013-dano-ef5-nws.jpg` | NWS 2013 Moore EF5 damage (1280×960 orig.) | https://commons.wikimedia.org/wiki/File:NWS_2013_Moore_EF5_damage.jpg | NWS WFO Norman, OK | Public domain |  |
| `us-dano-ef5-casa-skaggs-rd-noaa.jpg` | EF5 damage to a home along Skaggs Rd (1000×747 orig.) | https://commons.wikimedia.org/wiki/File:EF5_damage_to_a_home_along_Skaggs_Rd.jpg | National Oceanic and Atmospheric Administration | Public domain |  |
| `us-dano-ef5-exemplo-nws.jpg` | EF5 tornado damage example (1220×915 orig.) | https://commons.wikimedia.org/wiki/File:EF5_tornado_damage_example.jpg | National Weather Service, Parkersburg Storm Damage Survey | Public domain |  |
| `us-joplin-2011-dano-usace.jpg` | Joplin tornado damage (5881818947) (3504×2336 orig.) | https://commons.wikimedia.org/wiki/File:Joplin_tornado_damage_(5881818947).jpg | Kansas City District U.S. Army Corps of Engineers | Public domain |  |
| `us-joplin-2011-dano-nws.jpg` | 22 May 2011 Joplin tornado damage (1024×768 orig.) | https://commons.wikimedia.org/wiki/File:22_May_2011_Joplin_tornado_damage.jpg | National Weather Service in Springfield, Missouri | Public domain |  |
| `us-el-reno-2013-carro-samaras-nws.jpg` | 2013 El Reno tornado Samaras Car (1280×960 orig.) | https://commons.wikimedia.org/wiki/File:2013_El_Reno_tornado_Samaras_Car.jpg | National Weather Service Office in Norman, Oklahoma | Public domain |  |
| `us-moore-2013-trilhas-satelite-nesdis.png` | Tornado Tracks Streak Across Oklahoma (NESDIS 2013-05-21) (1920×1080 orig.) | https://commons.wikimedia.org/wiki/File:Tornado_Tracks_Streak_Across_Oklahoma_(NESDIS_2013-05-21).png | NOAA | Public domain |  |

Fotos de domínio público (NOAA/NSSL/NWS/USACE) cobrem: supercélula, mesociclone, wall cloud, nuvem-funil, tornado, dano EF5 (Moore 2013, Skaggs Rd, exemplo NWS), Joplin 2011, El Reno 2013. Não há foto de tornado em ação de Joplin 2011 em domínio público neste lote (só danos).
Vídeo CC (não baixado): `File:Xanxerê tornado 2015 CCTV Footage.webm` (domínio público, CCTV, 426×240) em https://commons.wikimedia.org/wiki/File:Xanxer%C3%AA_tornado_2015_CCTV_Footage.webm.

## 4. Música de fundo (`dl/musica/`)
Pixabay Music: **bloqueado** (Cloudflare 403 para download automatizado). Free Music Archive não tentada (não precisou). Fonte usada: Kevin MacLeod / incompetech, **CC BY 4.0**, sem Content ID (ele distribui com atribuição). URL de cada faixa: `https://incompetech.com/music/royalty-free/mp3-royaltyfree/<título com %20>.mp3`; catálogo: https://incompetech.com/music/royalty-free/music.html.
**Texto de crédito (colar na descrição, uma linha por faixa usada):**
`"<Título>" Kevin MacLeod (incompetech.com)` / `Licensed under Creative Commons: By Attribution 4.0 License` / `http://creativecommons.org/licenses/by/4.0/`

| Arquivo | Faixa | Duração | Uso sugerido |
|---|---|---|---|
| `Echoes_of_Time.mp3` | Echoes of Time | 4:45 | abertura/contexto, documental sóbrio |
| `Ossuary_6_Air.mp3` | Ossuary 6 - Air | 4:10 | bloco explicativo (meteorologia), atmosférico e contido |
| `Gathering_Darkness.mp3` | Gathering Darkness | 4:25 | tensão crescente (a tempestade se forma) |
| `Hidden_Past.mp3` | Hidden Past | 3:12 | transições e reflexão |
| `Dark_Fog.mp3` | Dark Fog | 4:00 | tensão leve, tom de mistério |
| `Frozen_Star.mp3` | Frozen Star | 3:41 | fecho / El Niño, mais aberto |
| `Unseen_Horrors.mp3` | Unseen Horrors | 4:11 | trecho dos estragos (cuidado: mais sombria) |
| `Ossuary_5_Rest.mp3` | Ossuary 5 - Rest | 3:56 | bloco calmo / fecho |

Cobertura: 3 faixas (Echoes of Time + Ossuary 6 + Gathering Darkness) somam ~13:20, e as 8 somam ~32 min. Não ouvi as faixas (só conferi duração): validar o clima antes de travar a trilha.

## 5. SFX (`dl/sfx/`, WAV 48 kHz mono)
Pixabay, BigSoundBank e Zapsplat bloquearam download automatizado (403); Freesound exige login; Kenney (CC0) não expõe o link do zip. **Soluções:** (a) Wikimedia Commons (CC0/PD/CC BY) para o que é gravação real; (b) o resto **sintetizado por nós** (numpy, script `/tmp` não versionado; sem licença de terceiros, uso livre).

**Gravações reais (Wikimedia Commons)**
| Arquivo | O que é | URL | Autor | Licença | Crédito |
|---|---|---|---|---|---|
| `ambiente-vento-tempestade-killiney-60s.wav` | Vento/tempestade (Storm Floris), 60 s | https://commons.wikimedia.org/wiki/File:Killiney_Hill_Storm_Floris_20250804_1537.ogg | Karlunun | CC0 | não exige |
| `ambiente-tempestade-quebec-60s.wav` | Ambiente de tempestade (trecho 2:00–3:00 de 26 min) | https://commons.wikimedia.org/wiki/File:Storm_in_Quebec_on_August_10,_2023.flac | Wilfredor | CC0 | não exige |
| `trovao-nosferatu-25s.wav` | Trovão (clap), 25 s | https://commons.wikimedia.org/wiki/File:Nosferatu_thunderclap_-_Richard_Humphries.wav | Richard Humphries | CC BY 4.0 | "Richard Humphries, Wikimedia Commons, CC BY 4.0" |
| `trovao-tempestade-rhumphries-40s.wav` | Tempestade com trovões (trecho 0:20–1:00) | https://commons.wikimedia.org/wiki/File:Rhumphries_-_rbh-thunder-storm.ogg | RHumphries | **CC BY 3.0** | "RHumphries, Wikimedia Commons, CC BY 3.0" |
| `datilografia-maquina-wws-26s.wav` | Máquina de escrever (sequência e batidas isoladas), 26 s; cortar uma batida com ffmpeg | https://commons.wikimedia.org/wiki/File:WWS_Typewriter.ogg | Work With Sounds / Konrad Gutkowski | CC BY 4.0 | "Work With Sounds / Konrad Gutkowski, Wikimedia Commons, CC BY 4.0" |
| `toc-madeira-real-stephan.wav` | Batida na madeira/porta, 6 s (várias batidas) | https://commons.wikimedia.org/wiki/File:Knocking_on_wood_or_door.ogg | stephan | domínio público | não exige |
| `papel-paginas-stephan-20s.wav` | Folhear papel/páginas, 20 s dos 78 s | https://commons.wikimedia.org/wiki/File:Book_paper_pages_assorted.ogg | stephan | domínio público | não exige |

**Sintetizados por nós (sem terceiros)**
| Pedido | Arquivos |
|---|---|
| "toc" seco de madeira, 3 variações | `toc-madeira-1.wav`, `-2`, `-3` (0,25 s) |
| Número carregando, suave, 2 variações | `tique-suave-1.wav`, `tique-suave-2.wav` (clique levíssimo, 0,08 s) e `tum-abafado-1.wav`, `tum-abafado-2.wav` (grave abafado) |
| Whoosh de câmera | `whoosh-curto-1.wav` (0,45 s), `whoosh-curto-2.wav` (0,6 s), `whoosh-medio.wav` (1,1 s), `whoosh-longo.wav` (2,2 s) |
| Swish de chicote (whip pan) | `swish-whip-pan.wav` (0,28 s) |
| Impacto suave (boom grave abafado) | `impacto-boom-1.wav` (2 s), `impacto-boom-2.wav` (2,6 s) |
| Papel (polaroid colocada) | `papel-colocando.wav` (0,7 s) |
| Datilografia | `tecla-maquina-unica.wav` (batida isolada), `tecla-maquina-sequencia.wav` (3,2 s) |
| Vento/rumble ambiente | `vento-rumble-tempestade-40s.wav` (40 s, grave com modulação lenta) |
| Trovão distante, 2 | `trovao-distante-1.wav` (7 s), `trovao-distante-2.wav` (9 s) |

Os sintetizados são funcionais mas simples: ouvir antes de usar; se algum soar artificial, trocar pelos reais acima (toc real, datilografia real) ou por pacote CC0 baixado manualmente pelo Rodrigo.
