# Régua do Universo (@reguadouniverso): análise de formato (16/11/2026)

Canal pt-BR criado em 18/10/2026; 1,42 mil inscritos; 17 vídeos longos (5,5–9 min), mediana 7,6 mil views. Vídeos analisados (720p, assistidos inteiros pelas 16 folhas de quadros a cada 2 s + transcrição Whisper + medições):

| | Asteroide (A) | Hubble (H) |
|---|---|---|
| ID / duração / no ar | bSJYrELB_E8 · 8:37 · 13/11 | BC42u5uBs-4 · 6:43 · 10/11 |
| Views (16/11) / views por dia | 290 mil / 96,6 mil | 60 mil / 9,9 mil |
| Likes por mil | 7,8 | 9,6 |
| Palavras/min · pausas > 0,6 s | 164 · 19 | 150 · 16 |
| Cortes secos/min · plano médio | 8,6 · 6,9 s (mediana 3,2 s) | 7,2 · 8,2 s (mediana 4,3 s) |
| Trocas por histograma · intervalo médio | 76 · 6,7 s | 58 · 6,8 s |
| Quadros quase parados | 60% | 56% |
| Loudness | −16,0 LUFS | −16,1 LUFS |
| Capítulos | 8 | 9 |

Arquivos: `contact.jpg` (24 quadros), `frames/` (40 frames `tipo_A|H_mmss.jpg`), transcrições `transcricao-*.txt`. Scripts em `~/cache/ref-mr/scripts/` (frames.sh, contact.py, audio_gaps.py, motion.py, f0.py, crops.py).

---

## 1. Roteiro

### Hook 0–30 s (transcrição)
**Asteroide:** "No meio do Atlântico, a meio caminho entre a África e o Nordeste do Brasil, o mar abre um buraco. Não é uma onda, é um buraco, com quilômetros de largura e a água subindo em volta dele como uma parede. Em Natal, a uns 1.500 quilômetros dali, ninguém viu nada, ainda. A pergunta que todo mundo faz nessa hora é a mesma: quanto tempo até a onda chegar? Só que essa talvez seja a pergunta errada. Vamos voltar. Nada disso vai acontecer." (0:30) "A pedra que abriu esse buraco existe, tem nome e tem data marcada: chama Apophis."
- Mecânica: cena hipotética em 2ª pessoa geográfica (Brasil/Natal) → pergunta óbvia → "pergunta errada" (loop) → desmonta o medo com honestidade ("nada disso vai acontecer") → âncora real (Apophis, 13/04/2029) → premissa "a gente muda uma coisa só: em vez de passar, ela cai" (0:50).

**Hubble:** "Se você apontar uma câmera para o pedaço mais escuro e mais sem graça do céu e deixar ela aberta por 10 dias seguidos, o que aparece? A resposta certa, em 1995, era provavelmente nada. E mesmo assim, um astrônomo resolveu gastar o telescópio Hubble exatamente nisso. Cientistas respeitados tinham ressalvas. O próprio responsável contou anos depois que tinha pensado no que faria se desse errado. 10 dias, 150 voltas em torno da Terra, 342 fotos de um ponto onde não havia nada para ver." (0:37) "O que apareceu ali mudou a forma como a gente olha para o céu e abriu uma corrida que ainda não acabou."
- Mecânica: pergunta-experimento → resposta "nada" → aposta com risco pessoal (diretor) → 3 números em sequência (frame `texto` 0:30–0:36: 10 · 150 · **342**) → promessa dupla (o que apareceu + corrida que continua).

### Estrutura em blocos (capítulos da descrição)
| A | Bloco | Função |
|---|---|---|
| 0:00 | O buraco no meio do Atlântico | cena hipotética + virada + premissa + CTA 1:01 |
| 1:06 | Apophis, o asteroide real | fatos reais (descoberta, 2,7%→0%, 340 m = Torre Eiffel, 32 mil km) |
| 2:09 | O primeiro minuto do impacto | "Agora troca" (1:48): energia 1.000 Mt, cavidade 6 km, 1/3 vira vapor, onda >100 m a 30 km |
| 3:15 | A onda atravessa o oceano? | "O palpite" (tsunami 2004) → "O formato" (onda alta e curta quebra) → 1% vira onda → plataforma |
| 4:43 | Duas ressalvas | "Então o Brasil não sente nada?" → ninguém publicou; estudo de 50 mil impactos |
| 5:56 | O que vai mais longe | "Vai para cima": som, água na estratosfera, ozônio |
| 7:19 | Já aconteceu: Eltanin | prova histórica (2,5 mi anos, sem cratera) |
| 7:53 | 13 de abril de 2029, de verdade | volta ao real: travessia de 1 h, sondas Ramses/OSIRIS-APEX, QR, fecho |

| H | Bloco | Função |
|---|---|---|
| 0:00 | Dez dias olhando para o nada | hook |
| 0:44 | A aposta de 1995 | Robert Williams, 10% do tempo do diretor |
| 1:35 | Como se escolhe o nada | 20 regiões → 3 → Ursa Maior, zona de visão contínua, moeda a 23 m |
| 2:21 | Dez dias no escuro | 18–28/12/1995, 342 exposições, 4 filtros, soma de luz |
| 3:08 | O que apareceu | **revelação: ~3 mil galáxias (3:19)**, "não mostra só longe, mostra antes" |
| 3:48 | A aposta repetida | "e se fosse acaso?" → HDF-S, UDF (10 mil), XDF (5.500, 13,2 bi anos) |
| 4:42 | Olhar longe é olhar para trás | luz esticada → James Webb, JADES 45 mil, MoM-z14 |
| 5:45 | Existe um fim? | radiação cósmica de fundo = parede de névoa |
| 6:24 | A moeda | callback e fecho |

### Loops / promessas e onde são pagos
| Vídeo | Abre (min) | Paga (min) |
|---|---|---|
| A | "Quanto tempo até a onda chegar? ... pergunta errada" (0:22) | 3:16–4:42 (onda quebra, 1%) e 5:54–7:16 ("o que vai mais longe... vai para cima"; "a resposta honesta" 7:07) |
| A | Título "a onda gigante não é o pior" | 5:56–7:16 (atmosfera/ozônio) |
| A | "Se você quer saber o que chegaria na praia" (1:01, junto do CTA) | 4:43–5:46 e 7:09 ("não é uma muralha de água, é um mar agitado") |
| A | "Então o Brasil não sente nada? Calma, tem duas ressalvas" (4:43) | 4:49–5:41 |
| A | "Isso já aconteceu de verdade" (7:20) | Eltanin 7:24–7:53 |
| A | Abertura "o mar abre um buraco" | fecho espelhado "Naquela noite, o mar vai estar liso" (8:28) |
| H | "O que aparece?" (0:05) | 3:19 (3 mil galáxias), no meio exato do vídeo |
| H | "Uma corrida que ainda não acabou" (0:40) | 3:48–5:38 e "é para lá que a próxima aposta vai apontar" (6:18) |
| H | Moeda a 23 m (2:05, "Pense nisso") | callback 6:25 "Lembra da moeda a 23 metros?" + HDF encolhendo até o tamanho de um ponto (`real_H_0630`) |
| H | "E se aquele pedaço fosse especial?" (3:40) | 3:52–4:00 |
| H | "Existe um fim?" (5:45) | 5:50–6:18 |

### Transições
- **Pergunta retórica ou palavra-gancho falada, repetida em texto de tela cheia** (cartela de 2–6 s): "PERGUNTA ERRADA?", "VAMOS VOLTAR.", "ELA CAI.", "O PALPITE", "O FORMATO", "MAIS UM FREIO", "DUAS RESSALVAS", "PARA CIMA", "A ÁGUA QUE SUBIU", "ESQUENTA OU ESFRIA?", "A RESPOSTA", "JÁ ACONTECEU" (`texto_A_0026`, `texto_A_0054`).
- Dobradiças faladas curtas: "Agora troca." (A 1:48), "E a onda?" (3:16), "Só que estamos no meio do Atlântico." (3:11), "Aqui está a parte que muda tudo." (H 4:41), "Só tem um jeito de saber." (H 3:46).
- **Marcadores de honestidade** como ritmo: "Mas isso ainda não é consenso" (4:41), "Quem der esse número está chutando" (4:57), "Para o tamanho do Apophis, ninguém fez essa conta" (6:58), "a resposta honesta é esta" (7:07), "conta nossa" nos rodapés. Viram cartões na tela (`texto-card_A_0425`).
- Pausa de 0,6–0,9 s em toda virada de capítulo (A 1:05, 2:08, 3:15, 4:43, 5:56, 7:19, 7:53; H 0:44, 1:35, 2:21, 3:08, 3:48, 4:42, 5:45, 6:24) com batida grave (ver Som).

### Fecho
- A: volta ao real (13/04/2029, sondas) → QR → imagem final poética "quem olhar para cima vai ver um ponto de luz passando" + cartela final "E se o Apophis caísse no oceano? O impacto mostrado neste vídeo é um cenário hipotético. O Apophis real passa longe." (8:34).
- H: callback da moeda → "Na próxima vez que você olhar para um pedaço escuro do céu, lembra: ele está cheio. Só falta tempo de exposição." Mesmo plano de abertura (círculo azul no céu, 6:36) + HDF real (6:40).
- Nenhum dos dois reserva 20 s de tela final: o vídeo acaba quase junto com a fala (A 8:34→8:37; H 6:40→6:43).

### CTAs (fala exata)
| Vídeo | Min | Fala | Tela |
|---|---|---|---|
| A | 1:01 | "Se você quer saber o que chegaria na praia, se inscreve, aperta o botão aí no controle." | cartão "INSCREVA-SE · o que chegaria na praia? · aperte o botão no controle" sobre IA da praia (`texto-card_A_0102`) |
| A | 5:46 | "Se você está gostando de testar esses palpites, se inscreve aí no controle, no celular ou na TV. Tem mais experimento desses vindo." | cartão "INSCREVA-SE · tem mais experimento desses vindo · aperte o botão no controle, no celular ou na TV" (`texto-card_A_0549`) |
| A | 8:21 | "Se quiser começar a olhar o céu até lá, o QR Code na tela leva para uma seleção de telescópios e livros." | QR no canto superior direito + cartão "PARA OBSERVAR O CÉU · telescópios e livros · aponte a câmera do celular para o QR code" + "link de afiliado" (`texto-card_A_0825`), 8:22–8:27 |
| H | 5:38 | "Se você gosta de ver o céu ficando mais fundo a cada aposta, se inscreve. Toda semana tem uma régua nova por aqui." | cartão "GOSTA DE VER O CÉU MAIS FUNDO? · Inscreva-se no canal" + "Toda semana, uma régua nova" (`texto-card_H_0544`) |

- O CTA de inscrição é **amarrado à promessa do vídeo** ("se quer saber o que chegaria na praia") e fala com quem assiste **na TV** ("no controle"). **Hipótese:** boa parte do público assiste em TV (fundo escuro, letras grandes e −16 LUFS combinam com isso).
- Produto: **afiliado Amazon** (tag `reguadouniver-20`): telescópio iniciante, binóculo, 1 livro de divulgação por vídeo (Neil deGrasse Tyson; Carl Sagan). No A há QR na tela; no H só na descrição.

### Descrições
- A: sinopse + **aviso "⚠️ CENÁRIO HIPOTÉTICO"** + "Neste vídeo:" + link de inscrição `?sub_confirmation=1` + capítulos + afiliados com aviso de comissão + **14 fontes com data de consulta** (NASA, CNEOS/JPL, Los Alamos/Gisler, Robertson & Gisler 2019, NASA/TM-2017-219463, Rumpf 2017, Pierazzo 2010, Imperial College, Eltanin NTRS, NOAA, ESA) + parágrafo **"Sobre os números"** (o que é suposição, o que é conta do canal, discordância ESA 375 m × NASA 340 m) + créditos de imagem: "cenas do impacto e do céu são ilustrações geradas por IA (marcadas na tela)", "Animação da passagem de 2029: NASA/JPL-Caltech", "Mapas e diagramas são do canal", "A NASA não endossa este canal" + "🎙️ Narração com voz sintética. Roteiro, pesquisa e edição do canal".
- H: inscrição + "Assista também" (2 vídeos) + afiliados + sinopse + capítulos + mais 1 link interno + 11 fontes + nota de contas próprias + crédito completo de cada imagem real (STScI/NASA/ESA/CSA com nomes) + "As demais cenas são ilustrações geradas por IA" + voz sintética.
- Música: **não citada** em nenhuma descrição.

---

## 2. Visual plano a plano

Contagem: todos os quadros de 2 s (A = 258, H = 201), classificados pelo tipo dominante.

| Tipo de plano | A (quadros · %) | H (quadros · %) | Exemplos |
|---|---|---|---|
| Ilustração/vídeo de IA (Higgsfield) | 56 · **21,7%** | 36 · **17,9%** | `ia_A_0002` (cratera, vídeo), `ia_A_0242` (coluna de vapor), `ia_A_0543` (cinema), `ia_H_0004`, `ia_H_0556` |
| Material real (NASA/STScI/ESA/JPL) com Ken Burns lento | 1 · 0,4% | 33 · **16,4%** | `real_A_0140` (animação JPL), `real_H_0017` (Hubble, "Foto: NASA"), `real_H_0318` (HDF), `real_H_0536` (MoM-z14), `real_H_0630` |
| Mapa esquemático (Atlântico, Brasil–África) | 23 · 8,9% | 0 | `mapa_A_0022` (relógio T+), `mapa_A_0616`, `mapa_A_0758` |
| Diagrama/escala/gráfico animado (motion próprio) | 74 · 28,7% | 48 · 23,9% | `diagrama_A_0124` (Apophis × Torre Eiffel), `diagrama-grafico_A_0204` (grade de 1.000 quadrados), `diagrama_A_0350` (onda), `diagrama_H_0146` (Ursa Maior), `diagrama_H_0258` (filtros RGB) |
| Número grande / palavra em tela cheia | ~35 · ~13,6% | ~18 · ~9% | `texto_A_0026`, `texto_A_0054`, `texto_H_0512` (45.000 galáxias) |
| Cartão de texto (kicker + frase + fonte) | ~64 · ~24,8% | ~55 · ~27,4% | `texto-card_A_0042`, `texto-card_A_0425`, `texto-card_H_0544` |
| Preto/transição | 5 · 1,9% | 11 · 5,5% | — |

**Real × IA × motion próprio:** A = 0,4% real · 21,7% IA · ~76% motion gráfico próprio. H = 16,4% real · 17,9% IA · ~60% motion próprio. Ou seja: o canal "de fotos da NASA" é na verdade **um canal de motion graphics em fundo preto**, com IA como "cena" e foto real só quando o tema é uma imagem real (Hubble).

**Vídeo de vídeo:** nenhum vídeo real de arquivo (B-roll filmado) nos dois. A única "animação real" é a da NASA/JPL (A 1:40), mostrada parada.

**Duração do plano:** médio ~7 s, mediana 3–4 s; planos longos são gráficos que se constroem por 20–36 s (ex.: A 2:10–2:28, profundidade do oceano; A 3:36–3:54, ondas). Planos de IA duram 2–14 s (A 0:00–0:12; A 2:30–2:58 em sequência de 4 clipes).

**De onde vem o movimento** (medido: diferença média entre quadros, `motion.py`):
- Clipes de IA **são vídeo** (rótulo "Vídeo: ilustração gerada (Higgsfield)"): diferença 3,4–4,6 contínua (A 0:00–0:09), contra 0,0–0,2 nos gráficos parados.
- Fotos reais: zoom/pan lento (diferença ~2,6, mediana 0,8; H 3:14–3:27) e um zoom-out que encolhe o HDF até virar um ponto (H 6:28–6:34).
- Gráficos: tudo entra animado e depois fica parado (mediana 0): contadores (2.999→3.000; 988→1.000 Mt; 37.739→50.000; 341→342; 12,9→13,2; 44.674→45.000; 1,0%→2,7%→1,4%→0,0%), grade que se enche (A 2:00–2:04; 6:28–6:32), linha que se desenha (ondas, curva do ozônio 6:50–6:56), **relógio T+ correndo no mapa** (A 0:20–0:24 T+03:48→15:00; 6:10–6:16 T+14:46→50:00; 7:58–8:04 travessia T+16:04→01:00:00), círculos de alcance que crescem (3:04–3:10), coluna d'água que sobe (6:20–6:26), calendário riscando dias (H 2:22–2:26).
- Por isso 56–60% dos quadros ficam "quase parados": a sensação de ritmo vem da **troca de informação** (novo número/novo cartão a cada 3–7 s) e da animação de entrada, não da câmera.

---

## 3. Tipografia e rótulos

- **Fonte (Hipótese):** família Montserrat. Títulos e frases dos cartões em grotesca larga e pesada com "a" de um andar (**Montserrat Alternates ExtraBold/Black**, `texto-card_A_0425`); kicker em Montserrat Bold caixa alta espaçada; rodapé em Montserrat Regular cinza.
- **Paleta semântica (A):** fundo quase preto (#0b0b10 aprox.); **laranja = hipotético/modelo** (2,7%, ≈1.000 Mt, ≈6 km, >100 m, "ELA CAI."); **ciano = real/fato** (APÓFIS, 0,0%, "13 DE ABRIL DE 2029", "PARA CIMA"); branco = neutro; cinza = comparação antiga (barras "estimativas antigas 15%").
- **Tela cheia:** 1 palavra ou número, centralizado, ~10–15% da altura (≈ 70–100 px em 720p), com subtítulo pequeno embaixo ("nada disso vai acontecer", "todo o resto fica igual", "estimativa de dezembro de 2004") e kicker em cima ("ASTEROIDE 99942", "NESTE VÍDEO, UMA MUDANÇA SÓ").
- **Cartão:** retângulo escuro arredondado, borda fina, barra de destaque ciano à esquerda; 3 linhas: KICKER ciano caixa alta (data/lugar/tipo: "SEATTLE · AGOSTO DE 2016", "A CONCLUSÃO", "O QUE OS MODELOS DIZEM") → frase branca de **1–2 linhas** → fonte cinza ("Relatório NASA/TM-2017-219463", "Rumpf, Lewis e Atkinson, 2017"). Posição: esquerda (topo, meio ou baixo), ~45% da largura; fica 4–10 s (A 5:00–5:14, 14 s em 2 cartões). Entrada por fade (H 3:40→3:42).
- **Sobre imagem:** número laranja grande no canto inferior esquerdo com kicker ("DISTÂNCIA DO PONTO DO IMPACTO ≈ 1.500 km", `ia_A_0015`; "VIRA VAPOR · MODELO A 20 KM/S ≈ 1/3 · no nosso cenário, mais lento: menos").

**Crédito na tela: existe, em 3 camadas (é o diferencial do canal):**
1. **Selo no canto superior esquerdo (só no A):** barra vertical + "CENÁRIO HIPOTÉTICO" em laranja caixa alta espaçada (~14–16 px em 720p) + 2ª linha ("ilustração do cenário", "Nordeste · ilustração", "ninguém calculou"); "REAL" em ciano (1:40); "ILUSTRAÇÃO · O QUE O CINEMA MOSTRA" (5:42). Fica o plano inteiro. No H não há esse selo.
2. **Crédito da imagem no canto inferior direito** (os dois vídeos): texto cinza ~11–13 px em pílula escura semitransparente, o plano inteiro: "Imagem: ilustração gerada (Higgsfield)", "Vídeo: ilustração gerada (Higgsfield)", "Imagem: NASA/JPL-Caltech", "Foto: NASA", "Imagem: Robert Williams and the Hubble Deep Field Team (STScI) and NASA", "Image: NASA, ESA, CSA, STScI, Rohan Naidu (MIT); Image Processing: Joseph DePasquale (STScI)". Legível na TV, quase invisível no celular.
3. **Rodapé de todo gráfico/mapa no canto inferior esquerdo** (~10 px, cinza): "ESQUEMA · contorno simplificado · cenário hipotético", "ESQUEMA em escala · distâncias da NASA", "Modelo: Gisler, Weaver e Gittings (Los Alamos), 2011", "Fonte: NASA / CNEOS", "esquema · Hubble Deep Field, 18 a 28 de dezembro de 1995 · NASA/STScI", "conta nossa".
- Nas thumbs: "ilustração" pequeno no canto inferior esquerdo, ou "foto real: ESO" / "foto real NASA / Hubble" no canto superior esquerdo (`thumbs.jpg`).

---

## 4. Fontes do material

| Material | Origem (tela + descrição) |
|---|---|
| Cenas de IA (vídeo e still) | **Higgsfield** (rótulo na tela); descrição: "ilustrações geradas por IA" |
| Fotos reais | NASA/STScI: Hubble Deep Field (R. Williams & HDF Team), HDF South, Ultra Deep Field (S. Beckwith/HUDF Team), eXtreme Deep Field (Illingworth, Magee, Oesch, Bouwens), JADES (NASA/ESA/CSA, B. Robertson et al.; A. Pagan), MoM-z14 (R. Naidu; J. DePasquale); Hubble em órbita: NASA |
| Ilustração/animação de agência | James Webb: ilustração NASA; passagem do Apophis 2029: NASA/JPL-Caltech |
| Mapas, diagramas, gráficos | do canal (motion próprio) |
| Dados | NASA, CNEOS/JPL, ESA, NOAA, Los Alamos (Gisler et al.), Imperial College (Earth Impact Effects), artigos revisados (AJ, Acta Astronautica, GRL, EPSL), National Geographic, STScI Newsletter |

---

## 5. Som

- **Voz:** sintética (declarado na descrição: "Narração com voz sintética"). Masculina (F0 mediano medido ~123 Hz nos dois vídeos, mesma voz), 150–164 pal/min, dicção limpa (Whisper small erra só nomes próprios). Fornecedor: **Hipótese** ElevenLabs (multilingual) ou Fish; não dá para afirmar sem ouvir/comparar.
- **Trilha:** cama contínua de pad/ambiente, ~13–15 dB abaixo da voz (voz −15 dB RMS; pausas −27 a −33 dB RMS; espectrograma mostra tons graves sustentados nas pausas). Não creditada na descrição (**Hipótese:** biblioteca do YouTube/Epidemic).
- **SFX:** nas viradas de capítulo, pausa de 0,6–0,9 s com **batida grave** (energia < 120 Hz com pico −13 dBFS e quase nada acima de 3 kHz; ex.: H 0:43,9; A 4:43,3; A 7:47,9 pico total −3 a −6 dBFS) → **Hipótese:** "boom/sub hit" ou subida de trilha, **sem whoosh** perceptível no espectro. H 0:11,6 (galáxias aparecendo) tem energia aguda nas pausas → **Hipótese:** brilho/"shimmer" de revelação. Não usa SFX de carimbo, digitação etc.
- **Mixagem:** −16 LUFS integrados (≈ −14 pedido pelo YouTube; não esmaga a voz), voz sempre na frente, sem música no clímax competindo com fala.

---

## 6. Por que o Asteroide estourou (290 mil) e a maioria fica em 1–5 mil

Placar do canal (`canal.csv`, 16/11): 290 mil (asteroide) · 110 mil (Vazio de Boötes) · 67 mil (Webb × Hubble) · 60 mil (Hubble no nada) · 50 mil (Próxima Centauri) · 34 mil (maior estrela) · 19 mil · 14 mil · 8 mil… e 9 vídeos entre 0,4 e 5 mil. Os de 12–16/11 têm só 1–4 dias, mas em views/dia também estão baixos (95–1.356/dia contra 96,6 mil/dia do asteroide).

| Fator | Vencedores (A 290k, Boötes 110k, Hubble 60k) | Fracos (buraco negro 1,7k, galáxias Webb 1k, Júpiter 0,4k, ELT 1,3k, céu escuro 3,5k) |
|---|---|---|
| Tema | **evento/catástrofe ou aposta com cena física** (asteroide cai, buraco no universo, telescópio olhando o nada) | conceito de livro didático ou superlativo ("o maior ___", "prova de que o universo começou") |
| Título | cena + virada: "Um asteroide cai no oceano. **A onda gigante não é o pior**"; "A NASA apontou… **Veja o que apareceu**" | rótulo/superlativo saturado: "O tamanho assustador do maior buraco negro…" |
| Thumb | imagem que o público já conhece (tsunami engolindo cidade; campo profundo com círculo vermelho) + 2 palavras que **negam** a expectativa: "NÃO É ASSIM.", "PARECIA VAZIO." | ilustração genérica (buraco negro, JWST, Júpiter) + frase sem conflito ("CADA VEZ MENOR.", "ISSO ERA POSSÍVEL?") |
| Público | fora da bolha de astronomia (desastre, medo, tsunami) | só fãs de astronomia (likes por mil 14–19 = núcleo fiel; o A tem 7,8 = público casual) |

O que só o asteroide teve:
1. **Medo próximo e geográfico:** o hook põe o impacto entre a África e o **Nordeste do Brasil** e pergunta pela onda em **Natal**; o CTA promete "o que chegaria na praia". Nenhum outro vídeo põe o espectador brasileiro dentro da cena.
2. **Contra-intuição verificável:** o título desmonta o clichê de filme (muralha de água) e o roteiro paga isso com estudos (1% da energia vira onda; 2016 NASA/NOAA; plataforma continental) e mostra o perigo real (atmosfera/ozônio). É "mito × ciência" com stakes, e não só escala.
3. **Gancho de data real:** Apophis 13/04/2029 é notícia recorrente e tem cara de "isso vai acontecer".
4. **Os 12 primeiros segundos são os mais cinematográficos do canal:** 3 clipes de vídeo de IA (cratera no oceano, parede de água), contra estrelas paradas no H.
5. **Hipótese** (sem dado de tráfego): estourou por sugeridos/navegar ao lado de vídeos de tsunami/asteroide/"e se", com público de TV (CTA "no controle").

---

## 7. O que copiar (forma, não conteúdo)
- Cor semântica **hipotético = laranja / real = ciano** + selo "CENÁRIO HIPOTÉTICO"/"REAL" no canto superior esquerdo + crédito da imagem embaixo à direita em todo plano + rodapé de fonte em todo gráfico. Dá confiança e permite usar IA sem enganar.
- Motion próprio barato (~60–76% do vídeo): fundo preto, contador, barra, grade, mapa com relógio T+, escala com objeto conhecido (Torre Eiffel, moeda a 23 m). A IA fica só para as "cenas" (~20%).
- Roteiro "cena hipotética → pergunta óbvia → 'pergunta errada' → real → 'muda uma coisa só' → passo a passo com ressalvas → prova histórica → volta ao real → imagem final espelhada".
- CTA de inscrição amarrado à promessa, aos ~1:00 e aos ~66% do vídeo; produto (afiliado) com QR só no fim.
