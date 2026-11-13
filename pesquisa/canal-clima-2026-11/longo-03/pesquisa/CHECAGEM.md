# CHECAGEM do roteiro: Em Relevo, vídeo 3 (A Grande Seca de 1877)

Feita em 13/11/2026 sobre `shared/roteiro.py` (47 blocos). Base: `FATOS.md` (C1–C12), `DADOS.md` (D1–D7) e consultas diretas desta data.
Regra: número sem fonte decente vira "segundo X", faixa, ou sai. Fala com números por extenso; tela com algarismos.

## Correções feitas em relação à pauta e ao 1º rascunho
| Onde | Antes | Depois | Por quê |
|---|---|---|---|
| hook (pauta) | "Fortaleza recebe mais de 100 mil retirantes" / "114 mil" | "chegam mais de 100 mil" (b01) e "quase 114 mil abarracados em agosto de 1878" (b13) | 113.900 é o nº de abarracados em ago/1878 (Barros Leal), não de chegados (C3b) |
| b04 | "muito mais brasileiros do que a Guerra do Paraguai" | "pelas contas mais altas, 5% da população do Império; proporcionalmente, a maior catástrofe da história do Brasil" | não achei o nº de mortos brasileiros no Paraguai com fonte firme; a Agência Senado diz literalmente "em termos relativos, a maior catástrofe da história do Brasil" e "5% da população do Império" |
| b26 | "visconde de Sinimbu" | "o chefe do governo, o senador Sinimbu" | o título de visconde é de 1888; em 1878 ele era senador e presidente do Conselho (gabinete de 05/01/1878) |
| b17 | "500 mil mortos" seco | faixa "de 150 mil a 500 mil" | NYT de época: 150 mil; Agência Senado/Ó Gráda: 400–500 mil (C2) |
| b16 | "dia dos mil mortos em 1879" (Wikipedia) | 10/12/1878 | erro da Wikipedia (C4) |
| — | "seca dos dois setes" | não usado | nome não achado em fonte (C1b) |
| — | frase da joia da Coroa como fato | narrada como lenda, com "não há documento" (b31) | sem fonte primária; O Povo 05/11/2026 diz que as joias não foram vendidas (C5b) |
| — | "+3,06 °C, o maior El Niño da história" | "pela mesma reconstrução, no nível do de 1877 ou acima" (b39) | +3,06 é ERSSTv5 mensal (out/2026) contra 1991–2020, não é o ONI oficial; a NOAA ainda não declarou recorde (ver longo-02) |

## Bloco a bloco
| Bloco | Afirmação | Valor na fala | Fonte | Status |
|---|---|---|---|---|
| b01 | Fortaleza ~25 mil hab. em 1877; chegam > 100 mil | 25 mil; mais de 100 mil | Diário do Nordeste; Agência Senado (~25 mil); Neves 2000 via Barboza 2015 (> 100 mil) | FAIXA (20–30 mil; usamos "uns") |
| b02 | Dez/1878: 160 mil pessoas, segundo Theophilo | 160 mil; "mais de 6 vezes" (160/25 = 6,4) | Theophilo via Diário do Nordeste | SÓ CITADO (atribuído a ele na fala) |
| b03, b16 | 10/12/1878: 1.004 mortos de varíola; > 200 corpos para o dia seguinte | 1.004; "mais de 200" (fonte: 230) | O Povo 12/04/2020; Diário do Nordeste | CONFIRMADO (imprensa citando registros/Theophilo) |
| b04 | ~500 mil = 5% do Império; maior catástrofe relativa | "estimativas chegam"; "pelas contas mais altas" | Agência Senado, Arquivo S, 01/10/2021 (lido em 13/11/2026) | CONFIRMADO como estimativa |
| b07 | Quadra chuvosa do sertão: fev–mai | — | Funceme (quadra chuvosa fev–mai, definição oficial) | CONFIRMADO |
| b08 | Tradição de São José (19/03); em 1877 não choveu | — | Agência Senado ("quando chegou o dia 19 de março e nenhuma gota de água caiu") | CONFIRMADO |
| b09 | Fortaleza: série desde 1849; média > 1.400 mm; 1877 = 468 mm (32%), o mais seco; 1878 o 2º (503 mm) | idem | GHCN v2, estação 30382397000 (NOAA NCEI), soma anual (`dados/chuva-fortaleza-anual.csv`; média 1849–2018 = 1.450 mm; 153 anos completos) | CONFIRMADO no dado (nosso cálculo) |
| b10 | Sertão chove menos; gado e roças perdidos | sem número | geral (C1) | OK |
| b11 | Ceará 1872: 721.686 hab. | "pouco mais de 700 mil" | Recenseamento de 1872 via Resgate/Unicamp | CONFIRMADO |
| b13 | Abarracamentos; ~113.900 abarracados em ago/1878 | "quase 114 mil" | Barros Leal via Rev. Instituto do Ceará 2008 | CONFIRMADO (acadêmica) |
| b14 | Carne estragada e farinha com cal (denúncias) | — | Agência Senado ("carne podre e farinha misturada com cal") | CONFIRMADO |
| b15 | Nov/1878: 9.844 mortes; dez/1878: 15.352 (14.491 de varíola) | "quase 10 mil"; "mais de 15 mil, quase todas de varíola" | O Povo 2020; artigo Resgate/Unicamp | CONFIRMADO |
| b16 | "Dia dos Mil Mortos" como nome | — | O Povo; Diário do Nordeste (usam o nome) | CONFIRMADO |
| b17 | Total: 150 mil–500 mil; chuva volta em 1880 | faixa | NYT 1879 (150 mil), Agência Senado/Ó Gráda (400–500 mil); Wikipedia/Agência Senado (1880) | FAIXA |
| b18 | O Besouro (RJ), 1878, fotos de retirantes de Fortaleza (J. A. Corrêa); "possivelmente a primeira experiência de fotojornalismo" | — | Embornal/UECE citando Andrade e Logatto (1994) | CONFIRMADO como leitura acadêmica ("possivelmente") |
| b20 | El Niño 1877–78 entre os mais fortes reconstruídos; nível de 82, 97 e 2015 | — | ERSSTv5 Niño 3.4, NDJ: 2015 +2,64; 1877 +2,41; 1997 +2,35; 1982 +2,14 (`dados/nino34-resumo.json`); Singh et al. 2018 ("El Niño recorde") | CONFIRMADO |
| b21 | Ar desce sobre o norte do NE no El Niño | — | longo-02 b24 (Painel El Niño/INMET) | CONFIRMADO |
| b22 | ZCIT e gradiente do Atlântico decidem a chuva de fev–mai no Ceará; Atlântico Norte recorde de quente em 1878 | — | Funceme (ZCIT, dipolo do Atlântico; Hastenrath & Heller 1977; Moura & Shukla 1981); Singh et al. 2018 (Atlântico Norte recorde em 1878) | CONFIRMADO |
| b23 | Índia 5,6–9,6 mi; China 9–13 mi | "de 5,5 a quase 10 milhões"; "de 9 a 13" | Wikipedia "Great Famine of 1876–78" (Dyson/Maharatna/Digby); Guinness/WPF | FAIXA (Davis dá mais: 12–29 mi para a Índia) |
| b24 | Singh et al. 2018 liga as fomes ao clima (El Niño + Índico + Atlântico Norte); > 50 milhões | "passam de 50 milhões" | Singh, Seager et al., J. Climate 31(23), 2018 (resumo NASA NTRS 20180007824) | CONFIRMADO como estimativa citada |
| b25 | 1877: nenhum grande açude, nenhuma ferrovia até o sertão | — | E.F. Baturité: Fortaleza–Pacatuba (1873), Baturité só em 1882 (`dados/historia.json`); Cedro começa em 1884 | CONFIRMADO |
| b26 | Sinimbu: "A solução depende da Divina Providência, e não de nós"; CPI de Silveira da Mota não aprovada | citação literal | Agência Senado (cita o discurso) | CONFIRMADO (secundária institucional) |
| b28 | Governo assume a E.F. Baturité em 1878 (Decreto 6.918, 01/06/1878), obra de socorro com retirantes; Baturité 02/02/1882; Quixadá 07/09/1891 | 1878, 1882, 1891 | `pesquisa/DADOS.md` §5; Centúrias/UECE | CONFIRMADO |
| b29 | Camocim–Sobral: Sobral em 31/12/1882 | "último dia de 1882" | `pesquisa/DADOS.md` §5 | CONFIRMADO |
| b30 | Açude do Cedro: obra 1884 (faixa 1881–1884), inaugurado 26/10/1906; Pedra da Galinha Choca; "primeiro grande açude público do país" | 1884; 22 anos; 1906 | O Povo 05/11/2026 (série "Açude Cedro 120 anos"); Diário do Nordeste ("primeiro açude do Brasil"); PL 6/2026 AL-CE ("primeiro grande açude público construído pelo Governo") | CONFIRMADO (início com faixa 1881–84; usamos 1884, o do O Povo) |
| b31 | Lenda da joia; "não há documento"; joias não foram vendidas | — | O Povo 05/11/2026 | CONFIRMADO como lenda |
| b32 | Passagens gratuitas para a Amazônia; 4.963 emigrantes no Amazonas (01/06/1877–20/08/1878) | "quase 5 mil em pouco mais de um ano" | Barboza 2015, RBH 35(70) (Falla do presidente do Amazonas); Agência Senado (passagens de graça) | CONFIRMADO |
| b33 | Seringueiros nordestinos no Acre (boliviano); Revolução Acreana; Tratado de Petrópolis 17/11/1903 | 1903 | Wikipedia (Tratado de Petrópolis); C6b | CONFIRMADO |
| b34 | Seca de 1877 como começo do caminho do Acre | "os historiadores apontam" | C6b ("tradicionalmente apontada como marco inicial") | FAIXA: formulado com "ajudou", "não sozinha" |
| b35 | Campos de 1915 e 1932; "currais do governo"; 1932: 7 campos, > 70 mil | "mais de 70 mil" | O Povo 2026 (> 73 mil); FAPESP/Kênia Rios (> 100 mil passaram) | FAIXA (usamos o piso) |
| b36 | IOCS em 1909 → DNOCS | — | IOCS (Decreto 7.619, 21/10/1909) → IFOCS 1919 → DNOCS 1945 (histórico oficial do DNOCS) | CONFIRMADO |
| b37 | Por que quase ninguém fala: mortos pobres, longe da capital, contagem falha, CPI barrada, secas repetidas | interpretação | C2, C5 | Interpretação do canal (dita como "parte da resposta") |
| b39 | El Niño 2026 muito forte; ERSSTv5 out/2026 +3,06 vs 1877 NDJ +2,41 (mesma base 1991–2020); previsão nov–jan: chuva abaixo da média em áreas do NE, sobretudo no norte | "no nível do de 1877, ou acima" | `dados/nino34-resumo.json`; INMET Painel El Niño, boletim de outubro/2026 | CONFIRMADO (formulação cautelosa: meses diferentes) |
| b40 | Funceme: cedo para prever a quadra chuvosa 2027 | — | Funceme set/2026 (`dados/hoje-2026.json`) | CONFIRMADO (imprensa citando Funceme) |
| b41 | Set/2026: seca em 96% do território do NE (Monitor de Secas) | 96% | Correio da Manhã 23/10/2026 citando o Monitor de Secas (ANA) | SÓ IMPRENSA sobre dado oficial; conferir no mapa de set/2026 na etapa 2 se quiser |
| b42 | > 1,2 milhão de cisternas (P1MC/ASA); Castanhão; transposição no CE desde 26/06/2020 | "mais de 1,2 milhão"; 2020 | ASA/Brasil de Fato 2024; IHU 2023; Diário do Nordeste | CONFIRMADO (piso conservador) |
| b43 | Seca 2012–2017: uma das piores em décadas; centenas de cidades em emergência; sem mortes em massa por fome | — | imprensa (78% dos 1.794 municípios em emergência ao menos uma vez); artigo UnB (mortalidade por fome "quase zero") | OK com formulação "uma das piores" |
| b47 | CTA: próximo vídeo = Furacão Catarina | — | pauta 16/11 (`BRIEF-lote-relevo-004-catarina`) | Se o 004 não sair, trocar a 2ª frase do b47 na etapa 2 |

## Checklist do canal (Em Relevo; bíblia de título em `../biblia-titulo.md`, formato do longo-02)
- [x] Hook com 1 lugar + 1 data + números concretos, sem resposta (b01–b03).
- [x] Barra das 4 perguntas (b06) e capítulos "PERGUNTA n/4" iguais ao longo-02; cada pergunta respondida e "A RESPOSTA" no fim volta ao hook.
- [x] Liga com o vídeo anterior (El Niño, b21) e anuncia o próximo (b47).
- [x] Nenhum número sem fonte; faixas onde as fontes divergem; lenda marcada como lenda.
- [x] Tom: sem sensacionalismo com as vítimas; fotos fortes só as menos explícitas (ver STORYBOARD).
- [x] Créditos só na descrição (nada de linha de fonte na tela; só lugar e data).
- [x] Títulos: 3 padrões diferentes, nenhum entrega a resposta (`TITULOS-THUMBS.md`).
