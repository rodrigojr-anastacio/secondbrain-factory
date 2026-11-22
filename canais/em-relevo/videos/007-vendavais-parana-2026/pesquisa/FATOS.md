# FATOS (curados) · Em Relevo 007 · vendavais no Paraná de 20/11/2026 · 21/11/2026

Base: `FATOS-bruto.md` (pesquisa de 21/11, com URL de cada linha) + leituras diretas na AEN via WARP + dados próprios (`../dados/`). Cada fato tem um ID usado no `SOURCES.md` e no `shared/roteiro.py`.
**P** = fonte primária (órgão oficial/artigo científico/dado bruto). **S** = secundária (imprensa citando o órgão): **reconferir na AEN/Simepar antes da voz (etapa 2)**; se não confirmar, a frase vira "segundo o Simepar" ou sai. **N** = dado próprio (calculado por nós a partir de dado público).

## E · O evento de sexta, 20/11/2026 (feriado da Consciência Negra)
| ID | fato | fonte | tipo |
|---|---|---|---|
| E1 | Previsão de 19/11: "Um sistema de baixa pressão se intensifica sobre o Paraguai e muda as condições de tempo já no período da manhã no Oeste e Sudoeste"; à tarde e à noite os temporais atingem as outras regiões, "favorecidos pelo calor e a umidade disponíveis na atmosfera"; > 30 °C previstos no Norte | Simepar (Lizandro Jacóbsen) via AEN, 19/11/2026 — https://www.parana.pr.gov.br/aen/Noticia/Feriado-tem-previsao-de-altas-temperaturas-e-chuva-volumosa-no-Parana-diz-Simepar | P (lido) |
| E2 | Dois tornados F1 (Fujita; vento estimado 117–180 km/h): Foz do Iguaçu (Vila Yolanda) ~15h; Manoel Ribas (área rural, Santa Mariana) ~18h; confirmação do Simepar em 21/11 16h42 | Simepar via O Bemdito, Metrópoles, CNN Brasil, 21/11 | S |
| E3 | Causa segundo o Simepar: "diversas linhas de instabilidade", das primeiras horas da tarde ao fim da noite; a metade oeste foi a mais atingida; umidade, instabilidade forte e vento que muda de força e direção com a altura | Marco Jusevicius (Simepar) via Agora Litoral; nota via Metrópoles, 21/11 | S |
| E4 | Rajadas das estações do Simepar (hora · km/h): Paranaguá 13h15 63,7 · Capanema 13h45 81,7 · Cambará 14h 88,6 · Francisco Beltrão 14h30 76,7 · Santa Helena 15h15 74,2 · Toledo 16h 67 · Cascavel 16h15 66,2 · Laranjeiras do Sul 16h15 68 · Ubiratã 16h45 74,5 · Santa Maria do Oeste 17h30 62,3 · Campo Mourão 17h45 79,9 · Cianorte 18h 70,2 · Maringá 18h45 77 (aeroporto 18h25 77,8) · Londrina 19h30 87,8 · Cornélio Procópio 20h15 98,3 (maior do dia) · Santo Antônio da Platina 20h45 62,6 | Simepar, lista repassada por CBN Curitiba e Folha de Londrina, 21/11 (`../dados/rajadas-2026-11-20.json`) | S |
| E5 | Copel: pico de 353.849 unidades consumidoras sem energia às 20h02 de sexta; 98.362 às 7h de sábado (Oeste 26,8 mil, Norte 24,9 mil, Noroeste 18,1 mil, Sudoeste 15,4 mil) | Copel via Diário do Sudoeste e Folha de Londrina, 21/11 | S |
| E6 | Defesa Civil PR (boletim de sábado 21/11): 9 municípios, 745 pessoas afetadas, 249 imóveis danificados (quase metade em Foz), 12 desalojados, 4 casas destruídas | Defesa Civil PR via CNN Brasil, Band News Curitiba, Misto Brasil | S |
| E7 | Foz: destelhamentos sobretudo na Vila Yolanda, ~50 quedas de árvores, lonas para ~200 famílias; Londrina: 43 ocorrências (39 quedas de árvores, 4 destelhamentos) | Defesa Civil de Foz e de Londrina via Folha de Londrina e Tarobá, 21/11 | S |
| E8 | Chuva estimada por satélite em 20/11 (dia UTC): máx. ~119 mm no litoral (−25,85; −48,85); média 16,6 mm no recorte do PR | NASA GPM IMERG Late (`../dados/nasa/pr-2026-11-20.json`) | N (P de base) |
| E9 | Sequência do satélite GOES-19 (canal 13, infravermelho, a cada 20 min, 9h → 0h): às 9h já há um aglomerado de tempestades a oeste/sudoeste do Paraná; ao longo da tarde ele cresce e se estica; às 20h é uma faixa de topos muito frios atravessando o estado de sudoeste a nordeste | NOAA/NESDIS STAR, setor "Southern South America" (`../dl/goes19/`, domínio público; crédito na descrição) | P (imagem) — **georreferenciar na etapa 2** (ver nota G) |

## N · Dados próprios
| ID | fato | como | tipo |
|---|---|---|---|
| N1 | Os picos de rajada de 14 estações (sem Paranaguá e Cambará, células separadas) caem numa reta: o pico chega mais tarde quanto mais a nordeste está a estação (r² = 0,98); direção ~54° do leste para o norte (sudoeste → nordeste); ~430 km de ponta a ponta; ~70 km/h | regressão hora × distância sobre E4 + coordenadas IBGE das sedes (script no `ETAPA1-PRONTA.md`; refazer na etapa 2) | N |
| N2 | Capanema → Cornélio Procópio: 423 km em 6 h 30 (13h45 → 20h15) ≈ 65 km/h em linha reta | grande círculo entre as sedes | N |
| N3 | Chuva de 1 a 20/11/2026 no PR: média de ~175 mm, contra ~108 mm esperados para esses 20 dias (climatologia IMERG 2001–2020) ≈ +61% | NASA GPM IMERG Late + GPM_3IMERGM (`../dados/nasa/pr-nov-1a20-anom.json`) | N |
| N4 | Perfil de relevo oeste → leste (Foz → Cascavel → Guarapuava → Curitiba → Serra do Mar): **gerar na etapa 2** com SRTM/Terrain Tiles (como `dados/perfis.json` do 006) e conferir as altitudes do R1 | SRTM | N (a fazer) |

## R · Relevo do Paraná
| ID | fato | fonte | tipo |
|---|---|---|---|
| R1 | Altitudes de ~120 m no Planalto de Foz do Iguaçu a ~800 m no Planalto de Cascavel | Atlas Geomorfológico do Paraná (2006), citado em capítulo da Embrapa — https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1128034/1/1805-capitulo-1.pdf | S (cita a primária) — conferir com N4 |
| R2 | Compartimentos de Maack: Litoral, Serra do Mar, Primeiro, Segundo e Terceiro Planaltos; o Terceiro desce de ~1.200 m a leste para ~300 m a oeste, em degraus, inclinado para o rio Paraná | Maack (1968), via resumos (infoescola/UEPG) | S — números finais vêm do N4 |
| R3 | Pico Paraná ~1.900 m, maior altitude do Sul do Brasil | IBGE/ICMBio (conferir) | S |

## C · Ciência (fora da manada como números/frases)
| ID | fato | fonte | tipo |
|---|---|---|---|
| C1 | Zipser et al. (2006, BAMS 87:1057), 7 anos do satélite TRMM: as tempestades mais intensas do planeta se concentram em poucas áreas continentais, entre elas o sudeste da América do Sul; release da NASA: "The strongest storms were found to occur east of the Andes Mountains in Argentina" | DOI 10.1175/BAMS-87-8-1057; release NASA/Goddard 27/10/2006 | P |
| C2 | Velasco & Fritsch (1987, JGR 92:9591): os complexos convectivos de mesoescala são tão frequentes na América do Sul de latitudes médias quanto na América do Norte; muitos crescem à noite | doi:10.1029/JD092iD08p09591 (abstract) | P — **conferir "à noite" no texto antes de usar** |
| C3 | Lopes & Nascimento (UFSM, 2025), 310 ocorrências: o setor de maior frequência de tornados no Sul inclui o norte do RS, o oeste de SC e o **sudoeste do PR** | Ciência e Natura 47, DOI 10.5902/2179460X84051 | P |
| C4 | Brooks, Lee & Craven (2003): ambientes favoráveis a tempestades severas significativas no sul do Brasil e norte da Argentina | Atmos. Res. 67–68 | P (só como apoio) |

## B · O "novamente"
| ID | fato | fonte | tipo |
|---|---|---|---|
| B1 | Rio Bonito do Iguaçu, 07/11/2025: laudo final F4; trilha de ~75 km, largura de 750 m a 3.250 m; 8 municípios de Quedas do Iguaçu a Cantagalo (de oeste para leste); a supercélula percorreu ~270 km a ~80 km/h; tornado em Rio Bonito ~18h10 | Simepar via AEN, 26/11/2025 — https://www.parana.pr.gov.br/aen/Noticia/Laudo-tecnico-final-do-Simepar-eleva-classificacao-de-tornados-que-atingiram-11-cidades | P |
| B2 | Maringá, 02/11/2026: tornado F2 de madrugada (~3h no radar), trilha de ~15 km, 180–250 km/h; telhas lançadas a mais de 1.300 m | Simepar via AEN, 04/11/2026 — https://www.parana.pr.gov.br/aen/Noticia/Classificacao-do-Simepar-confirma-que-Maringa-foi-atingida-por-um-tornado | P |
| B3 | Temporais de 1–2/11/2026: 17 municípios, 1.277 afetados, 350 residências danificadas (Maringá e Marquinho) | Defesa Civil PR via AEN, 02/11/2026 | P (lido) |
| B4 | 07/11/2026: 493,1 mil unidades sem energia, a maior contingência do ano para a Copel | Copel via AEN, 07/11/2026 | P |
| B5 | Simepar classificou 15 tornados no PR em 2026 até 06/11 (13 de supercélula, 2 landspouts) | Simepar via AEN, 06/11/2026 | P |
| B6 | 12/11/2026: 33 estações do Simepar passaram de 30 °C; máx. 35,1 °C em Cerro Azul | Simepar via AEN, 13/11/2026 | P |
| B7 | El Niño "muito forte"; Simepar prevê chuva acima da média no PR até março, com "mais temporais severos acompanhados de ventos fortes, incidência de granizo e raios" | Simepar via AEN, 12/11/2026 | P |
| B8 | Imagem Sentinel-2 da cicatriz do tornado de Rio Bonito | Wikimedia Commons, Copernicus/ESA (atribuição) | P (imagem) |

## O · Serviço
| ID | fato | fonte |
|---|---|---|
| O1 | Alertas da Defesa Civil por SMS: CEP para 40199 (também WhatsApp (61) 2034-4611) | Defesa Civil PR via AEN, 02/11/2026 |
| O2 | Defesa Civil: abrigo seguro, longe de árvores, postes, placas e estruturas que possam cair | idem |

## G · Notas para a etapa 2
- **GOES-19 georreferenciado:** o arquivo do STAR só guarda ~10 dias (baixado em `dl/goes19/`, 48 quadros 1800×1080 + 3600×2160 em 7 horários). Para pôr a sequência **no nosso mapa 3D**, use o NetCDF ABI-L2-CMIPF (canal 13) do bucket público `s3://noaa-goes19` (sem chave, permanente) e reprojete para lon/lat; o jpg do STAR só serve como prévia/thumb (cortar logo e legenda da NOAA: crédito só na descrição).
- **Reconferir os S do bloco E** na AEN/Simepar (notícias da Defesa Civil, Simepar e Copel sobre 20/11 devem sair entre 22 e 24/11). Fotos de 20/11 na AEN (galerias CC0) podem substituir a foto de 07/11 dentro do vídeo; a thumb C já tem foto CC0 de 07/11.
- **Não afirmar:** "uma linha só varreu o estado" (o Simepar fala em diversas linhas; Cambará 14h e Paranaguá 13h15 são células separadas); jato de baixos níveis ou frente fria como causa documentada de 20/11 (a frente fria é de domingo, 22); "primavera = pico de tornados" (a climatologia da UFSM dá o inverno).
