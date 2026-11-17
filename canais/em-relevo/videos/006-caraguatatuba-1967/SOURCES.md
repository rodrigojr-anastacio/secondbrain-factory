# SOURCES: Em Relevo 006 (Caraguatatuba 1967 × São Sebastião 2023) · 17/11/2026

Detalhe de cada fato (valor, fonte, grau, frase segura) em `pesquisa/FATOS.md`. Nenhum fato vem de vídeo/transcrição de concorrente; as transcrições (`ref/manada-*.txt`) só serviram para mapear o consenso (`ANGULO.md`).

## Fontes
| Sigla | Fonte | Tipo |
|---|---|---|
| CRUZ | Olga Cruz, "A serra do Mar e o litoral na área de Caraguatatuba – SP", Rev. Bras. Geografia 37(2), 1975 (IBGE, CC BY 4.0). https://rbg.ibge.gov.br/index.php/rbg/article/view/1161/858 | acadêmica (tese USP) |
| VIEIRA | B. C. Vieira, livre-docência FFLCH/USP, 2022. https://teses.usp.br/teses/disponiveis/8/630/tde-03062024-122514/publico/2022_BiancaCarvalhoVieira1.pdf | acadêmica |
| DIAS17 | Dias, Dias & Vieira, Rev. Depto. Geografia USP, 2017. https://revistas.usp.br/rdg/article/download/132714/129865/257869 | acadêmica |
| ISL20 | Dias, Vieira & Gramani, ISL 2020. https://www.issmge.org/uploads/publications/105/106/ISL2020-66.pdf | acadêmica |
| GADRI | M. Kobiyama, GADRI 2023 (dados CEMADEN). https://gadri.net/events/Kobiyama%20%28GADRI-report%202023%29-Sao%20Sebastiao-2023-Fev.pdf | técnico/dados oficiais |
| FAPESP | Pesquisa FAPESP 326 (2023), entrevista com P. L. Silva Dias (IAG-USP). https://revistapesquisa.fapesp.br/wp-content/uploads/2023/03/050-053_chuva-no-litoral-cie_326.pdf | divulgação científica |
| NASA-EO | NASA Earth Observatory, "Landslides in São Paulo, Brazil", 04/03/2023. https://science.nasa.gov/earth/earth-observatory/landslides-in-sao-paulo-brazil-151051/ | oficial |
| IBGE | Censo 2022 (Cidades); IBGE/CEMADEN 2018 "População em áreas de risco" (liv101589) | oficial |
| SGB | Cartas de suscetibilidade: Caraguatatuba (rigeo doc/19381), São Sebastião (doc/23448) | oficial |
| SRTM | AWS Terrain Tiles (SRTM/ETOPO), perfis em `shared/perfil_escarpa.py` → `dados/perfis.json` | dado bruto + cálculo próprio |
| IMERG | NASA GPM IMERG V07 (GES DISC), `dados/nasa/litoral-2023.json` | dado bruto + cálculo próprio |
| GEO | Almeida & Carneiro 1998, Rev. Bras. Geociências 28(2) (via resumos/citações) | acadêmica (secundária para nós) |
| FOTO | Defesa Civil de Ubatuba / Gov. SP, Commons, CC BY 2.0, 19/02/2023 (52699108915) | imagem com licença |

## Bloco → fatos (v2, regenerado do blocos.json)
| bloco | cap | fonte (IDs de pesquisa/FATOS.md) | fora da manada? |
|---|---|---|---|
| b01 | BERTIOGA (SP) · 18–19 FEV 2023 | C3 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b02 | SÃO SEBASTIÃO (SP) · 19 FEV 2023 | C3, S2 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b03 | SÃO SEBASTIÃO × CARAGUATATUBA | R2, R3 (perfis SRTM próprios), K1 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b04 | O MAPA | pergunta do T1/T2 | — |
| b05 | O MAPA | R2, R4 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b06 | O MAPA | R2, C4, P2 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b07 | O MAPA | P12; Cruz 1975 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b08 | 1 · A PAREDE | R4 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b09 | 1 · A PAREDE | R1, R2 (perfis SRTM próprios) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b10 | 1 · A PAREDE | R7 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b11 | 1 · A PAREDE | R4 (Cruz 1975), R6 (Almeida & Carneiro 1998, via resumos; sem idade) | parcial (recuo da escarpa no ToXu; aqui amarrado aos 1.300 m de Cruz) |
| b12 | 1 · A PAREDE | R3 (perfil SRTM próprio) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b13 | 2 · A CHUVA QUE A SERRA FABRICA | C3 (CEMADEN via Kobiyama/GADRI) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b14 | 2 · A CHUVA QUE A SERRA FABRICA | C1, C3, R3 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b15 | 2 · A CHUVA QUE A SERRA FABRICA | C7 (IMERG, cálculo próprio) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b16 | 2 · A CHUVA QUE A SERRA FABRICA | C2 (Pesquisa FAPESP 326) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b17 | 2 · A CHUVA QUE A SERRA FABRICA | C4, C5 (Kobiyama/GADRI, CEMADEN) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b18 | 2 · A CHUVA QUE A SERRA FABRICA | C8 (Cruz 1975, p. 103) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b19 | 2 · A CHUVA QUE A SERRA FABRICA | C10 (Vieira 2022, postos DAEE) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b20 | 3 · A CASCA DA SERRA | P2, P6 (corte ilustrativo) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b21 | 3 · A CASCA DA SERRA | P2 (De Ploey & Cruz 1979; Vieira 2022) | parcial (rocha + solo: fato obrigatório) |
| b22 | 3 · A CASCA DA SERRA | P10, P3 (Vieira 2022) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b23 | 3 · A CASCA DA SERRA | P5, P12 (Cruz 1975, carta de declividade) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b24 | 3 · A CASCA DA SERRA | P4, P6 (Dias, Dias & Vieira 2017) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b25 | 3 · A CASCA DA SERRA | foto Defesa Civil de Ubatuba/Gov. SP (CC BY 2.0), 19/02/2023 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b26 | 4 · 1967: O CAMINHO ATÉ A CIDADE | K1, K2 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b27 | 4 · 1967: O CAMINHO ATÉ A CIDADE | P7, P8, P9 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b28 | 4 · 1967: O CAMINHO ATÉ A CIDADE | P1, K2 | parcial (corrida de detritos citada por 4; aqui o termo de Cruz e "rodou") |
| b29 | 4 · 1967: O CAMINHO ATÉ A CIDADE | P11 (Gramani 2001) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b30 | 4 · 1967: O CAMINHO ATÉ A CIDADE | K3, K4 (Cruz 1975) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b31 | 4 · 1967: O CAMINHO ATÉ A CIDADE | K6, K7 | faixa e fazenda: sim; "número maior que o oficial": consenso |
| b32 | 4 · 1967: O CAMINHO ATÉ A CIDADE | M1 (SGB), P12, K7, K8 (IBGE 2022) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b33 | 5 · 2023: A MESMA RECEITA | S2 (NASA Earth Observatory) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b34 | 5 · 2023: A MESMA RECEITA | S2 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b35 | 5 · 2023: A MESMA RECEITA | R3, C3, P2 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b36 | 5 · 2023: A MESMA RECEITA | S3, S7 | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b37 | 5 · 2023: A MESMA RECEITA | S1 (Kobiyama/GADRI) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b38 | A RESPOSTA | síntese R1–R3, C1–C4, P2 | — |
| b39 | A RESPOSTA | síntese K2, S2 | — |
| b40 | A RESPOSTA | M1 (SGB); fecho sem previsão | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b41 | A RESPOSTA | M2 (IBGE/CEMADEN 2018) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b42 | A RESPOSTA | M3 (SMS 40199, Defesa Civil) | sim (dado/cena próprios; ver FATOS.md coluna manada?) |
| b43 | A RESPOSTA | CTA: puxa sessão para I5KpDKy6r3E (seca 1877, publicado); sem gancho de próximo vídeo | — |

## Cota de dados/cenas próprios (bíblia: ≥ 40%)
v2 (após crivo de ângulo r1): blocos de conteúdo = 39 (exclui pergunta b04, síntese b38–b39 e CTA b43); com dado/cena principal fora de todas as transcrições = 35; parciais/consenso = b11, b21, b28, b31 (fatos obrigatórios do tema, com palavras, números e ordem nossos) → **~90%**. As imagens do ToXu ("a serra que fabrica a chuva", "capa de solo", "concreto da betoneira", "a serra continua a mesma") foram retiradas.

## Divergências tratadas
- Chuva de 1967: 586 mm/48 h (cifra mais citada) × 115 + 420 mm (Cruz, posto da fazenda, aparelho transbordado) × 245 mm (DAEE): o roteiro usa Cruz e o DAEE como contraste (b19–b20) e não cita o 586.
- Vítimas de 1967: 120 (Cruz) a ~450–487 (IPT/contagem da época); "436 oficial" só na imprensa → faixa (b32).
- 2023: 682 × 683 mm (Bertioga), 626 × 627 (São Sebastião): usa 683/627 (FAPESP/Marengo).
- Inventário 2023 (~1.000 × 571 escorregamentos): não citado; "dezenas de faixas" na imagem.
