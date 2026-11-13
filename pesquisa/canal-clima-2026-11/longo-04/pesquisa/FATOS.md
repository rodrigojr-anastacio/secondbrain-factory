# Fatos com fonte: Em Relevo 004, 1983 (El Niño: enchente no Sul × seca no sertão)

Pesquisa 13/11/2026 (etapa 1). Regra do brief: número de 1983 só com fonte primária; sem primária vira "segundo X" ou sai.
Status: **PRIMÁRIA** (órgão oficial/dado bruto conferido por mim) · **SEGUNDO X** (acadêmico/memorial; narrado com atribuição) · **FORA** (não entra).

## Sul
| ID | Fato | Número | Fonte | Status |
|---|---|---|---|---|
| F1 | União da Vitória/Porto União, julho de 1983: o Iguaçu foi "de 2,50 metros" a **10,42 m**; chuva de ~800 mm (média jun–jul 138 mm); +2.400 famílias vulneráveis; **18 mortos**; cidade sem luz, água e comida | 2,50 → 10,42 m; 800 mm; 18 | Defesa Civil do Paraná, "Enchente de União da Vitória de 1983" (PDF) https://www.defesacivil.pr.gov.br/sites/defesa-civil/arquivos_restritos/files/documento/2019-05/enchente_de_uniao_da_vitoria_de_1983.pdf (lido 13/11) | PRIMÁRIA |
| F2 | Cota diária do Iguaçu em União da Vitória (estação ANA 65310000): **pico 10,42 m em 18/07/1983**; 4,94 m em 03/07; subiu 5,5 m em 15 dias; >6 m por 56 dias em 1983; cheia menor em maio (6,65 m em 01/06) e já em nov/1982 (6,45 m em 27/11); mediana 1982–84 = 2,9 m | ver `dados/ana_65310000_cota.json` | ANA HidroWeb (webservice `HidroSerieHistorica`, baixado 13/11) | PRIMÁRIA (bate com F1 ao centímetro) |
| F3 | Blumenau, régua do Itajaí-Açu em 1983: **04/03 10,60 m · 20/05 12,52 m · 09/07 15,34 m · 24/09 11,75 m** (quatro cheias acima de 10 m no mesmo ano). A de 07/08/1984 foi maior (15,46 m) | 15,34 m | Proteção e Defesa Civil de Blumenau, tabela "Enchentes registradas" https://defesacivil.blumenau.sc.gov.br/p/enchentes (lida com curl 13/11) | PRIMÁRIA |
| F4 | SC, julho de 1983: **78 municípios em calamidade pública, 197.790 desabrigados, 49 mortos** | 197.790; 49; 78 | Herrmann (2001), citado em artigo da Revista Brasileira de Geografia Física/Redalyc https://www.redalyc.org/pdf/317/31735766012.pdf; a NSC repete "49 mortos e quase 200 mil desabrigados". Não achei boletim oficial de 1983 | SEGUNDO X ("segundo levantamento da geógrafa Maria Lúcia Herrmann, da UFSC") |
| F4b | "162 de 199 municípios em calamidade" (Lavratti) e listas por município do Atlas IOESC | — | divergem entre si e de F4 | FORA |
| F4c | "80% de União da Vitória debaixo d'água por 45 dias"; "60.330 desabrigados em UV" | — | só imprensa (Gazeta do Povo) / Atlas citado em artigo; não está no documento da Defesa Civil PR | FORA |

## Sertão
| ID | Fato | Número | Fonte | Status |
|---|---|---|---|---|
| F5 | Mombaça (CE), pluviômetro do DNOCS (ANA 00539001, série 1911–2024, 70 anos completos): média **783 mm/ano**; 1979 625 · 1980 754 · **1981 472 · 1982 407 · 1983 366 mm (47% da média)**; 1983 é o 6º ano mais seco da série | 366 mm; 47% | ANA HidroWeb (`dados/ana_539001_chuva.json`, baixado 13/11) | PRIMÁRIA |
| F6 | Fortaleza 1983: 933 mm (64% da média de 1.450) — o litoral sofreu menos; 1984 voltou a 2.026 mm | 933 | GHCN v2/NOAA (`../longo-03/dados/chuva-fortaleza-anual.csv`) | PRIMÁRIA (não usado na fala; só se precisar) |
| F7 | Programa de Emergência (frentes de serviço) da seca: alistados **1981 1,169 milhão · 1982 702 mil · 1983 3,13 milhões**; pico de 1979 ~460 mil (dados da Sudene); gastos 1979–83 = US$ 1,204 bilhão | 3,13 milhões | Revista de Economia Política (SciELO), "Natureza econômica de uma catástrofe natural… seca nordestina de 1979-80", notas 2, 3 e 5 (dados da SUDENE) http://www.scielo.br/j/rep/a/vX9PHYKCD5MKLzLHqJH9MTJ/ | SEGUNDO X ("pelos números da Sudene") |
| F8 | Ago/1983: ~100 flagelados de Itapipoca ocupam o Palácio da Luz (governo do CE); dois dias depois, **5 mil flagelados saqueiam a Cobal em Canindé (CE)** | 5 mil | Memorial da Democracia (Instituto Lula), "País descobre a tragédia da seca" (12/08/1983) http://www.memorialdademocracia.com.br/card/pais-descobre-a-tragedia-da-seca | SEGUNDO X (fato amplamente noticiado; narrar sem número exato se preferir: "milhares") |
| F9 | Em 1983 havia **10 milhões de flagelados**, mais de 1/3 da população do NE | 10 mi | Memorial da Democracia (mesma página) | SEGUNDO X |
| F9b | "A Sudene estimou 3,5 milhões de mortos em 5 anos" | 3,5 mi | Memorial da Democracia; número muito citado e **contestado** (sem documento da Sudene localizado) | FORA da narração (só registrar). Narração: "ninguém contou os mortos" |
| F10 | 1979–1983 = a maior seca do século XX em área (técnico da Sudene); 2,7 milhões de alistados no ciclo todo (tabela PROJE) | — | UFPB/ABET (tabela citada); Diário do Nordeste | SEGUNDO X (usar só "uma das maiores secas do século") |

## Clima (El Niño)
| ID | Fato | Número | Fonte | Status |
|---|---|---|---|---|
| F11 | RONI (índice relativo, o que a NOAA usa para comparar El Niños): 1982-83 pico **+2,40 em DJF 1983** (recorde desde 1950); MJJ 1983 já **+0,47**; JJA 1983 +0,03 | ver `dados/roni.txt` | NOAA CPC https://www.cpc.ncep.noaa.gov/data/indices/RONI.ascii.txt (13/11) | PRIMÁRIA |
| F12 | ONI 1982-83 pico +2,14 (DJF 1983); ONI 2026 ASO **+2,46**; RONI 2026 ASO **+1,97** | | NOAA CPC oni.ascii.txt / RONI.ascii.txt | PRIMÁRIA |
| F13 | Boletim NOAA/CPC de **12/11/2026**: El Niño Advisory; Niño-3.4 **+2,5 °C**, Niño-1+2 +4,4 °C; El Niño forte a muito forte provável até JFM 2027 (**> 79%**); chance de evento histórico (RONI ≥ 2,5, maior desde 1950) **~60% em OND e NDJ**; deve enfraquecer no começo de 2027; "impactos mais prováveis, mas não garantidos"; próximo boletim 10/12/2026 | ~60%; >79% | https://www.cpc.ncep.noaa.gov/products/analysis_monitoring/enso_advisory/ensodisc.shtml (cópia em `dados/cpc-ensodisc-2026-11-12.html`) | PRIMÁRIA |
| F14 | Mecanismo Sul: em 1982-83, jato subtropical forte sobre a América do Sul + várias situações de bloqueio favoreceram as chuvas | — | Kousky & Cavalcanti (1984, INPE), citados em Atmósfera (Elsevier) https://www.elsevier.es/es-revista-atmosfera-76-articulo-re-analysis-pluvial-precipitation-in-southern-S018762361471104X ; mesma explicação do longo-02 b24 | SEGUNDO X (explicação didática, sem número) |
| F15 | No Sul, El Niño dá chuva acima da média **sobretudo na primavera e no outono-inverno do ano seguinte** (por isso as cheias de mai–jul/1983, com o Pacífico já esfriando) | — | Grimm et al. (UFPR), citado em Redalyc/RBGF; Grimm (2000) J. Climate | SEGUNDO X / consenso acadêmico |
| F16 | Mecanismo NE: ar sobe no Pacífico quente e desce sobre a Amazônia/norte do NE → menos chuva; no CE a quadra chuvosa é fev–mai, e em 1983 ela caiu em cima do pico do El Niño | — | longo-02 b24 (checado), longo-03 C7/C8b | já checado |
| F17 | Distância União da Vitória → Mombaça ≈ **2.580 km** (Blumenau → Mombaça 2.560 km) | ~2.500 km | cálculo haversine (coordenadas IBGE) | PRIMÁRIA (cálculo) |

## 2026 (paralelo, sem alarmismo)
| ID | Fato | Fonte | Status |
|---|---|---|---|
| F18 | Out/2026: INMET registrou 581,6 mm em Dionísio Cerqueira (SC) e **577,6 mm em Laranjeiras do Sul (PR)**, "com recordes na região Sul… devido à influência do El Niño" | INMET, nota de 09/11/2026 https://portal.inmet.gov.br/noticias/nota-sobre-os-destaques-meteorol%C3%B3gicos-de-outubro-de-2026 (checada no longo-02 4a) | PRIMÁRIA |
| F19 | SC, 7–8/11/2026: danos em **54 municípios**, 11 em emergência | Defesa Civil SC 09/11/2026 (longo-02 CHECAGEM §133) | PRIMÁRIA |
| F20 | INMET (Painel El Niño, out/2026): nov–jan com chance maior de chuva abaixo do normal em grande parte do Norte e áreas do Nordeste; Funceme: ainda cedo para prever a quadra chuvosa 2027 | longo-03 FATOS C11/D7 | OFICIAL (resumo) |
| F21 | > 1,2 milhão de cisternas no semiárido (P1MC/ASA) | longo-03 b42 (checado) | CONFIRMADO |
| F22 | Blumenau tem sistema de alerta de cheias (CEOPS/Furb) e a Defesa Civil manda alerta no celular | Hipótese de fecho genérica; **não** citar ano nem número | só formulação genérica |

## Fontes de imagem
Ver `FOTOS.md` (30 imagens com licença conferida; **nenhuma foto livre da enchente de 1983 nem da seca de 1983**) e a seção Satélite. Imagens novas desta etapa: `dl/fotos/satelite/landsat4-uv-19830703-par.jpg` (3/07, rio a 4,94 m, 0% nuvem) e `landsat4-uv-19830804-par.jpg` (4/08, rio ainda a 7,42 m; várzea a sudeste alagada; nuvens sobre a cidade). Mesma janela (72 × 40 km centrada em União da Vitória), Landsat 4 MSS, domínio público (USGS), processadas por `tools/landsat_par.py`. A cena de 26/07 (9,15 m) está coberta de nuvens: descartada.
