# Storyboard: Em Relevo 007 (vendavais no Paraná de 20/11/2026: por que o temporal entra pelo oeste)

Etapa 1 (22/11/2026). Fonte: `shared/storyboard.py` → `shared/storyboard.json`, `shared/cenas.json` (regenere com `python3 shared/storyboard.py`). Duração estimada **~9:54**; 46 blocos; ~153 eventos visuais (~15/min, alvo 2–4 s por evento); tempo por estilo: A 247 s · B 303 s · G 44 s. **Zero imagem de IA**; 10 mídias reais distintas; custo de imagem US$ 0.

## Linguagem visual (a do 005/006, visual v2)
- **A = satélite** (relevo SRTM do Paraná via Terrain Tiles + cor natural) para lugar e impacto; **B = relevo editorial** (navy) para dado, reta e rótulo; **G = satélite meteorológico** (GOES-19 infravermelho e NASA IMERG sobre o relevo).
- Câmera sempre em movimento; cada evento amarrado à palavra falada (gatilho) na etapa 2. Legenda só LUGAR · DATA; créditos só na descrição. Exagero vertical sempre com 'ILUSTRATIVO'.

## Assinaturas e fio condutor
1. **A linha das rajadas** (b05–b09, b13, b27, b33, b42–b43): 16 pontos do Simepar que acendem na hora do pico; 14 se ligam numa reta coral sudoeste → nordeste; Paranaguá e Cambará ficam em cinza (outras células). Gráfico hora × distância no b08 (dado nosso, r² 0,98).
2. **A escada do Paraná** (b04, b20–b26, b41 e a Thumb A): o estado em bloco 3D visto de lado, perfil SRTM oeste → leste com régua de altitude; a seta da tempestade encosta na ponta baixa.
3. **Duas linhas lado a lado** (b03, b30–b33, b43): a reta de 2026 (coral) e o rastro de Rio Bonito 2025 (amarelo, do laudo).

## Peças novas (prioridade; simplifique de baixo para cima se faltar tempo)
1. **Pinos que acendem + reta + relógio** (dados/rajadas-2026-11-20.json; refazer a regressão N1 com as coordenadas finais).
2. **GOES-19 sobre o relevo:** baixar ABI-L2-CMIPF canal 13 de 20/11 12–23 UTC do bucket público `s3://noaa-goes19`, reprojetar para lon/lat no bbox do PR (+ Paraguai/Misiones) e usar como camada (paleta infravermelho realçado). Prévia jpg do STAR em `dl/goes19/`.
3. **Bloco 3D do Paraná de lado** com perfil SRTM (N4) e régua; mesmo still serve à Thumb A.
4. **Camadas IMERG** (dados/nasa/pr-nov-1a20*.png) — já geradas.
5. **Rastro de Rio Bonito 2025** desenhado a partir do laudo (municípios em ordem) + Sentinel-2 (Commons, atribuição Copernicus).
6. Gráfico hora × distância (b08), termômetros (b23, b25), calendário (b35), barras por estação (b40), cards: componentes existentes.

## Mídias reais
| arquivo | blocos | licença/crédito (descrição) |
|---|---|---|
| `dados/nasa/pr-nov-1a20-anom-anomalia-camada.png` | b37 | NASA GPM IMERG (GES DISC), domínio público |
| `dados/nasa/pr-nov-1a20-camada.png` | b37 | NASA GPM IMERG (GES DISC), domínio público |
| `dl/fotos/aen-copel-2026-11-07-78655.jpg` | b12 | Copel/AEN, CC0 |
| `dl/fotos/aen-copel-2026-11-07-78659.jpg` | b45 | Copel/AEN, CC0 |
| `dl/fotos/aen-maringa-2026-11-04-defesacivil.jpg` | b35 | Defesa Civil/AEN (galeria CC0; conferir legenda) |
| `dl/fotos/commons-Sentinel-2_Rio_Bonito_scar_labelled_no_m` | b30 | Contains modified Copernicus Sentinel data 2025 (via Wikimedia Commons) |
| `dl/fotos/commons-rb-03-orig.jpg` | b31 | Ari Dias/AEN, CC0 |
| `dl/fotos/dpu/rb-telhado-54944696133-orig.jpg` | b34 | DPU (Defensoria Pública da União), CC0 |
| `dl/goes19/b13/20263241200_GOES19-ABI-ssa-13-1800x1080.jpg` | b15 | NOAA/NESDIS (GOES-19), domínio público |
| `dl/goes19/b13/20263242300-3600.jpg` | b15 | NOAA/NESDIS (GOES-19), domínio público |

## Plano por bloco
| bloco | t est. | estilo | plano | camadas |
|---|---|---|---|---|
| b01 | 0:00 | A | Abre baixo sobre o rio Iguaçu na fronteira (Argentina à esquerda, Brasil à direita), fim de tarde nublado; a câmera desliza até Capanema. Um pino coral acende na palavra 'rajada' e pulsa. | cartão CAPANEMA (PR) · 20 NOV 2026 · 13H45 · na palavra 'oitenta': ficha 81,7 KM/H sobe do pino |
| b02 | 0:10 | A | A câmera sobe e voa ~420 km para nordeste por cima do estado até Cornélio Procópio; um segundo pino acende lá. No meio do voo, dois pinos menores piscam: FOZ e MANOEL RIBAS (ícone de redemoinho simples, sem foto). | régua 423 KM · 6H30 entre os dois pinos · ficha 98,3 KM/H em Cornélio Procópio · pinos TORNADO F1 · FOZ DO IGUAÇU / TORNADO F1 · MANOEL RIBAS |
| b03 | 0:24 | A | Mesmo enquadramento do estado, mas outro dia: uma linha fina de 2025 aparece no centro-sul (Quedas do Iguaçu → Cantagalo), em amarelo pálido, e a câmera faz um leve zoom sobre Rio Bonito do Iguaçu. | cartão RIO BONITO DO IGUAÇU · 7 NOV 2025 · linha tracejada 2025 |
| b04 | 0:31 | B | Câmera recua até o Paraná inteiro em relevo editorial; uma seta grande entra pela borda oeste (a mesma da Thumb A). | pergunta em tipografia: POR QUE O TEMPORAL ENTRA PELO OESTE DO PARANÁ? · subtítulo: DE NOVO PELO MESMO LADO? |
| b05 | 0:38 | B | ASSINATURA: o mapa editorial do PR com 16 estações do Simepar como pontos apagados; um relógio no canto (13:00 → 21:00) começa a correr. | aba 1 · O RASTRO DE UMA TARDE · relógio 13:00 · pontos apagados = estações |
| b06 | 0:45 | B | Os pontos acendem um a um na hora do pico, em sincronia com a fala (Capanema → Santa Helena → Cascavel → Campo Mourão → Maringá → Londrina → Cornélio Procópio) e os demais da fila no intervalo; cada um deixa um número pequeno em km/h. | relógio corre até 20:15 · rótulos com hora e km/h (dados/rajadas-2026-11-20.json) · na palavra 'linha': a reta coral liga os pontos de SW para NE |
| b07 | 1:03 | B | Dois pontos acendem fora da ordem e fora da reta, em cinza: PARANAGUÁ (litoral) e CAMBARÁ (Norte Pioneiro); a câmera passa por eles e volta para a reta. | rótulos PARANAGUÁ 13H15 · CAMBARÁ 14H (cinza) · etiqueta OUTRAS CÉLULAS · a reta coral volta a brilhar: LINHA PRINCIPAL |
| b08 | 1:15 | B | Gráfico limpo sobre o mapa escurecido: eixo horizontal = distância ao longo da reta (0 → 430 km), eixo vertical = hora (13h → 21h); os 14 pontos caem quase sobre uma linha reta (dado nosso, N1). | gráfico HORA × DISTÂNCIA (14 estações) · número ~430 KM · ~70 KM/H · ícone de carro na estrada ao lado do 70 KM/H |
| b09 | 1:32 | A | A faixa de tempestade aparece como uma banda translúcida que desliza sobre o relevo ao longo da reta, de Capanema a Cornélio Procópio, em ~5 s (acelerado). | etiqueta 6H30 · 13H45 → 20H15 |
| b10 | 1:40 | A | A banda passa por Foz do Iguaçu; zoom até a cidade (satélite, cor natural); pino na Vila Yolanda. Depois a câmera corre para Manoel Ribas (zona rural, campos). | pino VILA YOLANDA · FOZ DO IGUAÇU · ~15H · ficha TORNADO F1 · 117–180 KM/H (ESTIMADO) · pino MANOEL RIBAS · ~18H · F1 |
| b11 | 1:58 | B | Contador sobe de 0 a 353.849 sobre o mapa do estado que escurece (lâmpadas se apagando por região); depois, 9 municípios se destacam em coral. | contador 353.849 IMÓVEIS SEM ENERGIA · 20H02 · ficha 9 MUNICÍPIOS · 249 IMÓVEIS DANIFICADOS · Foz destacada: QUASE METADE |
| b12 | 2:14 | A | Foto CC0 de árvore caída em temporal deste novembro (Copel/AEN, 07/11) como respiro, enquanto os números de Foz aparecem; depois volta ao mapa com as regiões da Copel e o Oeste em destaque. | ficha FOZ: ~50 ÁRVORES · LONAS PARA ~200 FAMÍLIAS · ficha OESTE: 26,8 MIL SEM LUZ NA MANHÃ SEGUINTE |
| b13 | 2:31 | B | A reta coral de novo, agora pintada em degradê: laranja (tarde) no oeste, azul-escuro (noite) no norte. | rótulos TARDE / NOITE ao longo da reta · ícone de relógio com interrogação (loop: pago no b27) |
| b14 | 2:39 | G | A câmera sobe e gira para oeste até mostrar Paraguai, Misiones e o PR; uma baixa pressão desenhada como um 'B' discreto sobre o Paraguai. | aba 2 · DE ONDE ELE VEM · rótulo BAIXA PRESSÃO · PARAGUAI (previsão do Simepar, 19/11) · setas suaves OESTE · SUDOESTE |
| b15 | 2:53 | G | Sequência real do GOES-19 (canal 13, infravermelho, 9h → 20h, a cada 20 min) sobreposta ao relevo, em ~6 s: o aglomerado nasce a oeste e se estica sobre o estado; relógio no canto. | relógio 9H → 20H (hora de Brasília) · rótulo GOES-19 · 20 NOV 2026 |
| b16 | 3:08 | A | A câmera recua até o continente inteiro: Andes à esquerda, a região entre Paraguai, norte da Argentina e Sul do Brasil se acende como uma mancha quente suave (sem números), a leste dos Andes. | rótulo A LESTE DOS ANDES · rótulo SATÉLITE TRMM · NASA · 7 ANOS DE DADOS |
| b17 | 3:25 | B | Duas silhuetas simples de continente lado a lado (América do Norte e América do Sul) com a faixa de latitudes médias destacada; ícones de 'complexo de tempestade' iguais nas duas. | etiqueta COMPLEXOS DE TEMPESTADE · LATITUDES MÉDIAS · sinal = entre os dois lados |
| b18 | 3:35 | A | Plano rápido de recapitulação: três setas finas e esmaecidas (Amazônia → sul; Andes como parede; ar frio do sul) sobre o continente, e um selo do nosso vídeo 001. | selo VÍDEO NO CANAL: TORNADOS DO SUL · seta grande final aponta: A OESTE DO PARANÁ |
| b19 | 3:51 | B | Mapa do Sul com a faixa de maior frequência de tornados do levantamento da UFSM (norte do RS, oeste de SC, sudoeste do PR) em coral translúcido; a borda oeste do PR acende. | etiqueta UFSM · 310 TORNADOS REGISTRADOS NO SUL · rótulo O LADO DE ONDE O TEMPORAL CHEGA |
| b20 | 4:04 | A | SEGUNDA ASSINATURA: o Paraná em bloco 3D visto de lado, de leste (mar, à direita) para oeste (rio Paraná, à esquerda), exagero vertical marcado 'ilustrativo' — o mesmo bloco da Thumb A. | aba 3 · A ESCADA DO PARANÁ · selo ILUSTRATIVO · ALTURA EXAGERADA |
| b21 | 4:09 | B | Régua de altitude vai marcando cada degrau na fala: litoral 0 m → Pico Paraná 1.877 m → Curitiba ~930 m → Guarapuava > 1.000 m (perfil SRTM N4). | rótulos com altitude: LITORAL 0 · PICO PARANÁ 1.877 M · CURITIBA ~930 M · GUARAPUAVA > 1.000 M |
| b22 | 4:27 | B | Continuação do perfil para oeste: os degraus descem até o rio Paraná; Cascavel e Foz marcados. | rótulos CASCAVEL ~780 M · FOZ DO IGUAÇU ~160 M · seta da tempestade chegando pela esquerda, na ponta baixa |
| b23 | 4:38 | B | Termômetro simples ao lado do perfil: a cor do ar fica mais quente à medida que o perfil desce para oeste. | etiqueta ~0,6 °C A CADA 100 M (MÉDIA) · degradê azul (alto) → laranja (baixo) |
| b24 | 4:53 | A | Mapa do PR com o norte em tom quente; ficha da previsão. | ficha PREVISÃO 19/11: > 30 °C NO NORTE · ficha CALOR + UMIDADE = ALIMENTO DA TEMPESTADE |
| b25 | 5:06 | B | Dois termômetros lado a lado: CURITIBA ~930 M e FOZ ~160 M, com a diferença calculada. | DIFERENÇA ~770 M → ~4 A 5 °C MAIS QUENTE EM FOZ (SÓ PELA ALTITUDE) |
| b26 | 5:21 | A | Volta ao bloco 3D: a seta da tempestade encosta na ponta baixa do oeste; um ícone de ímã riscado (a ladeira não puxa). | rótulo A LADEIRA NÃO PUXA · rótulo QUEM ELA ENCONTRA PRIMEIRO: A PONTA BAIXA E QUENTE |
| b27 | 5:32 | B | A reta coral com o relógio (paga o loop do b13): um ponto anda pela reta a 70 km/h; quando chega ao norte, o céu do mapa escurece (noite). | relógio 13H45 → 19H30 (LONDRINA) → 20H15 (CORNÉLIO PROCÓPIO) · ficha 70 KM/H |
| b28 | 5:47 | A | Zoom em Cornélio Procópio, à noite (relevo escurecido, luzes da cidade em pontos); a ficha 98,3 sobe. | ficha 98,3 KM/H · 20H15 · O MAIOR DO DIA · rótulo QUASE NA SAÍDA |
| b29 | 6:00 | A | O mesmo mapa, dia claro; o cartão de data troca de 2026 para 2025. | aba 4 · O MESMO LADO · cartão 7 NOV 2025 |
| b30 | 6:04 | A | A linha da supercélula de 2025 é desenhada sobre o relevo; depois o rastro do tornado (75 km) se pinta de Quedas do Iguaçu a Cantagalo, de oeste para leste; a imagem real do Sentinel-2 da cicatriz entra por 2 s. | ficha SUPERCÉLULA ~270 KM · ~80 KM/H (LAUDO SIMEPAR) · rótulos QUEDAS DO IGUAÇU → CANTAGALO · 75 KM |
| b31 | 6:22 | A | Zoom em Rio Bonito do Iguaçu; foto aérea CC0 em plano bem largo (cidade inteira, sem zoom em entulho, sem pessoas) por 2 s. | ficha F4 · UM DOS MAIORES DO PR EM 30 ANOS (SIMEPAR) |
| b32 | 6:33 | A | A linha da mesma supercélula continua para leste e um segundo rastro aparece em Candói/Entre Rios (Guarapuava). | rótulos CANDÓI · ENTRE RIOS (GUARAPUAVA) · 44 KM · seta UMA DIREÇÃO SÓ |
| b33 | 6:45 | B | ASSINATURA de volta: a reta coral de 2026 e a linha amarela de 2025 lado a lado no mesmo mapa; as duas setas apontam para o mesmo lado. | rótulos 2025 · 2026 · fichas 80 KM/H · 70 KM/H · rótulo A MESMA ENTRADA: O OESTE |
| b34 | 7:02 | B | A borda oeste/sudoeste do PR acende como uma 'porta' (faixa coral), virada para o Paraguai/Argentina. | rótulo MESMO LADO ≠ MESMA CIDADE · rótulo PORTA DE ENTRADA: OESTE E SUDOESTE |
| b35 | 7:11 | A | Calendário de novembro de 2026 no canto; dia 7 acende com o contador 493 mil; depois um contador de tornados do ano no PR chega a 15 (pinos discretos no mapa, sem fotos). | calendário NOV 2026: 7 · 20 · contador 493 MIL SEM LUZ · MAIOR DO ANO · contador 15 TORNADOS NO PR EM 2026 (SIMEPAR, ATÉ 6/11) |
| b36 | 7:30 | B | Pergunta em tipografia sobre o mapa do PR. | aba 5 · POR QUE TANTO AGORA · pergunta POR QUE TANTA COISA NUM MÊS SÓ? |
| b37 | 7:34 | G | Camada real NASA IMERG de 1–20/11 sobre o relevo do PR (fade-in com a câmera em movimento); depois a camada de anomalia. | ficha ~175 MM (MÉDIA NO PR) × ~108 NORMAIS · ficha MAIS DE 60% ACIMA · rótulo 1 – 20 NOV 2026 |
| b38 | 7:49 | B | Mapa das estações do Simepar com pontos que ficam laranja acima de 30 °C (33 deles); Cerro Azul destacado. | ficha 12 NOV: 33 ESTAÇÕES > 30 °C · pino CERRO AZUL · 35,1 °C |
| b39 | 8:01 | B | Pacífico equatorial pequeno no canto com a língua quente do El Niño (como no 002), e uma seta discreta até o Sul; a porta oeste do PR continua acesa. | ficha EL NIÑO MUITO FORTE (SIMEPAR) · rótulo AUMENTA AS CHANCES · NÃO FABRICA CADA TEMPESTADE |
| b40 | 8:16 | B | Barras simples por estação do ano (sem números inventados: só qual é a maior), com o inverno em destaque. | etiqueta UFSM · MÁXIMO DE TORNADOS NO SUL: INVERNO · rótulo NOVEMBRO 2026: CALOR + CHUVA DE SOBRA |
| b41 | 8:33 | A | O Paraná em relevo, vista da Thumb A, com a seta entrando pelo oeste. | aba A RESPOSTA · pergunta POR QUE PELO OESTE? |
| b42 | 8:37 | A | As três camadas acendem uma a uma: (1) o berçário a oeste (mancha quente do b16), (2) a reta sudoeste → nordeste com 70–80 km/h, (3) a ponta baixa e quente (degradê do b23). | fichas 1 · BERÇÁRIO A OESTE · 2 · ANDA DE SW PARA NE · 3 · PONTA BAIXA E QUENTE |
| b43 | 8:58 | B | As duas linhas (2026 coral, 2025 amarela) lado a lado, fixas; texto final. | rótulos CAPANEMA → CORNÉLIO PROCÓPIO (2026) · QUEDAS DO IGUAÇU → CANTAGALO (2025) · frase UM ANO DE DISTÂNCIA, A MESMA DIREÇÃO |
| b44 | 9:11 | B | Card de serviço (paleta do canal), celular simples com um alerta. | card ALERTAS DA DEFESA CIVIL: SMS COM O SEU CEP PARA 40199 · etiqueta O AVISO SAIU ANTES (SIMEPAR) |
| b45 | 9:26 | A | Foto CC0 de poste/árvore caídos (Copel/AEN, 07/11) como fundo esmaecido do conselho. | card LONGE DE ÁRVORES, POSTES E PLACAS |
| b46 | 9:34 | B | Encerramento: miniatura do vídeo 001 (tornados do Sul), logo do canal, mapa do PR com o oeste e o norte destacados ('manda para quem mora aí'). | card do vídeo 001 · logo EM RELEVO |

## Sensibilidade
Sem foto de pessoa, resgate, ferido ou TV; Rio Bonito por rastro, laudo e plano largo/telhado sem pessoas; vítimas não são citadas; fotos de 07/11 com legenda do dia certo (não fingem ser de 20/11); foto do telhado com legenda neutra.
