# História em Minutos: ângulo "a história que ninguém conta" num país já postado. Go/no-go (20/11/2026)

## Resumo (10 linhas)
1. **Veredito: GO condicional.** Vale 1 vídeo-teste com **fato específico no título** (Egito). **NO-GO** para a frase genérica "a história que ninguém conta / não te contaram".
2. A demanda existe para o fato específico. No recorte "história de país" em pt, **46 canais pequenos e médios** (≤ 500 mil inscritos) têm vídeo ≥ 3× a mediana. Exemplos: [SPkPEubbFNg](https://youtu.be/SPkPEubbFNg) 807 mil · 194×, [TAWnMHlZc5s](https://youtu.be/TAWnMHlZc5s) 414 mil · 156×, [2aepgFPTBW0](https://youtu.be/2aepgFPTBW0) 142 mil · 291×.
3. A frase genérica rende menos. A mediana de views é **1.012**, contra **10.188** do fato específico (×med 1,79 × 1,86; 32% × 37% acima de 3×). Os hits genéricos são viagem, atualidade, podcast ou canal grande.
4. **Título × roteiro (ADENDO):** em 5 dos 6 vídeos transcritos, o "não contado" é **só embalagem**: é a linha do tempo de sempre ou nem é história. Conteúdo novo de verdade só apareceu no **recorte aprofundado** (Guararapes: 75% do tempo em fatos fora das "histórias completas").
5. Não há correlação entre "roteiro diferente" e ×mediana (WTF History "Cleopatra was GREEK" faz 236× com fato batido). O "não sabia" fica em 0–5% dos comentários em todos. Quem decide o clique é o fato do título.
6. **País nº 1: Egito.** Tem a maior demanda pt (25 vídeos ≥ 100 mil, ×med mediano 6,0) e é o nosso melhor vídeo (448 views, CTR 5,58%, 44,5% visualizado), o que serve de controle. Há **brecha real**: as "histórias completas" param em Cleópatra, e os 2.300 anos de donos estrangeiros não existem como tema em pt.
7. Depois vêm **Brasil** (demanda enorme, mas o ângulo "não contado" e o Brasil holandês já foram muito feitos) e **Irã** (demanda puxada pela guerra; "Pérsia → Irã" saturado).
8. 3 pares para o Egito, aprovados no **crivo independente na 3ª rodada: nota 80/100** (A 84 · B 76 · C 81). Fio condutor: Nilo → trigo → cobiça → novo dono vestido de faraó → até Nasser e Suez.
9. **Ressalva:** o nosso 001 já resume esses donos em ~45% dos blocos. O vídeo novo tem de aprofundar e trazer fatos que o 001 não tem (lista em `embalagem/EMBALAGEM.md`, obrigação 3), além de corrigir o erro de Plutarco do 001.
10. Achado lateral: um canal **homônimo**, "História em minutos" (UCuquAW2…, 5,9 mil inscritos, desde 09/10/2026), faz 270 mil com "Toda a história da Rússia em 37 minutos" (102×) e 202 mil com a França. Custo desta pesquisa: US$ 0 (yt-dlp, `videos.list` e Max).

Arquivos: `corpus.csv` (3.048 vídeos, 81+13 buscas, 1.530 canais com mediana), `dados/recorte_historia_pais.csv`, `dados/demanda_paises.txt`, `dados/analise-roteiro-*.md`, `dados/checagem-fatos-egito.md`, `transcricoes/`, `dados/comentarios/`, `mosaico.jpg`, `embalagem/` (EMBALAGEM, refs, crivos r1–r3), `CRIVO.md`, `scripts/`.

## Método
- Buscas yt-dlp via WARP (`ytsearch40`, lang pt/en/es), sem `search.list`. 94 consultas no total: 8 frases genéricas pt, 3 por país × 10 países (genérica, completa, curiosidades), 25 fatos específicos e "por que [país]", 10 "untold history of [country]" en, 3 es e 13 de colisão do ângulo por país (`scripts/consultas.json`).
- Números pelo `videos.list`. Mediana = últimos 30 longos (≥ 3 min, ≥ 7 dias) de cada canal, via `playlistItems` + `videos.list` (`scripts/coleta.py`). ×med = views ÷ mediana. Janela de 7 a 730 dias.
- Classes de título (`scripts/classes.py`, regex; revisão manual dos topos):
  - genérica: não contada, ninguém conta, segredo, lado sombrio, verdadeira história…
  - fato específico: "por que / como / quando / quase / achava…" com sujeito concreto;
  - completa: completa, inteira, em N minutos…
- Recorte "história de país": título com país ou império, ≥ 5 min, sem viagem, atualidade, podcast ou religião.
- **Limite:** a busca enviesa o corpus para o que procuramos, e o regex erra nas bordas. Os números são de ordem de grandeza.

## 1. O ângulo tem demanda?
| classe (pt, história de país) | n | ×med mediano | % ≥ 3× | views medianas | canais ≤ 500 mil com ≥ 3× |
|---|---|---|---|---|---|
| frase genérica | 105 | 1,79 | 32% | 1.012 | 28 |
| **fato específico** | 184 | 1,86 | 37% | **10.188** | **46** |
| completa (controle) | 139 | 2,56 | 46% | 5.070 | 45 |

**Prova mínima (≥ 3 canais pequenos/médios com ≥ 3×): cumprida, com folga, no fato específico.**
| vídeo | canal (inscritos) | views | idade | ×med | classe |
|---|---|---|---|---|---|
| [Por que o Brasil fala português enquanto toda América do Sul fala espanhol?](https://youtu.be/SPkPEubbFNg) | Revelando Brasil (6,5 mil) | 807.411 | 136 d | 194× | fato |
| [A Holanda Achava que o Nordeste Era Seu — Até Guararapes](https://youtu.be/TAWnMHlZc5s) | Legado esquecido (37,9 mil) | 413.977 | 156 d | 156× | fato (recorte) |
| [Recife nos anos 1630: Quando Era Holandesa](https://youtu.be/2aepgFPTBW0) | Relíquias Perdidas (28,3 mil) | 142.081 | 294 d | 291× | fato |
| [Por que os europeus nunca colonizaram o Japão?](https://youtu.be/SmVTBEPXjAE) | História do Mundo (11,4 mil) | 196.424 | 153 d | 265× | fato |
| [Antes dos Aiátolas: As Civilizações Que Fizeram o Irã…](https://youtu.be/RDE_kH3pfsY) | Cruzadas da Antiguidade (16 mil) | 35.885 | 515 d | 149× | fato |
| [O Dia em que Portugal se Mudou para o Brasil](https://youtu.be/qWPL11MOzOg) | Mundos Reimaginados (109 mil) | 782.332 | 249 d | 6,7× | fato |
| [O Lado SECRETO Da RÚSSIA](https://youtu.be/EUrzBzLSVaw) | Bello Mundo (313 mil) | 922.635 | 643 d | 42,9× | genérica (atualidade) |
| [A Verdade Sobre o IRÃ que Ninguém Conta](https://youtu.be/Gpk-Ef0XGqk) | Mundo Marcante (51,8 mil) | 148.208 | 316 d | 38,8× | genérica (turismo) |
| [O Fim do Antigo Egito: A Verdadeira História da Queda](https://youtu.be/dPfV5_tDCzo) | História do Mundo (17,9 mil) | 376.637 | 187 d | 20,4× | genérica (história) |
| [O BRASIL ANTES DE 1500: A HISTÓRIA QUE VOCÊ NUNCA APRENDEU](https://youtu.be/ZUt_OO_C4Eo) | Canal Nostalgia (15,2 mi) | 7.538.255 | 585 d | 6,8× | genérica (canal gigante) |
| en: [Cleopatra … Was GREEK](https://youtu.be/2XIvbXsbt58) | WTF History (211 mil) | 58.254 | 546 d | 236× | fato |
| es: [La historia secreta de España que nadie te contó](https://youtu.be/RPWwoN2CJ_4) | Crónicas Ocultas (12 mil) | 651.245 | 392 d | 2.326× | genérica |

**O que rende mais:** o fato específico no título. A frase genérica funciona em es e em canais de viagem/atualidade, mas em pt, para história de país, ela fica com canais grandes (Canal Nostalgia, PrimoCast) ou com vídeos que não são de história. Em en, "untold history of X" tem 59% acima de 3×, mas é outro mercado.

## 2. Qual país já postado tem o melhor espaço
Demanda pt = vídeos com o país no título nas buscas (≤ 24 meses, ≥ 5 min). Nosso vídeo: Studio 23/10–19/11 (`youtube.studio_video`, exportado em 20/11).
| país | vídeos pt / ≥ 100 mil | ×med mediano | "não contado" do país já feito? | nosso vídeo (views · CTR · % visto) |
|---|---|---|---|---|
| **Egito** | 66 / 25 | **6,0** | só a "queda" (376 mil · 20×; 2,0 mi · 2,3×), que **para nos faraós**; **o pós-faraó não existe em pt** (brecha) | 445 · **5,58%** · 44,5% |
| Brasil | 130 / 54 | 2,2 | **muito feito**: Canal Nostalgia 7,5 mi, PrimoCast 580 mil, 5+ sobre o Brasil holandês, Portugal no Rio 782 mil (colisão) | 103 · 3,60% · 43,0% |
| Irã | 162 / 56 | 2,4 | feito: "Pérsia → Irã" 2,1 mi + 8 cópias, "Antes dos Aiatolás" 149×; demanda inflada pela guerra de 2026 | 38 · 4,88% · 42,9% |
| China | 63 / 28 | 3,2 | pouco (Qing e mongóis aparecem nas completas) | 393 · 4,09% · 39,8% |
| Índia | 55 / 28 | 2,0 | "lado sombrio" de viagem; Companhia das Índias em en | 288 · 3,99% · 41,8% |
| Rússia | 50 / 9 | 1,9 | só atualidade ("lado secreto") | 39 · 7,49% · 42,6% |
| Roma, Alemanha, Japão, França | 34–67 / 7–20 | 1,4–6,3 | pouco | 3–20 · 1,3–3,4% |

**Top 3:**
1. **Egito**: maior demanda, brecha real no pós-faraó e controle forte (nosso melhor vídeo).
2. **Brasil**: a demanda prova o fato específico, mas há colisão alta e o nosso vídeo é fraco.
3. **Irã**: há demanda, mas ela é de atualidade, os ângulos estão saturados e o nosso 003 já é rico em fatos pouco contados.

## 3. Egito: pares, promessa, fio e fatos
Detalhes e thumbs descritas em `embalagem/EMBALAGEM.md`; crivo em `CRIVO.md` (r1 62 → r2 74 → **r3 80, aprovado 3/3**).
| par | título | thumb (padrão) | nota |
|---|---|---|---|
| A | O Egito passou 2.300 anos governado por ESTRANGEIROS (52) | general romano bonequinho no trono **pondo a coroa dupla**, escriba pasmo, cena clara, sem texto (`cena-acao`) | 84 |
| B | Por que o Egito esperou 2.300 anos por um EGÍPCIO? (50) | Pedra de Roseta grande com a **faixa grega circulada** e o rótulo "GREGO", escriba apontando (`documento-evidencia`) | 76 |
| C | Como o Egito virou o PRÊMIO de todo império (43) | **Nilo aceso em ouro** e 6 setas vermelhas de impérios convergindo, "POR QUÊ?" (`mapa-lugar`) | 81 |

- **Promessa:** quem mandou no Egito depois dos faraós e por quê, um dono depois do outro, até o primeiro egípcio voltar ao comando e retomar o "prêmio" (Suez, 1956).
- **Fio condutor (molde History in Minutes):** o Nilo dá trigo → o trigo atrai impérios → cada dono se veste de faraó → povo e língua continuam → "mas… então…" o próximo dono. "Guarde isso": a lenda de Nectanebo II pai de Alexandre; a Pedra de Roseta (3 donos estrangeiros num objeto); os mamelucos escravos que viram sultões (pagos em 1811).
- **Fatos-âncora** (checados em `dados/checagem-fatos-egito.md`):
  1. Nectanebo II, último faraó nativo do país inteiro, cai em **343 a.C.** ([Britannica](https://www.britannica.com/biography/Nectanebo-II)). No *Romance de Alexandre*, ele é o pai lendário de Alexandre.
  2. Hicsos: tomaram o poder **por dentro**, não por invasão (isótopos, 2020), e trouxeram cavalo e carro de guerra ([Smithsonian](https://www.smithsonianmag.com/smart-news/first-foreign-takeover-ancient-egypt-was-uprising-not-invasion-180975354/)).
  3. Faraós núbios: Piye c. 727 a.C. repreende um príncipe por deixar os cavalos com fome; Taharqa é o "Tiraca" de 2 Reis 19:9 ([NatGeo](https://www.nationalgeographic.com/history/article/nubian-pharaohs-kushite-ancient-egypt)).
  4. Ptolomeus: a maioria **nem tentou aprender egípcio** e Cleópatra falava (Plutarco, *Antônio* 27, [texto](https://www.yorku.ca/pswarney/Texts/antonius-25-29.htm)). Cleópatra viveu mais perto da Apollo 11 do que da Grande Pirâmide.
  5. Augusto aparece **como faraó, com nome em cartucho**, no Templo de Dendur ([Met](https://www.metmuseum.org/essays/temple-of-dendur-cult-and-decoration)). Senador só entrava no Egito com permissão do imperador, por causa do trigo ([Britannica](https://www.britannica.com/place/ancient-Egypt/Roman-and-Byzantine-Egypt-30-bce-642-ce)).
  6. Mamelucos, soldados-escravos que viraram sultões em 1250, vencem os mongóis em Ain Jalut em 1260 ([Britannica](https://www.britannica.com/topic/Mamluk)).
  7. Muhammad Ali, nascido em Kavala (hoje Grécia), de família albanesa, governa de 1805 a 1848; a dinastia cai em 1952/53 ([Britannica](https://www.britannica.com/biography/Muhammad-Ali-pasha-and-viceroy-of-Egypt)).
  8. Nasser: "o primeiro egípcio de verdade a governar o país em vários milênios" ([Britannica](https://www.britannica.com/biography/Gamal-Abdel-Nasser/Nassers-accomplishments)). Ressalva: houve faraós rebeldes nativos no sul em 205–186 a.C.
- **Obrigações para o roteiro:** pagar o fato até 0:30 e o "prêmio" até 1:00; ≥ 60% do tempo depois de 30 a.C.; nenhuma frase do 001; 1 fato novo por era. Detalhes no EMBALAGEM.

## 4. Título × roteiro (ADENDO)
Transcrições automáticas (yt-dlp + WARP) de 7 vídeos do formato, contra 5 "histórias completas" do mesmo país + os nossos roteiros 001, 003, 005 e 007. Comentários: até 300 por vídeo. Análises por país em `dados/analise-roteiro-{egito,ira,brasil-russia}.md`.
| vídeo | ×med | duração | % do tempo em fatos fora das completas | fio condutor | promessa paga | % "não sabia" | veredito |
|---|---|---|---|---|---|---|---|
| Guararapes (TAWnMHlZc5s) | 156× | 28 min | **~75%** | sim (azarão × superpotência) | sim (7:46, 18:06) | 2% | **conteúdo diferente (recorte)** |
| Brasil fala português (SPkPEubbFNg) | 194× | 8 min | ~29% | sim (a pergunta) | sim (4:30–7:07) | 1–2% | misto: a pergunta vende, ~70% é matéria escolar |
| Fim do Antigo Egito (dPfV5_tDCzo) | 20× | 80 min | 16% (46% com os trechos que as completas resumem em 1 frase) | sim (queda por dentro) | sim (39 min) | 1,8% | misto |
| Cleopatra was GREEK (2XIvbXsbt58, en) | 236× | 13 min | 23% (casos laterais) | não | **não** (não trata a Cleópatra) | — | só embalagem |
| Antes dos Aiatolás (RDE_kH3pfsY) | 149× | 20 min | 27% | fraco | parcial (aiatolás nunca aparecem) | 3% | só embalagem (leve) |
| Verdade sobre o Irã (Gpk-Ef0XGqk) | 39× | 50 min | 4% (o resto é turismo) | não | não (23% dos comentários reclamam) | 0% | outro gênero |
| Lado secreto da Rússia (EUrzBzLSVaw) | 43× | 20 min | ~3% de história (top 10 de atualidade) | não | parcial | 1% | não é história |

**Conclusão:**
- O ângulo, como o mercado faz, é **quase só embalagem**: o título promete segredo e o roteiro repete a linha do tempo (ou nem é história).
- O público clica no fato e não cobra novidade ("não sabia" ≤ 5% em todos). Quando a promessa é traída, ele reclama (Irã: 23% dos comentários).
- O único caso de conteúdo novo de verdade é o **recorte aprofundado com fio** (Guararapes), também com ×med alto.
- Para nós: o ângulo é **real se o roteiro for recorte**. No Egito, "depois dos faraós" é exatamente o trecho que as completas espremem.
- O título carrega o clique; o roteiro diferente é o que pode segurar a retenção e ganhar o "Testar e comparar", que decide por tempo de exibição.

## 5. Veredito: GO condicional
- **Por quê (3 linhas):**
  1. Fato específico no título tem prova em pt: 46 canais pequenos/médios com ≥ 3× e 10× as views medianas da frase genérica, que fica saturada e com canais grandes.
  2. O Egito tem a brecha que o formato pede: as completas param em Cleópatra e o pós-faraó é um recorte real, com fatos checados. O crivo deu 80/100 e é o nosso melhor vídeo, o que permite comparar mesmo país × ângulo novo.
  3. O ganho esperado é **CTR e impressões** (nosso gargalo, com CTR médio de 4,59%), não retenção. Medir CTR e views no dia 7 contra o 001.
- **Condições:**
  - título de fato específico, nunca "a história que ninguém conta";
  - roteiro de recorte que paga em até 1 min e não reaproveita o 001;
  - se o teste não passar do 001 em CTR e views no dia 7, o ângulo morre.
- **Se fosse no-go**, a alternativa seria o recorte por pergunta concreta sem a moldura "não contado" ("Por que o Brasil fala português…", 194×), que já cabe no título-pergunta da bíblia.
- **Fila desta noite:** este job não mexe em fila, backlog nem bíblia. Para entrar hoje, o vídeo precisa de linha em `youtube.videos` e dos briefs e1/e2 (decisão do Rodrigo). A embalagem aprovada está pronta para ser copiada para `videos/NNN-egito-estrangeiros/`.
