# Embalagem padrão-ouro: grupo "geral" (8 canais gigantes)

17/11/2026 · canais: MrBeast, Ryan Trahan, Mark Rober, Veritasium, Kurzgesagt, Johnny Harris, MagnatesMedia, Yes Theory.
Fonte: `corpus/<canal>.csv` (top por views em ~2 anos + recentes; ×med = views ÷ mediana real dos últimos 30 longos), os 16 mosaicos (normal e 160×90) e 13 thumbs individuais de flops (×med < 1).
Método: 180 títulos "top" classificados à mão (1 estrutura principal cada) + estatística em Python; 80 thumbs (top 10 × 8 canais; Magnates 10 de 14) anotadas a olho.
**Viés:** o "top" foi escolhido por views, então ×med > 1 é esperado; vale comparar estruturas **dentro** do canal (índice relativo) e hit × flop do mesmo canal.

---

## 1. Título

### 1.1 Estruturas no top (n = 180)
| Estrutura | n | med ×med | índice relativo* |
|---|---|---|---|
| curiosidade/lacuna ("Why…", "The REAL reason", "Truth about", "Inside", "Explained") | 47 | 1,36 | 1,05 |
| "Eu fiz X"/1ª pessoa | 36 | 1,90 | 0,97 |
| afirmação estranha ("Alcohol is AMAZING", "There Is Something Faster Than Light") | 24 | 1,51 | 1,02 |
| superlativo ("World's Most…", "Most Isolated", "Biggest") | 21 | 1,38 | 0,94 |
| pergunta | 16 | 1,57 | 1,05 |
| desafio/aposta ("Survive X, Win $", "Last to Leave") | 15 | 1,42 | 1,01 |
| vs/escala ("$1 vs $1,000,000,000") | 10 | 1,40 | 0,97 |
| número extremo/dinheiro ("The $47 Billion Cult") | 6 | 1,49 | 1,07 |
| contraste/antes×depois | 4 | 0,91 | 0,84 |

*índice = ×med do vídeo ÷ mediana do ×med do top do mesmo canal (tira o efeito "Ryan Trahan tem ×med 5–11").
**Leitura:** normalizada por canal, toda estrutura dá ~1,0. **A estrutura não faz o hit; ela é a assinatura do canal.** Cada canal usa 1–2 estruturas quase sempre:

| Canal | Estrutura dominante no top |
|---|---|
| MrBeast | desafio/aposta 13/25, vs 6 |
| Ryan Trahan | "I Tested/Tried/Took" 20/25 |
| Mark Rober | 1ª pessoa 7/16 |
| Veritasium | afirmação estranha 7 + lacuna 7 + superlativo 5 (de 25) |
| Kurzgesagt | afirmação estranha 10 + lacuna 10 (de 25) |
| Johnny Harris | lacuna 16/25 ("The REAL reason", "What's ACTUALLY happening", "Explained") |
| Magnates | afirmação estranha 4 + superlativo 4 + "INSANE/DISTURBING TRUTH" 3 (de 14) |
| Yes Theory | superlativo 9 + lacuna 8 (de 25), "Most Isolated/Dangerous" |

### 1.2 Tamanho (n_chars)
| Grupo | n | mediana |
|---|---|---|
| top (todos) | 180 | **40** |
| recentes abaixo da mediana (×med < 1) | 31 | 44 |
| hits (×med ≥ 1,5, todo o corpus) | 89 | **39** |
| flops (×med < 0,7) | 25 | **46** |

Por canal (top × recentes < 1): Ryan 38 × 52 (série "Top 10 Places - Cidade"), Veritasium 45 × 48, MrBeast 37 × 38, JH 38 × 39,5. Exceções: Yes Theory vive de títulos longos (top 58: `"he's crazy" - …(39 years isolated)`) e Kurzgesagt tem flops curtos e vagos ("Dying Is Complicated", 20).
**Faixa de ouro: 30–45 caracteres.** Passar de 50 só com um gancho entre parênteses/aspas (padrão Yes Theory).

### 1.3 Marcadores (contagem de títulos)
| Marcador | top (180) | hits (89) | flops (25) |
|---|---|---|---|
| número ou $ | 35% | 33% | 52% |
| moeda/Billion/Trillion | 16% | 13% | 12% |
| termina em "?" | **10%** | 10% | 16% |
| palavra em CAIXA ALTA (INSANE, REAL, TRILLION) | 9% | 8% | 8% (0% nos recentes < 1) |
| superlativo/Every/Top N | 23% | 21% | 44% |
| começa com "I/We" | 21% | 28% | 52% |
| parênteses de reforço | 9% | 8% | 0% |

- **Pergunta no fim é rara** (10%) e não protege: nos flops aparece mais (16%).
- Número e superlativo **sozinhos não salvam**: aparecem mais nos flops ("I Visited the Top 10 Places…", "$250,000 Hunger Games In Real Life" 0,48×).
- CAIXA ALTA numa palavra só (REAL, ACTUALLY, INSANE, TRILLION) é tempero de JH/Magnates/Kurzgesagt; nenhum recente fraco usou.

**Palavras de poder recorrentes no top:** Most (16), Days/Hours (23, unidade de tempo = prova de esforço), World/World's (14), Survive/Survived (9), Win (8), Every (8), America (8), Inside (7), Truth (5), Real (5), Actually (5), Insane (4), Explained (4), Isolated (4), Dangerous (4), Secret (3), Illegal (3), No One Knew (2).

---

## 2. Thumb (top 10 × 8 canais = 80)

### 2.1 Frequências
| Atributo | Contagem | Nota |
|---|---|---|
| elemento dominante: rosto + emoção | 44/80 | MrBeast 10, Rober 8, JH 8, Magnates 6, Yes 6, Ryan 4, Veritasium 2, Kurzgesagt 0 |
| objeto (máquina, semente, logo, seringa) | 16/80 | Veritasium 6, Kurzgesagt 6, Magnates 3 |
| cena/lugar | 20/80 | Ryan 6, Kurzgesagt 4, Yes 4 |
| número como elemento dominante | 0/80 | número só como texto ("DAY 29", "-36C°", "$3.5K") |
| ≤ 2 focos | 64/80 | 3+ focos só em JH (rosto+mapa+bandeiras) e cenas de multidão |
| tem texto | 47/80 (59%) | Rober 0/10, MrBeast 5, Magnates 4, JH 6, Ryan 7, Yes 7, Veritasium 9, Kurzgesagt 9 |
| palavras no texto | 1–4 (mediana 2) | nunca > 4 |
| texto repete o título | 10/47 (21%) | Kurzgesagt 3 ("FENTANYL", "GRAVASTARS"), JH 3 ("MIDDLE EAST EXPLAINED"), Yes 2, Mag 1, Ver 1 |
| texto completa sem repetir | 37/47 (79%) | MrBeast, Ryan e Rober: 100% |
| desfecho pendente/tensão | 62/80 | Rober 10, MrBeast 9, Ryan 8, Ver 8, Yes 8, Kurz 7, JH 6, Mag 6 |
| escala (enorme/minúsculo) | 11/80 | pirâmide com bonequinhos (MrBeast), torre Eiffel minúscula sob baleia (Kurz), homem pequeno sob prédios vazios (Yes) |
| seta/círculo/zoom | 13/80 | Ver 3, Rober 3, Kurz 2, JH 2, Yes 2 |
| lê a 160×90 | 75/80 | falham: cenas largas sem foco (Ryan "First Class", JH "Saudi Arabia" com letra espaçada fina) |

### 2.2 Assinatura visual por canal
| Canal | Fórmula |
|---|---|
| MrBeast | rosto em careta (dentes, olhos arregalados) + oponente/objeto + "DAY N" no canto; cor saturada clara |
| Ryan Trahan | rosto sério, quase neutro, numa cena absurda; card de review 1 estrela ("LOCK WINDOW") ou "day 6" grande |
| Mark Rober | rosto + engenhoca no instante antes do desfecho (carro contra a parede pintada, pulo no trem); seta vermelha; zero texto |
| Veritasium | fundo preto, objeto real, 1–4 palavras serifadas brancas com sublinhado vermelho: juízo ("This shouldn't exist.", "How was this allowed?") |
| Kurzgesagt | ilustração saturada sobre escuro, 1 foco, 1–3 palavras CAIXA ALTA no topo ("WE LOST CONTROL", "LOST FOREVER") |
| Johnny Harris | rosto dele (sério, olhando à câmera) + mapa vermelho ou rosto de líder (Hitler censurado, Xi, Musk); paleta vermelho/preto |
| Magnates | rostos ilustrados hiper-reais com olhos brilhando, logo da marca, dinheiro/fogo/sangue |
| Yes Theory | rosto desconfiado + lugar real + pergunta curta ("WHY IS IT EMPTY?", "SCAM? PARADISE?"); logo fixo |

---

## 3. Relação título × thumb
- Repete palavra do título: **10/47** thumbs com texto (21%); 33/80 nem têm texto (a imagem é o complemento).
- Regra dominante: **título = assunto/promessa; thumb = reação, prova ou o nome escondido.**

5 exemplos de "completa sem repetir":
1. "Why Farmers Can't Legally Replant Their Own Seeds" · Veritasium · 23,2 mi · 2,24× → semente com "DO NOT PLANT" carimbado.
2. "Inside the Most Prepared Country on Earth" · Johnny Harris · 6,1 mi · 1,61× → "FINLAND" (o título esconde o país, a thumb entrega).
3. "The Nazi Brothers Who Started Rival Shoe Companies" · Magnates · 1,67 mi · 3,45× → logos adidas | PUMA sobre 2 meninos fardados.
4. "The Biggest Chemical Coverup In History" · Veritasium · 37,7 mi · 3,64× → garfo de Teflon + "How was this allowed?".
5. "I Tested 1-Star Hotels (finale)" · Ryan Trahan · 28,1 mi · 6,49× → review 1 estrela "LOCK WINDOW" + silhueta na janela.
(+ "AI Just Crossed the Terrifying Line - Now What?" · Kurzgesagt · 24,1 mi · 4,31× → "WE LOST CONTROL"; "Exploring the World's Largest $100 Billion Failed Ghost City" · Yes · 10,8 mi · 3,01× → "WHY IS IT EMPTY?")

---

## 4. Hit (≥ 1,5×) × flop (< 0,7×) no mesmo canal
1. **Sujeito nomeado e aposta alta × genérico.** "Beat Ronaldo, Win $1,000,000" · MrBeast · 416,7 mi · 2,80× contra "Beat Professional Athlete, Win $100,000" · MrBeast · 99,4 mi · 0,67×: mesmo formato e mesma thumb de careta (com Haaland), mas o título troca o nome por categoria e o prêmio cai 10×. JH: "The REAL reason the US can't beat Iran" · 6,6 mi · 1,76× contra "The world's most extreme places, explained" · 0,8 mi · 0,21×.
2. **Série, episódio e compilação matam.** "I Took the Longest Train Ride in America" · Ryan · 28,0 mi · 6,49× contra "I Visited the Top 10 Places in America - Grand Canyon" · Ryan · 1,7 mi · 0,40× (53 caracteres, todos os 8 episódios entre 0,40 e 0,63×). JH: "How the Mormon Church Made $293 Billion" · 4,4 mi · 1,16× contra "The Real Story Behind the Mormon Church" (thumb "[COMPILATION]") · 1,3 mi · 0,35×; "Why Egypt Guards This River With an Army" · 0,72× com thumb de pôster "THE HUMAN ELEMENT – EPISODE 1".
3. **Thumb sem conflito nem desfecho pendente.** "I Saved 1,000 Animals From Dying" · MrBeast · 256 mi · 1,72× (leão ferido, "ANIMAL #967") contra "I Granted 100 Kids Their Biggest Wish!" · MrBeast · 77,4 mi · 0,52× (foto posada sorrindo com The Rock, nada a resolver). "$250,000 Hunger Games In Real Life" · 0,48×: arco e flecha, sem oponente, sem número, sem texto. JH no Ártico ("extreme places", 0,21×): só retrato, sem mapa nem objeto.
4. **Pergunta de aula × risco/tabu/culpa.** "Why Does Fentanyl Feel So Good?" · Kurzgesagt · 14,4 mi · 2,56× contra "How Are Memories Stored Inside Your Brain?" · 3,7 mi · 0,65×. "The Biggest Chemical Coverup In History" · Veritasium · 3,64× contra "Why does every mammal get 1 billion heartbeats in their life?" · 6,9 mi · 0,67× (61 caracteres). O hit tem vilão, perigo ou proibição; o flop tem dúvida escolar.
5. **Título sobre o próprio canal.** "We're trying something new..." · Veritasium · 0,14×; "our secret project is finally out" · Yes · 0,15×; "We're saying goodbye to Seek Discomfort" · Yes · 0,24×. (Exceção: "We need to talk" · Ryan · 1,62×, notícia pessoal de um rosto conhecido.)
Bônus: flops têm títulos mais longos (mediana 46 × 39 nos hits).

---

## 5. O que se transfere para canais SEM ROSTO (história/geografia/dossiê narrados)
Os mais próximos: Kurzgesagt (sem rosto, ilustrado), Johnny Harris e Magnates (narrados, mapa e personagem), e Veritasium nas thumbs sem rosto (objeto + frase).

1. **Rosto com emoção continua sendo o motor (44/80), mas vem do personagem, não do apresentador.** Magnates põe Altman × Musk e os irmãos Dassler fardados; JH põe Hitler censurado, Xi, Trump × Xi. Para nós: o personagem histórico ou bonequinho com raiva/medo, cara a cara com o rival (confirma o COROA × TURBANTE do historia-ptbr).
2. **Molde Kurzgesagt para thumb ilustrada:** 1 foco ilustrado saturado sobre fundo escuro + 1–3 palavras CAIXA ALTA no topo com o **veredito**, não o tema ("LOST FOREVER", "WE LOST CONTROL", "IT'S IMPOSSIBLE*"). Repetir o tema só quando o tema é a curiosidade ("FENTANYL").
3. **Molde Veritasium para dossiê:** fundo preto, objeto ou documento real, frase curta de juízo em 1ª pessoa ou retórica ("How was this allowed?", "We cracked it", "NOT A MYSTERY" sobre recortes de jornal em "What Actually Happened To Amelia Earhart?" · 15,4 mi · 1,49×). Combina com carimbo do dossie-es.
4. **Mapa como protagonista, só se tiver ação:** área em vermelho + círculo de zoom/foto de satélite ("What's ACTUALLY Happening in North Korea" · JH · 5,9 mi · 1,57×; "50 hours in a Secret Russian town in America" · Yes · 11,1 mi · 3,09×). Mapa parado (panorama + nome do país) é o padrão que já falhou no nosso CTR < 2%.
5. **A thumb entrega o nome que o título esconde** (logo, bandeira, nome do país): "Inside the Most Prepared Country on Earth" + "FINLAND"; "The Nazi Brothers…" + adidas | PUMA. Título com lacuna, thumb com a chave: zero repetição.
6. **Moldes de título que servem para história/dossiê** (sujeito nomeado + risco + 30–45 caracteres):
   - "[Coisa] esteve a [dias] do desastre e ninguém soube" ← "This Skyscraper Was Days From Collapsing And No One Knew" · Veritasium · 26,4 mi · 2,55×.
   - "Por que [coisa banal] era mortal antes de [ano]" ← "Why Cold Drinks Were Deadly Before 1914" · Veritasium · 12,3 mi · 1,19×.
   - "A razão REAL de [potência] não conseguir [X]" ← "The REAL reason the US can't beat Iran" · JH · 1,76×.
   - "O culto de US$ 47 bilhões" / número concreto ← "The $47 Billion Cult" · Magnates · 2,0 mi · 4,16×; "…374,142 Bunkers…" · Yes · 2,74×.
   - "Os irmãos [X] que [fato improvável]" ← "The Nazi Brothers Who Started Rival Shoe Companies" · 3,45×.
7. **Evitar** (todos com flop documentado): "Explicado" sem sujeito forte, "Episódio 1"/série, compilação, pergunta de aula sem vilão, título sobre o canal, categoria genérica no lugar do nome ("um atleta profissional", "os lugares mais extremos").
8. **Escala e estado pendente são baratos de ilustrar e raros (11/80):** objeto gigante com algo minúsculo de referência (baleia × torre Eiffel; asteroide "NORMAL" × cidade). Em história: exército enorme × um homem; muralha × um cavaleiro. E sempre congelar **antes** do desfecho (62/80 têm tensão pendente).
9. **Teste do celular:** 75/80 leem a 160×90; os que falham são cenas largas sem foco e letras finas espaçadas. Uma cor quente (vermelho/amarelo) sobre fundo escuro é o contraste dominante de Kurzgesagt, JH e Veritasium.
10. **Coerência de canal > fórmula do mês:** a estrutura de título não explica o hit (índice ~1,0 em todas); o que explica é sujeito específico + aposta + thumb pendente dentro da assinatura fixa do canal. Para nós: cada bíblia define 1–2 estruturas e um layout fixo de thumb; o vídeo varia o sujeito e a tensão.
