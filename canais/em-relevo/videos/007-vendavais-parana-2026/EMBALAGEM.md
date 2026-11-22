# Embalagem em-relevo/007-vendavais-parana-2026 · versão r1 · 21/11/2026
Tema: o temporal de 20/11/2026 no Paraná como caso; a pergunta perene "por que o temporal entra pelo oeste do Paraná (e por que voltou tanto)" · idioma pt-BR · duração-alvo ~10 min (BRIEF) · cota gasta: ~40 unidades da Data API (`videos.list`, `channels.list`, `playlistItems`); **search.list: 0** · mosaicos: `embalagem/mosaico.jpg` (top do tema por views + 4 nossos), `mosaico-explica.jpg` (explicativos do tema), `mosaico-padroes.jpg` (referências de padrão), `vizinhas-em-relevo.jpg` (grade do canal 003–006) · prévias: `previa-b-goes-1280.jpg`/`previa-b-320.jpg`, `previa-c-araucaria-1280.jpg`/`previa-c-320.jpg` · medianas: `medianas.json` (script) + `medianas-extra.json` (calculadas à mão: últimos ≤ 30 longos, ≥ 3 min).

## Pesquisa (resumo)
279 vídeos em `refs.csv` (11 termos pt). Top do tema (≤ 400 d), views e ×mediana de 21/11/2026:
| link | canal | views | data | mediana | ×med | padrão de título | padrão de thumb |
|---|---|---|---|---|---|---|---|
| [GOC2Dzxr82g](https://youtu.be/GOC2Dzxr82g) | Band Paraná | 1.032.470 | 30/09/2026 | 1.829 | 564,7× | notícia ("Imagens mostram destruição…") | cena-acao (aéreo do estrago) + tarja TV |
| [06PHZHtdeQM](https://youtu.be/06PHZHtdeQM) | Brasil Urgente | 520.084 | 21/11/2026 | 15.661 | 33,2× | notícia de 20/11 ("Dois tornados atingem o Paraná…") | foto do funil + tarja TV |
| [N9U-HFY5XRE](https://youtu.be/N9U-HFY5XRE) | De olho no céu | 513.910 | 02/11/2025 | 3.531 | 145,6× | "Três SUPER CÉLULAS em 6 HORAS!" (número + tempo) | cena-acao (supercélula real, sem texto) |
| [kUTyeaHS98M](https://youtu.be/kUTyeaHS98M) | Ric RECORD Paraná | 359.080 | 04/11/2026 | 2.497 | 143,8× | "Tornado F2: entenda…" | cena-acao (árvores na tempestade) + "ÁRVORES ARRANCADAS PELA RAIZ" |
| [9w1f8S44OpY](https://youtu.be/9w1f8S44OpY) | g1 | 283.165 | 10/08/2026 | 31.138 | 9,1× | "Brasil tem o 2º maior corredor…" | funil + "Corredor de tornados" |
| [Kzo1yKN-O3w](https://youtu.be/Kzo1yKN-O3w) | Brasil Urgente | 205.021 | 05/11/2026 | 15.661 | 13,1× | "Por que tornados e ciclones estão atingindo o Centro-Sul do país?" | documento-evidencia (imagem de satélite real dominando) + tarja TV |
| [x_xE2HyxQE0](https://youtu.be/x_xE2HyxQE0) | Além do Mapa | 80.398 | 06/11/2026 | 1.716 | 46,9× | "Tem Algo Estranho Acontecendo no Sul do Brasil" | mapa-lugar (América do Sul, Sul em vermelho, funil, seta) |
| [unBF8Vnsx8Q](https://youtu.be/unBF8Vnsx8Q) | Ric RECORD Paraná | 71.521 | 23/07/2026 | 2.497 | 28,6× | "Paraná teve 6 tornados em apenas 3 dias…" (número + tempo) | funil + tarja |
| [B3oYl6QkVHs](https://youtu.be/B3oYl6QkVHs) | Diego San Araujo | 352.593 | — | — | 5,0× | ao vivo ciclone | documento-evidencia (painéis de radar reais) |
| [j7jjL-fy4EA](https://youtu.be/j7jjL-fy4EA) | Prof. JeanGrafia | 13.209 | 08/11/2025 | 26.515 | **0,5×** | "Tornado no Paraná: por que a região SUL está na zona de risco?" | rosto + funil |

**Colisões (não repetir):** "corredor de tornados" (g1, Tornado Flix, Rogerdautry 524 casos, Band "2º principal corredor", ALDO, Além do Mapa); "a verdade que ninguém conta" (ALDO); "o que está acontecendo / tem algo estranho no Sul" (Além do Mapa, nosso 001); "Paraná na rota dos tornados" (William Batista, Rogerdautry "nova rota"); "por que a região SUL está na zona de risco" (JeanGrafia, 0,5×: "por que + tornado + Sul" genérico rende pouco — nenhum título nosso usa "tornado" nem "Sul/zona de risco"); notícia "dois tornados atingem o Paraná" (Brasil Urgente, Terra, g1). Nenhum título do tema fala em **oeste**, em **7 horas/atravessou o estado** ou em **3 temporais em 20 dias**.
**Thumbs do tema:** quase todas = foto/vídeo do **funil** ou do **estrago**, escura e cinzenta, com **tarja de TV** (Brasil Urgente, Band, Ric, CNN, g1); explicativos = funil + palavra ("CORREDOR") ou rosto assustado. Evitar: funil, céu cinza genérico, tarja, rosto. **Nossa grade** (`vizinhas-em-relevo.jpg`): 9 de 12 = mapa escuro + número/palavra grande; as 3 do 006 já fugiram (bloco 3D claro, Landsat, foto de solo sem texto).

## Promessa
- **Frase:** no mapa (estações, satélite e relevo 3D), ver o caminho que o temporal de 20/11 fez pelo Paraná — de Capanema às 13h45 a Cornélio Procópio às 20h15 — e entender por que os temporais entram pelo oeste do estado e por que voltaram três vezes em 20 dias.
- **Material que a sustenta** (BRIEF §Fontes; `pesquisa/FATOS.md`): E4 (16 rajadas com hora, Simepar), N1/N2 (reta sudoeste → nordeste, r² 0,98, ~430 km em ~7 h, ~70 km/h), E2 (2 tornados F1, Foz ~15h e Manoel Ribas ~18h), E5 (353.849 sem luz às 20h02), E1 + E9 (baixa pressão sobre o Paraguai; GOES-19 baixado, 48 quadros do dia), C1–C3 (tempestades mais intensas a leste dos Andes; sudoeste do PR no setor de mais tornados do Sul), R1–R2 + N4 (escada do relevo, Foz ~120 m × Cascavel ~800 m), B1–B4 (Rio Bonito 2025 trilha de oeste para leste a ~80 km/h; Maringá F2 02/11; 493,1 mil sem luz 07/11), N3/B6/B7 (novembro +61% de chuva, 35 °C, El Niño muito forte).
- **Onde o roteiro paga:** hook (0:00–0:35): Capanema 13h45 → Cornélio Procópio 20h15, os dois tornados no caminho, "a terceira vez em 20 dias" (2/11, 7/11, 20/11) e a frase-âncora; 1º minuto: as estações acendem no mapa e viram uma reta (atravessou o estado em ~7 h). O vídeo inteiro sustenta: cada capítulo é uma camada da mesma resposta (de onde vem → por que pelo oeste → por que de novo).

## Título 1 · padrão "Por que [LUGAR] [anomalia]?" (controle da bíblia) · 46 caracteres
"Por que o temporal entra pelo OESTE do PARANÁ?"
Referências (≥ 2):
| link | canal | views | data | mediana | ×med |
|---|---|---|---|---|---|
| [xpBOF8FXXHM](https://youtu.be/xpBOF8FXXHM) "Por que a Região Sul é o OPOSTO…" | Chão do Sul | 873.711 | 24/10/2026 | 48.014 | 18,2× |
| [it5Vsv851Rc](https://youtu.be/it5Vsv851Rc) "Por que Existem Duas Guianas?…" | Mundo Entrópico | 516.846 | 11/09/2026 | 48.513 | 10,7× |
| [Kzo1yKN-O3w](https://youtu.be/Kzo1yKN-O3w) "Por que tornados e ciclones estão atingindo o Centro-Sul do país?" (no tema) | Brasil Urgente | 205.021 | 05/11/2026 | 15.661 | 13,1× |
Contraevidência declarada: JeanGrafia "Tornado no Paraná: por que a região SUL está na zona de risco?" 0,5×: genérico (Sul inteiro, "zona de risco", sem anomalia concreta). O nosso nomeia **uma direção concreta e verificável no mapa** (o oeste) e não usa "tornado".
Por que não é cópia: nenhum título do tema fala em entrada pelo oeste; a fórmula "Por que [lugar]" é a da bíblia, não a de um clone do tema; não entrega a resposta (o porquê é o vídeo).

## Título 2 · padrão "O/A [coisa concreta] que [faz algo]" · 45 caracteres
"O temporal que atravessou o PARANÁ em 7 horas"
Referências (≥ 2):
| link | canal | views | data | mediana | ×med |
|---|---|---|---|---|---|
| [obG4EMWkCcA](https://youtu.be/obG4EMWkCcA) "O EF5 de Smithville: O Tornado que Arrancou o Asfalto" | Natureza Sinistra | 668.952 | 30/05/2026 | 193.439 | 3,5× |
| [ZSBraswH1To](https://youtu.be/ZSBraswH1To) "O Estado ISOLADO que pode MUDAR o FUTURO do Brasil" | Mundo Entrópico | 114.550 | 20/05/2026 | 48.513 | 2,4× |
Apoio de "tempo curto" no tema: [N9U-HFY5XRE](https://youtu.be/N9U-HFY5XRE) "Três SUPER CÉLULAS em 6 HORAS!" 145,6×.
Por que não é cópia: o objeto (o temporal) e o feito (atravessar o estado em 7 h, medido por nós: Capanema 13h45 → Santo Antônio da Platina 20h45) não existem em nenhum título do tema; não diz o porquê.

## Título 3 · padrão "[LUGAR]: N [eventos] em N [dias/horas]" · 48 caracteres
"PARANÁ: 3 grandes temporais em 20 dias. Por quê?"
Referências (≥ 2):
| link | canal | views | data | mediana | ×med |
|---|---|---|---|---|---|
| [unBF8Vnsx8Q](https://youtu.be/unBF8Vnsx8Q) "Paraná teve 6 tornados em apenas 3 dias; neste ano o total chega a 9 ocorrências" | Ric RECORD Paraná | 71.521 | 23/07/2026 | 2.497 | 28,6× |
| [N9U-HFY5XRE](https://youtu.be/N9U-HFY5XRE) "Três SUPER CÉLULAS em 6 HORAS! Surto de tempestades no Paraná" | De olho no céu | 513.910 | 02/11/2025 | 3.531 | 145,6× |
Por que não é cópia: os dois são contagem de tornados/supercélulas em notícia; o nosso conta temporais do mês (2/11 Maringá F2 + 17 municípios; 7/11 maior apagão do ano, 493,1 mil; 20/11 dois F1 + 353.849 sem luz: B2–B4, E2, E5) e pergunta o porquê. "Grandes" é definido no roteiro pelos três critérios (tornado e/ou apagão recorde).

## Pares A/B/C (resumo)
| par | título | padrão do título | padrão da thumb (vocabulário) | elemento dominante | texto da thumb |
|---|---|---|---|---|---|
| A | T1 | Por que [LUGAR] [anomalia]? | `mapa-lugar` | o Paraná inteiro em relevo 3D, cor de satélite clara, com a escada descendo para oeste e uma seta coral grossa entrando pelo oeste | "POR AQUI?" (palavra-pergunta) |
| B | T2 | O/A [coisa] que [faz algo] | `documento-evidencia` | a imagem real do satélite GOES-19 das 20h de 20/11: a faixa de topos de nuvem laranja/vermelha atravessando o contorno do Paraná | "13H45" … "20H45" (dois rótulos de hora nas pontas da faixa) |
| C | T3 | [LUGAR]: N eventos em N dias | `cena-acao` | foto real da araucária tombada sobre a avenida molhada e os fios, no temporal de 07/11/2026 (AEN/Copel, CC0) | nenhum |
Por que são 3 thumbs diferentes: A = **maquete 3D clara + seta + pergunta**; B = **satélite infravermelho do dia + rótulos de hora** (dado bruto da NOAA, sem relevo, sem seta); C = **foto de rua, árvore-símbolo caída, sem texto**. Composição (bloco inclinado × imagem chapada vista de cima × foto ao nível da rua), elemento dominante (relevo × nuvem × árvore) e tipo de texto (pergunta × horário × nenhum) distintos. Em 5 palavras: A "estado em relevo com seta"; B "nuvem laranja de satélite real"; C "araucária caída na avenida molhada".

## Thumb A · padrão `mapa-lugar` · par de T1 (controle)
- **Composição:** o Paraná recortado em bloco 3D (nosso mapa: SRTM/Terrain Tiles + satélite em cor natural **clara**), visto de sudoeste, um pouco de cima, ocupando ~70% do quadro; exagero vertical forte (≥ 4×, com "ilustrativo" pequeno fora da leitura) para a escada ler: Serra do Mar alta à direita, planaltos descendo até a ponta baixa do oeste à esquerda. Uma seta coral `#E8505B` grossa, curva, vindo da borda esquerda (Paraguai/Argentina) e cravando na ponta oeste (Foz). Fundo: céu cinza-claro dessaturado (não navy).
- **Texto:** "POR AQUI?" em Anton, canto superior esquerdo, "POR" branco `#FBF8F1`, "AQUI?" amarelo `#FFD23F`, contorno `#0E1426`; tipo: palavra-pergunta.
- **Promete:** que existe um lado por onde o temporal entra e que o mapa mostra o porquê · **Conversa com T1:** o título pergunta "por que pelo oeste"; a thumb aponta o lugar exato e pergunta "por aqui?" — juntos: "por que justo por aqui?". Sem repetir "OESTE" nem "temporal".
- **Leitura a 320×180:** 1 foco = a seta coral entrando no bloco claro; o formato do Paraná + "PARANÁ" no início do título identificam o assunto.
- **Execução:** still do nosso mapa 3D (Remotion/three.js, `canal.yaml`) + seta e texto no `Thumb.jsx`; US$ 0, sem IA.
- **Referências do padrão (≥ 2):** [x_xE2HyxQE0](https://youtu.be/x_xE2HyxQE0) Além do Mapa 80.398 · 06/11/2026 · 46,9× (mapa do continente com o Sul destacado e seta curva; no tema); [xpBOF8FXXHM](https://youtu.be/xpBOF8FXXHM) Chão do Sul 873.711 · 24/10/2026 · 18,2× (bloco 3D + seta, bíblia); [it5Vsv851Rc](https://youtu.be/it5Vsv851Rc) Mundo Entrópico 516.846 · 10,7× (pergunta sobre mapa com 1 região).
- **Desvio da bíblia:** nenhum (controle `mapa-lugar` em cor de satélite clara, como o 006 aprovado). Diferença da vizinha 006-A ("UMA PAREDE?", **corte lateral** de um morro): aqui o elemento é o **estado inteiro** visto em perspectiva com uma seta que entra de fora; a 006-A não tem seta de fora nem contorno de estado.

## Thumb B · padrão `documento-evidencia` · par de T2 (exploração)
- **Composição:** a imagem real do GOES-19 (NOAA/NESDIS STAR, canal 13 infravermelho, 20/11/2026 23:00 UTC = 20h) recortada sobre o Paraná (`previa-b-goes-1280.jpg`): a faixa de topos frios (vermelho/laranja/preto) atravessando o quadro de sudoeste a nordeste sobre fundo cinza-médio do infravermelho; o contorno do Paraná redesenhado em branco grosso (3–4 px a 1280) para ler o estado; logo e legenda da NOAA cortados (crédito na descrição).
- **Texto:** dois rótulos em IBM Plex Mono Bold sobre tarja navy pequena, nas pontas da faixa: "13H45" (sudoeste, ao lado de Capanema) e "20H45" (nordeste); tipo: rótulo de horário (sem pergunta, sem número grande).
- **Promete:** a prova do satélite de que foi uma coisa só cruzando o estado numa tarde · **Conversa com T2:** o título diz "atravessou em 7 horas"; a thumb mostra **o que** atravessou e **de onde a onde** (as duas horas), sem repetir "7 horas".
- **Leitura a 320×180:** 1 foco = a mancha laranja/vermelha em diagonal (conferido em `previa-b-320.jpg`); as cores quentes saltam numa grade de fotos cinzentas de funil.
- **Execução:** jpg do STAR já baixado (`dl/goes19/b13/20263242300-3600.jpg`, domínio público NOAA) ou, melhor, o NetCDF ABI-L2-CMIPF reprojetado (`pesquisa/FATOS.md` §G) + contorno IBGE + rótulos no `Thumb.jsx`; US$ 0.
- **Referências do padrão (≥ 2):** [Kzo1yKN-O3w](https://youtu.be/Kzo1yKN-O3w) Brasil Urgente 205.021 · 05/11/2026 · 13,1× (imagem de satélite real dominando o quadro, no tema); [B3oYl6QkVHs](https://youtu.be/B3oYl6QkVHs) Diego San Araujo 352.593 · 5,0× (painéis de radar reais). Evidência de exploração declarada (padrão sem placar no canal; `thumb.md` lista radar/chuva real como `documento-evidencia`).
- **Desvio da bíblia:** nenhum. Não é "mapa escuro dominante": o dominante é a nuvem colorida, e a A é clara (regra de no máximo 1 escura respeitada). Diferença das vizinhas: nenhuma thumb do canal usa satélite infravermelho nem rótulo de hora.

## Thumb C · padrão `cena-acao` · par de T3 (exploração)
- **Composição:** foto real em tela cheia (`dl/fotos/aen-copel-2026-11-07-78655.jpg`, 1356×897, AEN "Foto: Copel", galeria CC0): araucária tombada sobre a avenida, apoiada nos fios, asfalto molhado, céu branco de chuva. Recorte 16:9 mais apertado na árvore e nos fios (cortar o 2º carro à esquerda; o carro branco fica como escala; borrar placas).
- **Texto:** nenhum.
- **Promete:** o estrago real de um dos temporais do mês, com a árvore-símbolo do Paraná no chão · **Conversa com T3:** o título conta "3 grandes temporais em 20 dias. Por quê?"; a imagem é a cara do problema no Paraná (a araucária) — juntos: "o que está derrubando o Paraná?".
- **Leitura a 320×180:** 1 foco = a copa da araucária em diagonal sobre os fios (conferido em `previa-c-320.jpg`); foto clara e nítida no meio de thumbs escuras com tarja.
- **Execução:** foto CC0 já baixada; recorte e leve contraste no `Thumb.jsx`/PIL; US$ 0. Crédito "Foto: Copel/AEN" na descrição.
- **Referências do padrão (≥ 2):** [kUTyeaHS98M](https://youtu.be/kUTyeaHS98M) Ric RECORD Paraná 359.080 · 04/11/2026 · 143,8× (árvores na tempestade, no tema); [GOC2Dzxr82g](https://youtu.be/GOC2Dzxr82g) Band Paraná 1.032.470 · 30/09/2026 · 564,7× (estrago real do temporal em Toledo, sem pessoas em destaque); [N9U-HFY5XRE](https://youtu.be/N9U-HFY5XRE) De olho no céu 145,6× (foto real sem texto, bíblia).
- **Desvio da bíblia:** nenhum (`cena-acao` com 1 herói de perto, sem pessoa, sem máquina, sem texto — a lição aprovada do 006). A foto é de 07/11 e não de 20/11: o T3 fala dos **3 temporais do mês**, e 07/11 é um deles (B4), então não vende a foto como sendo de 20/11. Se a AEN publicar foto CC0 equivalente de 20/11, a etapa 2 pode trocar.

## Obrigações (contrato com as próximas skills)
- **roteiro:** o hook paga a promessa até **0:35**: dizer Capanema 13h45 e Cornélio Procópio 20h15 (com os km/h), os dois tornados no caminho, a contagem "terceira vez em 20 dias" (citando 2/11 e 7/11) e a **frase-âncora**: "Por que o temporal entra pelo oeste do Paraná, e por que voltou três vezes em 20 dias? A resposta está no mapa." Até **1:15**: as estações acendem e viram uma reta, com "atravessou o estado em cerca de 7 horas" (paga T2). Cap. 2–3 (até ~6:00) respondem "pelo oeste"; cap. 4–5 (até ~9:00) respondem "por que de novo" com os 3 temporais nomeados (paga T3). Não prometer previsão do próximo temporal; El Niño só como aumento de chance.
- **thumbnail:** 3 artes, **uma por conceito** (A maquete 3D clara + seta + "POR AQUI?"; B GOES-19 + contorno + "13H45"/"20H45"; C araucária sem texto), nunca 3 variações do mesmo.
- **pacote-youtube:** título A = T1, B = T2, C = T3 (pareados às thumbs A/B/C), com o padrão de cada par no `youtube.txt`; regravar `embalagem/variantes.json` + `embalagem_variantes.py registrar` com títulos finais e arquivos. Créditos: NOAA/NESDIS STAR (GOES-19), NASA GPM IMERG, Copel/AEN (CC0), Simepar, Defesa Civil PR, Copel.
- **qa:** conferir na `legendas.srt` a frase-âncora ≤ 0:35 e "7 horas" ≤ 1:15; os 3 temporais nomeados até ~9:00; cada thumb final contra o seu conceito; as 3 seguem diferentes.

## Crivo
Rodada r1: (pendente)
