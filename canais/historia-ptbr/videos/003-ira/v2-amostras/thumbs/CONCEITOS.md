# Thumbs v2 do Irã (003): pesquisa, 4 conceitos novos e o que mudar no Egito e na Índia

Data: 2026-11-04. Vídeo: "A história INTEIRA do Irã em 15 minutos" (`youtube.videos` id 5, não publicado).
Problema: o CTR do Egito e da Índia, já no ar, está abaixo de 2% (informação do Rodrigo, 2026-11-04; o número exato e a janela não foram registrados). As thumbs A/B/C do Irã (`entrega/thumb-A/B/C.jpg`) repetem a fórmula "ilustração + PAÍS gigante + ANO a.C. – 2026".

Arquivos:
- `thumb-1.jpg` … `thumb-4.jpg`: os 4 conceitos (1280x720, de 154 a 244 KB).
- `prancha-4-thumbs.jpg`: as 4 em 2x2. `prancha-4-thumbs-celular.jpg`: as 4 com 320 px de largura, lado a lado, sobre fundo escuro (como na grade do app).
- `prancha-pesquisa.jpg`: as 52 thumbs da pesquisa com canal, views e idade. Os originais e o `manifest.tsv` estão em `pesquisa/`.
- `base/`: as ilustrações sem texto (`c*-a/b.png`), os prompts (`prompts*.json`), o `gen.py` (chamada ao fal) e o `compose.py` (texto em PIL), com as fontes em `base/fonts/`.

---

## 1. Pesquisa

**Método.** Views do RSS público de cada canal (via WARP, 2026-11-04) e da busca do YouTube em pt-BR (via WARP, `hl=pt-BR&gl=BR`). As thumbs foram baixadas de `i.ytimg.com/vi/<id>/hqdefault.jpg`, e o que já havia em `youtube.garimpo_videos`/`assistidos` e em `pesquisa/countrycorns/ANALISE.md` também entrou. **Limite:** view não é CTR. O total mistura idade do vídeo, assunto, notícia do momento e tamanho do canal. As comparações mais limpas são **dentro do mesmo canal**, com o mesmo template e idades parecidas. Tudo o que vem daqui é **Hipótese** até o CTR do Studio confirmar.

### 1.1 O padrão "nome + datas + panorama" quase não funciona em pt-BR
| Vídeo (pt-BR) | Canal | Views | Idade | Thumb |
|---|---|---|---|---|
| `V5uw1BPpToA` Roma em 12 min | História em Minutos (UCvVu…) | 142 | 3 sem | ROMA + "753 a.C. – 476" + panorama |
| `KRu9UPzH8BE` Roma em 8 min | História Todo dia | 150 | 6 meses | centurião + "1000 ANOS DE HISTÓRIA" |
| `Cdk3m2OYfPs` Roma em 12 min | HistoriaMundialSemFiltros | 171 | 3 sem | bonequinho com as mãos na cabeça + "2.000 ANOS 1 IMPÉRIO" |
| `TGe2XhMt7zI` Roma em 10 min | Encantos Retrô | 577 | 2 dias | personagem + ROMA + datas |
| `9zPaQphHBbQ` Roma em 13 min | Vultos e Impérios | 672 | 1 mês | ROMA + datas + panorama (igual à nossa) |
| `XyulPwDw1CE` Roma em 12 min | History Easy Guide | 1.536 | 7 dias | bonequinho + ROMA + "A HISTÓRIA INTEIRA" |
| `g847Td0Plsk` **nosso** Egito | historia-ptbr | 20 | 1 dia | EGITO + "5000 a.C. – 2026" + panorama |
| `MV5SSjoccqE` **nossa** Índia | historia-ptbr | 17 | 2 dias | Gandhi + ÍNDIA + "3300 a.C. – 2026" |

O formato "A história INTEIRA de X em N minutos" com essa thumb virou commodity em pt-BR: há dezenas de clones e quase nenhum passa de mil views. A thumb igual à de todo mundo não dá motivo para clicar **no nosso**. **Hipótese** forte.

**A exceção que precisa ser dita:** `uEDDMWJ04Vo` (Crônicas de Ferro, "Toda a história do Irã em 20 minutos", **1.460.196 views**, 7 meses) usa exatamente essa fórmula: panorama + "IRÃ" em serifa vermelha + "4000 a.C. - 2026". **Hipótese:** ele saiu por volta de abr/2026, logo depois da morte de Khamenei (fev/2026, N094 do roteiro), e pegou a onda de busca. Nós não temos essa onda. Ou seja, a fórmula não é proibida, mas não gera curiosidade sozinha: depende de demanda por busca.

### 1.2 Mesmo canal, mesmo template: o rosto pesa mais que o panorama
History in Minutes (UCYjRQ6T2BxBnJtPytI9OnNg), todos com "PAÍS + datas", de 25 a 54 dias no ar:
| ID | Tema | Views | Arte |
|---|---|---|---|
| `p9IIGdg91fE` | Índia | **613.956** | rei indiano grande em primeiro plano |
| `VQPzrVMHWlg` | Egito | 445.878 | panorama (pirâmides; tema icônico) |
| `UEdPIsvxlGg` | Ucrânia | 178.557 | Zelensky + prédios em chamas |
| `XVwr1Rm_9jc` | **Irã** | **89.891** | só panorama (mesquita de Isfahan) |
| `EOA5-VFVI-g` | China | 55.587 | — (não baixada) |
| `DEZa_8_KicU` | Roma | 19.861 | panorama + águia |
| `JX-e5db8HzI` | Israel-Palestina | 16.092 | dois homens parados, sem emoção |

O Irã sem personagem teve 1/7 da Índia com personagem, no mesmo canal. Archive in Minutes (`pbIzG1QvoWs` Gestapo 351 mil, `PmpWyltn08s` SS 329 mil, `YLqXhVlZKQo` NKVD 22 mil) **sempre** põe um personagem grande, e a variação ali vem do assunto. **Hipótese:** personagem grande é o requisito mínimo, e o tema/ângulo faz o resto.

### 1.3 Irã em pt-BR: o que concentra as views
| ID | Canal | Views | Idade | O que a thumb faz |
|---|---|---|---|---|
| `dVY_arfXbk0` | GeoDocs | 3.946.796 | 1 ano | lugar estranho (vila nas rochas) + 2 velhos de costas; o título promete virada ("Este vídeo vai mudar sua visão") |
| `tArMc9-s7Fw` | Estranha História | **2.141.572** | 1 ano | **antes × depois**: relevo persa antigo, apresentador espantado no meio e Khomeini; título "Como a Pérsia 'se tornou' o Irã?" |
| `3D_vS0XlC1w` | Canal Nostalgia | 1.968.494 | 1 ano | **conflito**: Netanyahu × Khamenei frente a frente, explosão no meio, bandeiras |
| `uEDDMWJ04Vo` | Crônicas de Ferro | 1.460.196 | 7 meses | a exceção (1.1) |
| `T9g8yzOc3KA` | Brasil Paralelo | 843.375 | 8 meses | Khomeini no centro, o xá e presidentes dos EUA, "A REVOLUÇÃO IRANIANA DE 1979" |
| `gCcHuuKm-SU` | Globalizando Conhecimento | 550.422 | 3 anos | mapa 3D com bandeira |
| `dPfppHKbwhM` | Fatos Desconhecidos | 215.065 | 9 meses | **rosto dividido**: metade rei persa, metade clérigo moderno |
| `-Qm2Kg2nMPs` | Plano Piloto | 198.804 | 1 ano | cartoon (bonequinho + persa espantado) + "Mega Resumo" |
| `oaa1SDG0U0Q` | Brasil Paralelo | 194.054 | 7 meses | Khomeini + xá, "RESUMO" |

- O **turbante preto + barba branca** (Khomeini/clérigo) aparece em 5 das 9. É o ícone visual do Irã para o público brasileiro.
- **"Pérsia → Irã"** é a pergunta que o público já faz: 3 vídeos com o título "Como a Pérsia (se) tornou o Irã?" somam ~2,55 mi de views. Dois deles usam **rosto dividido / antes × depois**.
- O mesmo recurso fora do Irã: `ZUt_OO_C4Eo` (Canal Nostalgia, "BRASIL ANTES DE 1500", **7,4 mi**) é um rosto dividido, metade indígena e metade português.

### 1.4 Outros sinais (EN e pt-BR)
- **CountryCorns / History Tab** (`pesquisa/countrycorns/ANALISE.md`): `ihGK1iyUN1E` Israel, **1,14 mi**: personagem com raiva **apontando** para a palavra gigante. `HHIQeJqnkuE` Coreia (354 views): conflito frente a frente, mas com troca de formato e de público, então não serve de prova contra o conflito.
- **OverSimplified** (`tsxmyL7TUJg` 72,6 mi, `AAGIi62-sAU` 58,4 mi, `QLq6GEiHqR8` 40 mi): caricaturas com **emoção forte** (raiva, desconfiança) nas bordas, os lados do conflito visíveis e um objeto estranho no centro (a cerveja da Lei Seca, o porco da Pig War). Pouquíssimo texto.
- **Kings and Generals** (`kd-ZNqGaajg` 463 mil, `H2xV6FnbSkQ` 422 mil, `hSMwc_RRqiQ` 345 mil × `qlw39TP8OrE` 48 mil): as boas têm **um personagem em ação/tensão** + 2–3 palavras grandes. A fraca é um quadro escuro, sem texto e sem foco.
- **pt-BR geral:** `3bkzyOnRPM0` Você Sabia? (3,19 mi): rosto **espantado** + 4 épocas lado a lado. `5n_KfzZcN3s` Problema de Rico (525 mil): afirmação que provoca ("A MAIOR ILUSÃO DA HUMANIDADE"), não o nome do tema. `7amJtj96T0w`/`aMld6kMmcm4` "História em minutos" (UCuquAW2…): França 140 mil e Rússia 206 mil com o **líder atual + cidade em chamas**, mas Austrália (`CZZz1lHMBMM`) com o mesmo template tem 1.976. O tema manda.

### 1.5 Regras extraídas (todas **Hipótese** até o CTR do Studio)
1. **Personagem grande com emoção, ou dois em conflito, ocupando ≥ 40% da arte.** Panorama sem rosto é o pior caso (HiM: Irã 90 mil × Índia 614 mil; clones de Roma com 142–1,5 mil).
2. **Uma tensão ou lacuna em no máximo 3 palavras, que o título não responde:** antes × depois (Pérsia → Irã: 2,14 mi + 215 mil; "Brasil antes de 1500": 7,4 mi), conflito (Nostalgia: 1,97 mi; OverSimplified), pergunta ou objeto misterioso.
3. **Thumb e título não se repetem.** O título já diz "A história INTEIRA do Irã em 15 minutos", então a thumb não precisa de "IRÃ + 4200 a.C. – 2026". Ela vende o *porquê* (a surpresa do roteiro). Datas só como detalhe, e só se forem viradas (1891 · 1979).
4. (Identidade) Para ser reconhecível na grade sem copiar ninguém: os **bonequinhos de cabeça redonda branca** como personagens, **Libre Caslon 700** no texto principal e **amarelo-ouro** (#F7C21B) em um único elemento por thumb (palavra, seta, faixa ou pílula).

---

## 2. Os 4 conceitos (gerados)

Comum a todos: ilustração do `fal-ai/nano-banana/edit` com 2 imagens do canal como referência de estilo (`001-egito/imagens/I041.jpg` e `002-india/imagens/I041.jpg`), saída de 1344x768 reduzida para 1280x720. Texto composto em PIL com Libre Caslon Text 700 e Open Sans 800 (TTF do repositório google/fonts, OFL), contorno preto grosso e sombra chapada. Todos foram conferidos com 320 px de largura (`prancha-4-thumbs-celular.jpg`): as palavras principais leem. A única parte pequena é a pílula "1891 · 1979" da thumb 3, que é secundária.

### thumb-1: "PÉRSIA → IRÃ" (antes × depois)
- **Arte:** tela dividida por uma rachadura luminosa. À esquerda, um rei aquemênida (coroa dourada, barba quadrada, fundo dourado com as colunas de Persépolis). À direita, um clérigo de turbante preto e barba branca, carrancudo, sobre fundo vermelho e preto. Os dois se encaram.
- **Texto:** `PÉRSIA` (ouro) `→` (seta ouro) `IRÃ` (branco).
- **Gatilho:** contraste antes × depois e a pergunta que o público brasileiro já faz ("como a Pérsia virou o Irã?", ~2,55 mi de views em 3 vídeos). Usa também o ícone do turbante, presente em 5 das 9 thumbs de Irã mais vistas.
- **Com o título:** o título promete "a história INTEIRA" e a thumb mostra as duas pontas dela. A lacuna é o meio: como se vai de um para o outro? Bate com N013–N015 (o nome Irã/Pérsia) e N073 (o pedido de 1935).
- **Por que deve passar de 2%:** é o padrão com mais prova no nicho em pt-BR (Estranha História e Fatos Desconhecidos no Irã; Canal Nostalgia em "Brasil antes de 1500"). **Hipótese**, e a mais segura das quatro.
- Base: `base/c1-persia-ira-a.png` (1ª tentativa).

### thumb-2: "SALVOU O IRÃ?" (o caixão do poeta)
- **Arte:** à noite, diante de um portão persa de azulejos turquesa, um caixão de madeira entreaberto solta uma luz dourada. O bonequinho, enorme, espia a fresta em choque (boca aberta, mãos no rosto). Ao fundo, uma caravana de camelos pequena.
- **Texto:** `SALVOU` (branco) / `O IRÃ?` (ouro) + seta amarela apontando para o caixão.
- **Gatilho:** **lacuna de informação pura**, com um objeto misterioso e uma reação de choque. Ninguém adivinha o que há dentro de um caixão que "salvou" um país, e a resposta (a língua persa) só vem em N051.
- **Com o título:** é o hook do vídeo (N001–N005) virado imagem: "E o que salva o Irã… está dentro daquele caixão." Quem clica ouve, nos primeiros 15 s, exatamente a promessa da thumb. Isso ajuda a retenção do início e evita a sensação de clickbait.
- **Por que deve passar de 2%:** é a mais diferente da grade (nenhuma thumb de "história inteira" usa objeto + pergunta) e tem rosto com emoção. **Hipótese:** é a de maior risco e maior teto. Pode perder para a 1 em quem busca "Irã" e ganhar em quem navega.
- Base: `base/c2-caixao-b.png` (2ª tentativa; a 1ª tinha o caixão pequeno e um portão de castelo europeu).

### thumb-3: "COROA × TURBANTE" (conflito)
- **Arte:** um xá (coroa de joias com pluma, farda com dragonas e faixa azul) e um clérigo (turbante preto, barba branca) testa contra testa, os dois com raiva. O clérigo aponta o dedo, há um raio amarelo entre eles e uma multidão vermelha atrás do clérigo.
- **Texto:** `COROA` (ouro) `×` `TURBANTE` (branco) + pílula amarela `1891 · 1979`.
- **Gatilho:** **conflito** com dois lados visíveis (como OverSimplified, Canal Nostalgia 1,97 mi e CountryCorns). A pílula traz a lacuna: o que liga 1891 a 1979?
- **Com o título:** promete o fio que atravessa o vídeo ("Um turbante vence uma coroa. Guarde esse tabaco", N069, e "De novo, um turbante enfrenta uma coroa", N081). 1979 é o ano mais buscado do Irã em pt-BR (Brasil Paralelo, 843 mil).
- **Por que deve passar de 2%:** conflito com rosto e emoção, e uma palavra (turbante) que é a imagem mental do Irã moderno. **Hipótese.** Risco: pode parecer vídeo só sobre a revolução, e não sobre a "história inteira".
- Base: `base/c3-turbante-coroa-a.png` (1ª tentativa).

### thumb-4: "VIRARAM PERSAS" (o absurdo)
- **Arte:** num jardim persa com cúpula turquesa e ciprestes, quatro conquistadores bonequinhos (hoplita grego, guerreiro árabe, soldado turco, mongol com arco) sentados num tapete vermelho, felizes, tomando chá em copinho de vidro e lendo livros de poesia. As espadas ficam esquecidas na grama.
- **Texto:** `VIRARAM` (preto, contorno branco, sobre o céu) / `PERSAS` (preto sobre faixa amarela).
- **Gatilho:** **incongruência e humor**: guerreiros temidos fazendo o oposto do esperado. A pergunta é "como assim?". O traço de bonequinho combina com o tom (cartoon como Plano Piloto, 199 mil, e OverSimplified).
- **Com o título:** é a tese do vídeo (N004 "Todos vão embora… ou acabam virando persas", N056–N057 "Ele os digere" e N101). O título dá o escopo e a thumb dá o ângulo.
- **Por que deve passar de 2%:** é a mais "nossa" (a identidade de bonequinho como diferencial na grade), com humor e uma afirmação estranha. **Hipótese:** é a mais fraca em rosto (personagens menores e sorrisos iguais), por isso a ponho como 4ª no teste.
- Base: `base/c4-viraram-persas-b.png` (2ª tentativa; na 1ª o mongol tinha rosto realista e o grego faltava).

**Recomendação para o "Testar e comparar" (3 slots):** 1 (PÉRSIA → IRÃ), 2 (SALVOU O IRÃ?) e 3 (COROA × TURBANTE). A 4 fica de reserva ou para um Short. Registre o vencedor e o CTR de cada uma em `conhecimento/thumbnails/README.md`.

---

## 3. O que mudar nas thumbs do Egito e da Índia (não geradas; propostas para trocar no YouTube)

As duas estão abaixo de 2% e seguem "panorama/personagem + PAÍS + datas". A proposta é aplicar as mesmas 3 regras usando o hook de cada roteiro.

### Egito (`g847Td0Plsk`, "A história INTEIRA do Egito em 17 minutos")
1. **"COMO ASSIM?": Cleópatra e o iPhone (paradoxo do tempo, N003).** Uma Cleópatra bonequinho, espantada, segura um iPhone. Atrás dela, as pirâmides já em ruína, com bonequinhos construtores ao longe. Texto: `MAIS PERTO` (branco) / `DO iPHONE?` (ouro), ou só `COMO ASSIM?` com uma seta para o celular. Gatilho: fato contraintuitivo e objeto fora do lugar (como a cerveja do OverSimplified). Com o título: a "história inteira" cabe num paradoxo que só o vídeo explica. **Hipótese.**
2. **"95% DESERTO" (antes × depois / mapa estranho, N001–N002).** O Egito visto do espaço, todo bege, com só uma linha verde fina (o Nilo). O bonequinho astronauta aponta para a linha, em choque. Texto: `SÓ ISSO?` em ouro com seta para a faixa verde. Gatilho: imagem estranha e pergunta (mapa como Globalizando, 550 mil). **Hipótese.**

### Índia (`MV5SSjoccqE`, "A HISTÓRIA COMPLETA da Índia em 19 minutos")
1. **"O MESMO PAÍS?" (antes × depois, N001–N003).** Tela dividida na mesma paisagem: à esquerda, maio (terra rachada, marrom, sol vermelho); à direita, setembro (tudo verde, chuva). No meio, um camponês bonequinho de queixo caído, metade suado e metade molhado. Texto: `MAIO` (branco) `→` `SETEMBRO` (ouro) ou `O MESMO PAÍS?`. Gatilho: antes × depois, o padrão com mais prova (seção 1.3). **Hipótese.**
2. **"O REI QUE CHOROU" (emoção, cap. 3 "O imperador arrependido").** Ashoka bonequinho, coroado, ajoelhado e chorando num campo de batalha (Kalinga) com a espada caída. Texto: `O REI` (branco) / `QUE CHOROU` (ouro). Gatilho: emoção forte num rosto e lacuna (por que um conquistador choraria?). Substitui o Gandhi (rosto famoso, mas sem lacuna, e fora do traço do canal). **Hipótese.**

Na troca, mantenha a regra de 1 elemento amarelo, os bonequinhos e no máximo 3 palavras. Gere as 2 de cada vídeo e suba no "Testar e comparar" junto com a atual, para medir contra a linha de base.

---

## 4. Custo e notas técnicas
- **fal.ai `fal-ai/nano-banana/edit`:** 6 imagens × US$ 0,039 = **US$ 0,234** (R$ 1,37 com câmbio de 5,8528), em `financas.consumo` id 61 (`ref_id` = 5). Uma chamada da 2ª tentativa do conceito 4 voltou HTTP 422 sem imagem e foi repetida logo depois com sucesso. Ela não entrou na conta: confira no painel do fal se foi cobrada.
- O nano-banana/edit respeita `aspect_ratio: "16:9"` e devolve 1344x768.
- **PIL:** nenhum Python da VPS tinha Pillow (`tools/.venv`, sistema e kokoro). Usei um venv temporário em `/tmp/thumbwork/venv` (uv), sem mexer no `tools/.venv`. Para rodar o `compose.py` de novo: `uv venv /tmp/x && VIRTUAL_ENV=/tmp/x uv pip install pillow`.
- **Fontes:** Libre Caslon e Open Sans não estão instaladas no sistema (`fc-list`), e o Remotion as baixa em tempo de render. Por isso usei os TTF variáveis do github google/fonts, guardados em `base/fonts/`. Nos variáveis do PIL, a ordem dos eixos do Open Sans é `[wght, wdth]`: `set_variation_by_axes([800, 100])`. Na ordem trocada, o texto sai em peso fino.
