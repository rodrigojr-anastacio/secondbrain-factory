# Ângulo em-relevo/007-vendavais-parana-2026 · 21/11/2026

**Transcrição barrada:** em 21/11 (~23h) o YouTube respondeu "Sign in to confirm you're not a bot" a todo pedido de legenda/áudio pelo WARP (`manada.py transcrever` falhou nos 8 vídeos; testados 5 player clients do yt-dlp: web_embedded, mweb, android_vr, ios, tv_simply). A busca segue funcionando. Por isso o consenso abaixo foi montado com **títulos, capítulos e descrições** (Data API `videos.list`) + o que o nosso 001 já disse, e é **provisório**. Atualização de 22/11 ~00h: o player voltou e a legenda deu 429; o Whisper transcreveu 2 (`ref/manada-x_xE2HyxQE0.txt` Além do Mapa e `ref/manada-GSSCfXMD4wQ.txt` ALDO, que confirmam o consenso abaixo: muro dos Andes, rios voadores, choque de massas, "2º corredor", "o endereço que se repete"); o roteiro do nosso 001 entrou como referência (`ref/nosso-001-bG6-E4qjXYc.txt`). Detector: 14/100 (001), 3 e 1 (manada). as transcrições entram em `ref/manada-*.txt` quando o bloqueio cair, e o detector (`tools/similaridade_roteiro.py`) roda contra elas na etapa 2, **antes da voz** (pendência no `ETAPA1-PRONTA.md`).

## A manada (vídeos de mais views do tema; `ref/manada.json`, `embalagem/refs.csv`)
| id | canal | views | idioma | dur. | recorte (título / capítulos) |
|---|---|---|---|---|---|
| X3FaimD9FbQ | Ric RECORD Paraná | 628 mil | pt | 16:23 | Rio Bonito do Iguaçu 2025: reportagem do estrago |
| ag6pIQ4m_7w / SVCC5nmbMEM | Band Paraná / Band Jornalismo | 586 / 455 mil | pt | 19:27 / 6:51 | Rio Bonito: cidade devastada, vítimas |
| GOC2Dzxr82g | Band Paraná | 1,03 mi | pt | — | temporal em Toledo (set/2026): imagens de destruição |
| 06PHZHtdeQM | Brasil Urgente | 520 mil | pt | — | **20/11/2026**: "Dois tornados atingem o Paraná e deixam 80 mil imóveis sem energia" |
| 9w1f8S44OpY | g1 (JH) | 283 mil | pt | 4:46 | "Brasil tem o 2º maior corredor de tornados do mundo" |
| Kzo1yKN-O3w | Brasil Urgente | 205 mil | pt | 8:46 | "Por que tornados e ciclones estão atingindo o Centro-Sul?" (frente fria + ciclone; "mais de 100 tornados no ano") |
| GSSCfXMD4wQ | ALDO - Além do Óbvio | 115 mil | pt | 10:20 | "Tornados no Brasil: a verdade que ninguém conta": o que é tornado; EUA 1.200/ano; corredor entre Andes, Amazônia e ar frio; 28 tornados em 2024; sequência de nov/2026; 524 registros do Prevots |
| iYLaJe3jMGE | Tornado Flix | 108 mil | pt | 19:18 | "O Corredor dos Tornados no Brasil e porque Você não está Seguro" |
| x_xE2HyxQE0 | Além do Mapa | 80 mil | pt | 14:20 | "Tem Algo Estranho Acontecendo no Sul do Brasil": Andes e choque de massas; Xanxerê; ciclones/furacão/enchentes; corredor; Chapecó; El Niño; "o endereço do choque" |
| TfTiDfsKK04 | Prof. Rogerdautry | 56 mil | pt | 18:56 | "O CORREDOR DE TORNADOS NO BRASIL: 524 Casos": mapa de ocorrências; rios voadores, ar polar e cisalhamento; supercélulas; ranking de cidades; radar Doppler |
| e135HFW4TGU | Prof. Rogerdautry | 10 mil | pt | 14:47 | "MÁQUINA DE TORNADOS": 8 tornados em 9 meses; cicatriz do F4 de Rio Bonito; anatomia da supercélula; "2º maior corredor"; choque de massas; Fujita; histórico desde 1927; El Niño e aquecimento |
| TVy9lrcW00U / j7jjL-fy4EA | Prof. JeanGrafia | 42 / 13 mil | pt | 12:59 / 9:54 | como se forma um tornado; tornado × furacão; "por que o Sul/Paraná tem condições ideais"; comparação com os EUA |
| r2m4ucK0xVc | William Batista TV | 12 mil | pt | 22:33 | entrevista Simepar (Piraí do Sul): "Paraná está na rota dos tornados?" |
| 5UTQ4KrtVGc / lsEA9tGMFQQ | PBS Terra / Vox | 3,0 / 2,2 mi | en | 11:42 / 5:51 | Tornado Alley (EUA) se mudando; por que os EUA têm tantos tornados |
| — (nosso) bG6-E4qjXYc | Em Relevo 001 | — | pt | 10:23 | 7 tornados em 6 dias; Amazônia + jato de baixos níveis + Andes + frente fria + cisalhamento; supercélula/mesociclone; "2ª região do mundo"; NASA tempestades intensas; El Niño; Fujita; Rio Bonito como F4; o que fazer |

## Consenso da manada (o que NÃO fazer) — provisório
- **Hook repetido:** imagem/flagrante do tornado ou do estrago + número de vítimas/casas ("seis mortos", "90% da cidade", "80 mil sem energia"); nos explicativos, "o Brasil tem o 2º maior corredor de tornados do mundo".
- **Sequência de beats dos explicativos:** o que é tornado → como nasce a supercélula → corredor da América do Sul (Andes + Amazônia/rios voadores + ar frio da Argentina) → "2º lugar do mundo" / Brasil × EUA → Fujita → casos (Rio Bonito, Xanxerê, Chapecó, Maringá) → El Niño/aquecimento → "não estamos seguros".
- **Anedotas/números repetidos (proibidos como cena principal):** "2º maior corredor do mundo"; EUA ~1.200 tornados/ano; 524 casos do Prevots / 581 da UEPG; rios voadores; supercélula girando/mesociclone; Rio Bonito "90% da cidade" e vítimas; Fujita explicada degrau por degrau; El Niño "pode aumentar tornados".
- **Também proibido por ser o nosso 001:** a explicação continental completa (Amazônia → jato → Andes → frente fria → cisalhamento → rolo de ar em pé). Aqui: 1 frase de recapitulação + convite ao 001.
- **Consenso da cobertura de 20/11 (TV):** minuto a minuto, vídeo de celular do funil em Foz, telhados da Vila Yolanda, "80 mil sem energia", entrevista com morador. Nada disso como cena; usamos só os números oficiais.

## Ângulos propostos
1. **O rastro de uma tarde no mapa** — reconstruir o 20/11 como uma linha de rajadas medidas (14 estações, hora a hora) sobre o relevo 3D e o satélite, e responder **por que o temporal entra pelo oeste/sudoeste do Paraná e chega ao Norte Pioneiro à noite**: berçário de tempestades a oeste (C1–C3), deslocamento sudoeste → nordeste medido (N1), escada do relevo com a ponta baixa e quente a oeste (R1–R2). Fecha com o "novamente": as trilhas de Rio Bonito 2025 e de novembro de 2026 no mesmo mapa + o novembro encharcado (N3, B6, B7). · Paga a demanda (quem busca "vendaval Paraná" vê o 20/11 inteiro, com números oficiais) · cabe na forma (pergunta + mapa + capítulos) · fontes: Simepar/AEN, Copel, Defesa Civil, NOAA GOES-19, NASA IMERG, Zipser 2006, UFSM 2025, laudo de Rio Bonito · **ninguém da manada faz**: nenhum vídeo (nem o nosso 001) usa as horas das estações como dado, mede a velocidade do temporal, mostra o satélite do dia nem o relevo do Paraná como escada.
2. **Novembro de 2026, o mês dos três temporais** — calendário 2/11 → 7/11 → 20/11 com chuva IMERG acumulada e anomalia, calor e El Niño. · Paga a demanda, mas vira "quente" puro e repete o El Niño do 001 e da manada; perde validade em semanas.
3. **Por que Foz e Manoel Ribas tiveram tornado e Cascavel só vento** — cisalhamento e células isoladas × linha. · Interessante, mas sem dado público suficiente (radar do Simepar sem licença clara, laudo ainda não publicado): promessa incumprível hoje.

## Escolhido: 1 — o rastro de uma tarde
Justificativa: é o único que (a) responde uma pergunta que continua valendo depois da semana ("por que o oeste primeiro?"), (b) usa só dado público medido e cria dado nosso (N1–N3), (c) é geográfico (relevo + posição no continente), que é a promessa do canal, e (d) não repete o 001. O ângulo 2 entra como o capítulo 5 (o "novamente"), não como tese.

## Anedotas e dados próprios previstos (fora da manada) — meta da bíblia ≥ 40%
| anedota/dado | fonte | aparece em título/capítulo da manada? |
|---|---|---|
| A reta das rajadas: 14 estações, r² 0,98, ~430 km em ~7 h, ~70 km/h | N1 (Simepar E4) | não |
| Capanema 13h45 → Cornélio Procópio 20h15, 98,3 km/h o maior do dia | E4, N2 | não (a TV deu "rajadas de até 98 km/h" sem a sequência) |
| GOES-19 a cada 20 min: o aglomerado às 9h a oeste, a faixa às 20h | E9 | não |
| Previsão do Simepar: baixa pressão sobre o Paraguai, oeste e sudoeste primeiro | E1 | não |
| NASA/TRMM: as tempestades mais fortes do planeta a leste dos Andes (frase do release) | C1 | o 001 citou "entre as mais intensas"; manada não — usar a frase nova e o mapa do TRMM, não a ideia do corredor |
| UFSM 2025: sudoeste do PR no setor de mais tornados do Sul | C3 | não |
| Escada do relevo: ~120 m em Foz, ~800 m em Cascavel, Serra do Mar a leste (perfil SRTM nosso) | R1, R2, N4 | não |
| Laudo de Rio Bonito: supercélula de 270 km a ~80 km/h, trilha de oeste para leste — mesma ordem de velocidade do 20/11 | B1 + N1 | Rio Bonito aparece, mas pela tragédia; o rastro/velocidade não |
| Chuva de 1–20/11 ~+61% (IMERG) | N3 | não |
| 33 estações > 30 °C em 12/11 | B6 | não |
| 353.849 sem luz às 20h02 (o pico, não os "80 mil" da TV) | E5 | parcial (TV deu o número da manhã) |
Cota estimada: ~9 de 11 dados centrais fora da manada (~80%).

## Ordem prevista dos capítulos (≠ da manada) e onde o ângulo aparece no hook
Hook (0:00–0:35): Capanema 13h45 81,7 km/h → Cornélio Procópio 20h15 98,3 km/h, 423 km depois; dois tornados no caminho; terceira vez em 20 dias → "Por que o temporal entra pelo oeste do Paraná? E por que voltou?" → "a resposta está no mapa".
1 · O RASTRO DE UMA TARDE (as estações viram uma reta; velocidade) → 2 · DE ONDE ELE VEM (o satélite das 9h; Paraguai; a leste dos Andes; UFSM) → 3 · A ESCADA DO PARANÁ (relevo; ponta baixa e quente a oeste; por que de noite no norte) → 4 · O MESMO CAMINHO (Rio Bonito 2025, Maringá e 07/11/2026 sobre o mapa) → 5 · O NOVEMBRO ENCHARCADO (IMERG +61%, calor, El Niño, com cautela) → A RESPOSTA → fecho útil.
A manada começa no estrago/vítima e explica o continente; nós começamos em **duas horas e dois números de estação** e explicamos **o Paraná por dentro**.
