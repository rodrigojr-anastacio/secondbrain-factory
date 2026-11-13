# Dados e geometrias: longo 03 (Grande Seca de 1877-79)

Acesso a todas as fontes em **13/11/2026**. Scripts em `shared/` (`prep_sst.py`, `prep_semiarido.py`, `prep_trilhos.py`, `prep_historia.py`), rodados com um venv fora do repo (`~/cache/venv-nc`: h5py, numpy, shapely, openpyxl). Brutos grandes em `dl/dados/` (fora do git). Lat/lon WGS84; para a cena, usar a projeção de `../longo-02/shared/geo.json` (`P(lon,lat)`).

## 1. Chuva anual em Fortaleza: `dados/chuva-fortaleza-anual.csv`, `chuva-fortaleza-resumo.json`
- **Fonte:** NOAA NCEI, GHCN v2 precipitação mensal, estação 30382397000 Fortaleza (-3,70; -38,50), https://www.ncei.noaa.gov/pub/data/ghcn/v2/v2.prcp.gz (bruto: `dl/dados/fortaleza_v2_raw.txt`). Domínio público (governo dos EUA). A série original é da Funceme/INMET (artigos: Fortaleza 1849-1999 vem da Funceme).
- **Processo:** soma dos 12 meses (décimos de mm / 10). Ano com mês faltando fica sem `mm` (coluna `meses_faltando`; `mm_parcial...` traz a soma dos meses existentes). 1849-2019 existem; 153 anos completos (2019 incompleto; **2020-2026 não estão na série**, GHCN v2 parou).
- **Média 1849-2018: 1.450 mm** (mediana 1.415; 1991-2018: 1.482).
- **Anos-chave (mm; % da média):** 1877 = **468 (32%)**, 1878 = 503 (35%), 1879 = 597 (41%), 1915 = 563, 1932 = 878, 1958 = 518, 1983 = 933, 1993 = 1.010, 2012 = 1.012, 2013 = 890, 2014 = 1.237, 2015 = 1.260, 2016 = 1.415, 2017 = 1.469, 2018 = 1.342.
- **Ranking dos mais secos (153 anos): 1877 (1º), 1878 (2º), 1958, 1915, 1879 (5º).** Os três anos da Grande Seca somam 1.568 mm, média 523 mm/ano.
- Mensal 1877: jan 24, fev 16, mar 84, abr 40, mai 102, jun 84, jul 44, ago 46, set 20, out 0, nov 8, dez 0 mm (o "quadra chuvosa" de 1877 foi um terço do normal). 1878: maio 192, mas jun 4, depois ~0.
- Cuidados: a série de Fortaleza é costeira (a seca de 2012-17 quase não aparece na capital: média 2012-18 = 1.232 mm); antes de ~1900 a qualidade do pluviômetro é incerta (instrumento, local). Um ano com 1 mês faltando fica sem total.

## 2. Niño 3.4: `dados/nino34-1870-2026.csv` (começa em 1854), `nino34-resumo.json`
- **Fonte:** NOAA ERSSTv5, `sst.mnmean.nc` (NOAA PSL THREDDS, https://psl.noaa.gov/thredds/fileServer/Datasets/noaa.ersst.v5/sst.mnmean.nc; 162 MB, em `dl/dados/`), 1854-01 a 2026-10. Domínio público.
- **Processo:** média ponderada por cos(lat) da caixa 5S-5N, 170W-120W; **anomalia vs. climatologia mensal 1991-2020** (valores em °C). Atenção: o ONI oficial da NOAA usa bases móveis de 30 anos, então nossos números **não são o ONI** (antes de 1950 o ONI sai menor porque a base é mais fria). O URL de `nino34.long.anom.data` do PSL não existe mais (404).
- **Média nov-dez-jan (NDJ) dos maiores eventos:** 2015-16 **+2,64**; **1877-78 +2,41**; 1997-98 +2,35; 1982-83 +2,14; 1888-89 +2,03; 2023-24 +1,96; 1972-73 +1,92.
- **Pico mensal:** 1877-11/12 = +2,40; **1878-02 = +2,53**; 1982-12 +2,19; 1983-01 +2,33; 1997-11 +2,40; 2015-11 +2,71; 2016-01 +2,56; 2023-12 +2,03.
- **2026:** jun +1,54, jul +1,99, ago +2,53, set +2,84, **out/2026 = +3,06, o maior mês de toda a série 1854-2026**. Em 1877: jul +0,93, ago +1,88, set +2,00, out +2,07, nov +2,40, dez +2,40, jan/78 +2,43, fev/78 +2,53, mar +0,81, depois La Niña (nov/78 -1,63).
- Caveats: reconstrução estatística, incerteza grande antes de 1900 (poucos navios); dizer "reconstruções indicam", não "foi medido".

## 3. Mapas de anomalia da temperatura do mar
Formato idêntico a `../longo-02/shared/sst_pacifico.json` (`lon0,lat0,passo,nx,ny,datas,grades[t][linha lat sul→norte][col lon oeste→leste]`, `null` onde não há dado).
- `dados/sst_1877.json`: **Pacífico** (lon 100E→290E, lat -30→+30, passo 1°, 191×61), datas 1877-11, 1877-12, 1878-01, 1878-02 (rótulos dia 15 = média do mês). 248 KB.
- `dados/sst_1877_global.json`: mundo (lon -179..180, lat -89..89; mesmo formato de `sst_global.json`) para as mesmas 4 datas. 1,3 MB.
- `dados/sst_comparativo.json` (Pacífico) e `sst_comparativo_global.json` (mundo): dez/1877, dez/1982, dez/1997, dez/2015, dez/2023 e **out/2026**. Serve para lado a lado. Os de out/2026 usam a mesma fonte (ERSST), então são comparáveis com 1877; o `sst_pacifico.json` do longo-02 (OISST diário 0,25°, 2026-06 a 11-08) tem mais resolução mas **fonte diferente**, evite misturar na mesma comparação.
- **Fonte/processo:** ERSSTv5 (grade nativa de **2°**; interpolado bilinearmente para 1° só para encaixar no formato; a resolução real continua 2°). Anomalia vs. 1991-2020 (mesma base do OISST do longo-02). Pontos de referência: pico anômalo no Pacífico leste/central em dez/1877 de até +4,6 °C numa célula; no equador a 140W: 1877-12 +2,8; 1982-12 +3,1; 1997-12 +3,1; 2015-12 +3,2; **2026-10 +4,1**.
- **Aviso editorial:** antes de 1900 o ERSST é reconstrução esparsa: padrão em grande escala, não detalhe local. Em 1877 a "mancha" é suavizada.

## 4. Geometrias
- `dados/semiarido.json`: GeoJSON com 3 Features: **Semiárido brasileiro** (1.477 municípios, lista IBGE "Situação 2022"; = SUDENE 2021), **Semiárido no Ceará** (175 de 184 municípios) e **contorno do Ceará**. Dissolvido e simplificado (0,01°), 30 KB.
  - Fontes: lista `https://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/semiarido_brasileiro/Situacao_2022/lista_municipios_Semiarido_2022.xlsx` (IBGE, dados abertos; citar IBGE) + malhas municipais IBGE API v3 (`servicodados.ibge.gov.br/api/v3/malhas/estados/<UF>?intrarregiao=municipio`, qualidade mínima). O IBGE só publica **lista**, não shapefile; a geometria é nossa (união das malhas).
  - **Polígono das Secas (1936/1951): NÃO achei shapefile.** O Semiárido oficial atual é a referência, mais amplo que o polígono histórico. Se for preciso o polígono antigo, é digitalização manual.
- Estados do NE: **`../longo-02/dados/br-ufs.json` serve** (todas as 27 UFs, `codarea` 21-29 = MA a BA, 23 = CE; baixa resolução). Malhas municipais do CE prontas em `dl/dados/mun23.json`.
- `dados/rios-ce.json`: **Jaguaribe, Banabuiú, Acaraú, Curu, Salgado, Choró** (MultiLineString, simplificado 0,008°). Fonte: OpenStreetMap (relações `waterway=river`, Overpass), **licença ODbL: "© contribuidores do OpenStreetMap"**. O Natural Earth 10 m não tem nenhum rio do CE (só Parnaíba), e o Overpass só respondeu com User-Agent próprio.

## 5. `dados/historia.json`
Pontos (cidades, açude, estações), linhas ferroviárias, rota da migração, marcos e números dos retirantes. **Cada item tem `fonte` e `nota`.**
- Coordenadas das cidades: Wikipedia pt (API `prop=coordinates`); Crato, Iguatu, Rio Branco e Maracanaú: aproximadas de conhecimento geral (Wikipedia não devolveu ponto utilizável), marcadas no JSON.
- **Açude do Cedro (barragem central): -4,97825; -39,06293** (OpenStreetMap, way 547305578 "Barragem Central"; vertedouro em -4,97666; -39,06096). Início da obra varia por fonte (1877 planejamento; 1881; 1884; 1890) e conclusão **1906** (120 anos em 2026).
- **EF de Baturité:** empresa fundada 05/03/1870; Fortaleza–Parangaba 14/09/1873; Mondubim/Maracanaú 14/01/1875; Pacatuba 09/01/1876; **Decreto 6.918 de 01/06/1878** (governo assume a obra, vira frente de socorro); ramal Canoa–Baturité 02/02/1882; **Quixadá 07/09/1891**; Senador Pompeu ~1896-97 (inferência, data exata não confirmada); Iguatu 05/11/1910; Crato anos 1920 (Wikipedia: 1926 "chega ao Crato", sem data). Fontes: Wikipedia pt "Estrada de Ferro de Baturité", Fortaleza em Fotos e Fatos, Diário do Nordeste. Traçado = **trilhos atuais do OSM** (menor caminho entre estações), pode diferir do original em detalhes.
- **EF de Sobral:** obra iniciada 1878; 1os trilhos em Camocim 26/03/1879; Camocim–Granja (24,5 km) **15/01/1881**; Sobral **31/12/1882**; Ipu 1894; Crateús 25/01/1925. Traçado Camocim–Granja: trechos OSM abandonados ligados por retas; **Granja–Sobral é esquemático** (leito desativado, fora do OSM; estações intermediárias não verificadas).
- Rota marítima Fortaleza→Belém→Manaus→Rio Branco: **esquemática** (cabotagem, calha do Amazonas, Purus). Números de migração (divergem): ~120 mil para a Amazônia + 68 mil para outras partes (Wikipedia en "Grande Seca", dos ~800 mil da região); Teófilo >300 mil (estimativa alta); só 4.963 emigrantes registrados chegando à província do Amazonas entre 06/1877 e 08/1878 (SciELO RBH).
- **Fortaleza:** 1872 = 42.458 hab (O Povo) ou 21 mil (Fortaleza em Fotos): fontes divergem; chegou a 100-130 mil (Freyre: 160 mil hab em dez/1878, 120 mil retirantes). **Dia dos Mil Mortos: 10/12/1878, 1.004 corpos enterrados num dia** (varíola + fome; O Povo).
- Retirantes na EFB: ~30 mil (pico), ~50 mil em dois anos, >60 mil (1878-80): fontes divergem. Uma fonte diz que a empresa parou por falta de caixa em 1877-78 antes do governo assumir.

## 6. `dados/fome-global-1877.json`
- **Total global:** Singh et al. 2018, *J. Climate* 31(23) "Climate and the Global Famine of 1876-78" (doi 10.1175/JCLI-D-18-0159.1; resumo: NASA NTRS 20180007824): "mais de 50 milhões" de mortos (cifra muito incerta, tratar como "estimativas chegam a mais de 50 milhões"). O título "The Great Global Drought of 1875-1878" não é o do artigo. Causas segundo o paper: Pacífico frio 1870-76, El Niño recorde 1877-78, dipolo do Índico recorde 1877, Atlântico Norte quente 1878; seca na Ásia de monções = a mais intensa em 800 anos.
- **Índia:** 5,6-9,6 milhões (oficial 5,6; Maharatna 8,2; Digby 9,6); Mysore perdeu 874 mil habitantes vs. 1871. (Wikipedia en "Great Famine of 1876-1878", citando Dyson.) Madras/Bombaim/Hyderabad sem número por província.
- **Norte da China:** 9,5-13 milhões; por província (Forrest, 1879): Shanxi 5,5 mi, Zhili/Hebei 2,5 mi, Henan 1,0 mi, Shandong 0,5 mi; Shaanxi sem número (Wikipedia en "Northern Chinese Famine of 1876-1879"; Edgerton-Tarpley).
- **Brasil:** Nordeste 150-300 mil (Cicinato Ferreira Neto) a ~500 mil (Herbert Smith; repetido sem fonte primária); Ceará ~150-200 mil, "um terço da população morreu ou migrou". A cifra "400 mil no Ceará" (EBC) parece confundir com o Nordeste.
- **África / outras:** Singh et al. citam só "norte e sudeste da África" e Austrália (via Atlântico/Índico). **Não achei fonte verificada de mortes nem de recorte por país (Egito, Marrocos, Etiópia, África do Sul não confirmados).** O JSON deixa a linha com `null`; não desenhar mortes para isso.
- Centroides são aproximados (de regiões, não de polígonos).

## 7. Hoje: `dados/monitor-secas-2026-09.json`, `dados/hoje-2026.json`
- **Monitor de Secas:** o mais recente publicado é **setembro/2026** (divulgado ~20/10). **Outubro/2026 ainda não existe** (`.../mapas/outubro2026.zip` dá 404 em 13/11; sai por volta do dia 20). O arquivo é cópia do `../longo-02/dados/monitor-secas-2026-09.json` (categorias SI/S0/S1/S2; sem S3/S4). Fonte: ANA, Monitor de Secas (dado público; citar). Se o Rodrigo quiser outubro, repetir em ~20/11 com o mesmo procedimento do `longo-02/pesquisa/SATELITE.md` §5.
  - Manchetes: seca em **96% do Nordeste** (Correio da Manhã 23/10/2026); seca grave avançou na BA, PE, PI e SE/AL/PB passaram de moderada a grave; seca grave em 28% do NE (fontes divergem entre agosto e setembro). Ceará em jan/2026: **68 municípios em seca extrema (S3), pior desde fev/2019**; excepcional não ocorre no CE desde jan/2018 (Diário do Nordeste 23/02/2026).
- **Cisternas:** P1MC/ASA: **mais de 1,2 milhão** de cisternas de consumo humano (marca dos 20 anos, 2023; matéria de fev/2026 repete ">1,2 mi"); média ~50 mil por ano; 1.262 municípios. Sem número oficial de 2026 com data de corte (painel do MDS/ASA teria).
- **Previsão:** NOAA/CPC (set/2026): 93% de chance de El Niño "muito forte", 69% de nível histórico em out-dez. **Funceme (set/2026):** ainda não dá para dizer como será a quadra chuvosa 2027 (fev-mai); El Niño pode trazer "maior irregularidade", veranicos e calor; o Atlântico tropical também decide; atualização "nos próximos meses". **INMET (Painel El Niño, outubro):** nov/2026-jan/2027 com maior chance de chuva abaixo do normal em grande parte do Norte e áreas do Nordeste; impactos no NE em verão e outono, sobretudo no norte da região. A previsão trimestral dez-fev para o semiárido **não foi verificada no PDF original** (só em notícias).
- **Açudes do CE:** 46% da capacidade no início de outubro/2026 (O Povo 03/10; 3º maior volume da década); Sertões de Crateús, Baixo Jaguaribe, Banabuiú e Médio Jaguaribe < 30%; Cogerh espera mais evaporação com El Niño. Número de novembro: Portal Hidrológico do Ceará.

## Arquivos
| Arquivo | O que é |
|---|---|
| `dados/chuva-fortaleza-anual.csv` | ano, mm, meses_faltando, parcial, destaque (1849-2019) |
| `dados/chuva-fortaleza-resumo.json` | médias, razões 1877-79, ranking dos mais secos |
| `dados/nino34-1870-2026.csv` | ano_mes, anomalia_c (1854-01 a 2026-10, base 1991-2020) |
| `dados/nino34-resumo.json` | picos NDJ e mensais por ano |
| `dados/sst_1877.json`, `sst_1877_global.json` | anomalia do mar nov/77-fev/78 (Pacífico; mundo) |
| `dados/sst_comparativo.json`, `sst_comparativo_global.json` | dez/77, 82, 97, 2015, 2023 e out/2026 |
| `dados/semiarido.json` | Semiárido, Semiárido no CE, contorno do CE |
| `dados/rios-ce.json` | rios principais do CE (OSM, ODbL) |
| `dados/historia.json` | cidades, estações, linhas, rota, marcos |
| `dados/fome-global-1877.json` | regiões, centroides, mortes com fonte |
| `dados/monitor-secas-2026-09.json` | Monitor de Secas, set/2026 (ANA) |
| `dados/hoje-2026.json` | cisternas, previsão Funceme/INMET/NOAA, açudes |
