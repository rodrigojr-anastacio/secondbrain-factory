# Em Relevo, rodada 2: 3 candidatos EVERGREEN de "pergunta grande" (17/11/2026)

Brief: `~/workspace/referencias/BRIEF-em-relevo-proximos-r2.md`. A rodada 1 (`pesquisa/em-relevo-proximos-2026-11-17/`) foi recusada por "parecer notícia". Esta rodada busca a linha do O Mundo e Tudo ao Redor: "e se / qual o maior / quanto / por quê", sobre a Terra e o Brasil, com retorno de longo prazo. Espaço ficou fora.

Coleta em 17/11/2026, entre 22h e 0h UTC:
- autocomplete do YouTube via WARP: 88 prefixos em pt, en e es;
- yt-dlp via WARP: 162 buscas em 30 perguntas (pt e en/es), janela de 5.000 dias, ou seja, vídeos antigos entram;
- Data API: `videos.list`/`channels.list`/`playlistItems`, ~2 mil unidades, sem `search.list`;
- 3 snapshots de views dos 121 vídeos-evidência;
- manada transcrita (legendas automáticas);
- crivo do clique feito por 2 subagentes sem o meu contexto.

Google Trends respondeu 429 e ficou de fora. Custo: US$ 0.

## Resumo (10 linhas)
1. **Banco:** 30 perguntas varridas, 22 no `banco.csv` com status. Todas saíram de evidência: autocomplete, títulos que explodiram e vídeos antigos que seguem rendendo.
2. **Filtro evergreen:** o tema passa se tiver ≥ 3 vídeos com ≥ 1 ano e ≥ 100 mil views, de canais diferentes, publicados em anos diferentes. Passaram 16 das 22. Caíram as "ondas" (Rio Madeira, Amazônia profunda: hits de 6 semanas, sem histórico) e os temas que não puxam em pt (Amazonas ao contrário: 6 de 6 vídeos pt de 2026 com < 1,2 mil views).
3. **Crivo do clique:** 13 candidatas foram para 2 avaliadores independentes. Os dois deram "SIM convicto" só a 4: Itaipu, Tsunami, Trens e Zero pontes. O padrão das que pegam: ameaça ou falta em algo que o brasileiro conhece, mais um número concreto. As que soam como "aula de escola" (Encontro das Águas, Nilo × Amazonas, origem de SP) caíram.
4. **#1 "O que aconteceria se ITAIPU rompesse?"** A sugestão aparece no autocomplete genérico de "o que aconteceria se", e em pt quase não existe vídeo: o único direto (Fivertix, 2,5 mil inscritos) fez **103× a mediana**. Em en, o mesmo "e se" com a Três Gargantas tem 1,56 mi, 901 mil e 729 mil views. O mapa 3D é a resposta: a onda descendo o vale do Paraná.
5. **#2 "Um TSUNAMI pode atingir o Brasil?"** É feito em pt desde 2017 e volta a render a cada notícia:
   - Beto Fazanaro, 2.306× (2017);
   - Geografia Irada, 2.144× (2021);
   - Fatos Desconhecidos, 635 mil (set/2026);
   - Naked Science (La Palma), 4,25 mi em 9 anos.

   Nosso ângulo: a onda sobre batimetria real e o tsunami de 1755, que chegou a PE e PB (artigo de 2022, UERJ).
6. **#3 "Por que o Brasil não tem TRENS?"** Rende há 6 anos (BBC 1,13 mi em 2021, Fatos 2,09 mi em 2022, CTD 1,29 mi em 2025), e um canal de 11,9 mil inscritos ainda fez 90× em jan/2026. A manada explica pelo rodoviarismo e pela bitola. Nosso ângulo é o relevo: a Serra do Mar, com 796 m de paredão em Paranapiacaba, e os rios que correm para o interior.
7. **Reservas:**
   - "Por que o MAIOR rio do mundo não tem nenhuma ponte?" Clique forte e evergreen (2,65 mi em 2023), mas há 8 clones pt em out–nov/2026, todos com < 1,3 mil views.
   - "O Brasil já tremeu 1.815 vezes": o crivo deu "talvez"; só funciona com o número na thumb.
8. **Descartados mais tentadores:**
   - "Brasil quando o mar era 120 m mais baixo": o crivo disse que um vizinho do feed já ocupa o lugar ("Era do Gelo no Brasil", 1,16 mi), e o tema fica perto do OMTR de 15/11.
   - "E se o Atlântico secasse": O Mapa Não Mente fez 574 mil há 8 dias, e o crivo deu NÃO/NÃO.
   - "Encontro das Águas": "vi na escola".
9. **Nenhum dos 3 repete o OMTR** (`canal.csv`: 17 títulos, quase todos de espaço e oceano). Todos têm ≥ 55% de tela possível em material livre mais mapa 3D (Commons: Itaipu 313 + Paraná 376; La Palma 2021 152; Paranapiacaba 870 + ferrovias 487), sem depender de foto creditada.
10. **Riscos:**
    - Itaipu: não achei estudo público de ruptura. O "até onde" pede um cenário próprio, rotulado HIPOTÉTICO e sem alarmismo.
    - Tsunami: o cenário de La Palma (Ward & Day 2001) é contestado, e o vídeo tem que dizer isso.
    - Trens: o relevo é parte da resposta, não toda. O título não pode dizer "a serra matou".

---

## 1. Método
- **Banco (pergunta 1 do brief):** o autocomplete (`autocomplete/sugestoes.json`) deu as perguntas que o brasileiro digita, por exemplo:
  - "o que aconteceria se a barragem de itaipu rompesse"
  - "porque o brasil não tem terremoto/vulcão/furacão/tsunami/ferrovias"
  - "o brasil já teve tsunami"
  - "e se o mar secasse"
  - "porque o rio amazonas não tem ponte"
  - "porque o pacífico e o atlântico não se misturam"

  Os títulos que explodiram (OMTR, Manicule, Régua, RealLifeLore, Wendover, Ciência Todo Dia, e o corpus de `pesquisa/embalagem-padrao-ouro-2026-11/`) deram o formato. As perguntas e consultas estão em `perguntas.tsv` e os resultados em `q/<pergunta>/{pt,int}/refs.csv` (views, idade, mediana do canal, ×mediana).
- **Evergreen (pergunta 2):** para cada pergunta separei 2 a 10 vídeos-evidência relevantes (`evidencias.tsv`) e medi idade, views, views/dia da vida e views/dia de hoje (`evergreen.csv`). Para views/dia de hoje, há 3 snapshots dos 121 vídeos (`snap1.json`, `snap2-48min.json`, `snap3.json`; ver §4).
- **Brecha em pt-BR (pergunta 3):** quem já fez em pt, quando e com quantas views ×mediana; o que só existe em en/es; colisão com o OMTR.
- **Clique (pergunta 4):** `crivo/CANDIDATAS.md` traz 13 candidatas, cada uma com 2 títulos e 1 thumb, colocadas como 11º vídeo de um feed com 10 vídeos reais do nicho. Dois subagentes sem o meu contexto avaliaram: `crivo/PARECER-curioso.md` (espectador de 28 anos) e `crivo/PARECER-cetico.md` (estrategista de CTR). Só passou o que levou "SIM convicto" nos dois.
- **Visual (pergunta 5):** contagem nas categorias do Commons (API), NASA EO e dados abertos.

## 2. Ranking
| # | Pergunta | Evergreen (≥ 1 ano, ≥ 100 mil) | Brecha pt-BR | Crivo (2 avaliadores) | Material livre | Risco |
|---|---|---|---|---|---|---|
| 1 | **O que aconteceria se Itaipu rompesse?** | 6 vídeos, 6 canais, de 2020 a 2024 | **tema vazio** (1 vídeo direto, 103×) | SIM / SIM (o 1º dos dois) | alto | cenário próprio, sem estudo público |
| 2 | **Um tsunami pode atingir o Brasil?** | 7 vídeos, 7 canais, de 2017 a 2025 (5 em pt) | ângulo (batimetria + 1755) | SIM / SIM | alto | hipótese de La Palma contestada |
| 3 | **Por que o Brasil não tem trens?** | 5 vídeos, 5 canais, de 2020 a 2025 (todos pt) | ângulo (relevo) | SIM / SIM | alto | relevo é só parte da resposta |
| R1 | Por que o maior rio do mundo não tem ponte? | 5 vídeos, 5 canais, de 2023 a 2025 | saturado agora | SIM / SIM | alto | 8 clones pt flopando em out–nov/2026 |
| R2 | O Brasil já tremeu 1.815 vezes | 4 vídeos, 4 canais, de 2017 a 2024 (todos pt) | ângulo (catálogo) | talvez / talvez | médio (pouca foto) | "o espectador já sabe" |

### #1 O que aconteceria se ITAIPU rompesse?
- **Títulos:**
  - T1 "O que aconteceria se ITAIPU rompesse?" (37 caracteres). É a frase exata do autocomplete, no formato OMTR com 1 palavra em caixa alta; os 2 avaliadores escolheram este.
  - T2 "Se Itaipu rompesse, até onde a água chegaria?"
- **Thumb:** vale do Paraná em relevo 3D real, escuro; a barragem com uma rachadura vermelha; uma mancha azul descendo o vale; "ATÉ ONDE?". O cético alertou que um pino com nome some em 160 px, então vai só a mancha e o texto. O curioso sugeriu pôr o tempo ("9 H"), se o cenário der o número.
- **Evergreen (3 números):**
  - [youtu.be/BVNfOps722Q](https://youtu.be/BVNfOps722Q), Megaprojects, "What Would Happen if the Three Gorges Dam Failed?": 1,56 mi, 2,3 anos, 1,9 mil/dia na média da vida.
  - [youtu.be/RjHWkCdZdOE](https://youtu.be/RjHWkCdZdOE), simulação de ruptura da Três Gargantas: 901 mil, 6,3 anos, 36,6× a mediana, ainda ~390/dia na média.
  - [youtu.be/RkWSWAaWweQ](https://youtu.be/RkWSWAaWweQ), INCRÍVEL, "E se as maiores barragens do mundo rompessem" (pt): 221 mil, 2020, 61,6×.
  - O gênero "barragem rompendo" é perene: [lYbFLBqJXVc](https://youtu.be/lYbFLBqJXVc) tem 23,4 mi em 4 anos e ainda ganha ~2,6 mil/dia; [DRyU5YjEmnY](https://youtu.be/DRyU5YjEmnY), pt, tem 5,36 mi (17×) e ~3,5 mil/dia hoje.
- **Brecha pt-BR:** o único vídeo direto é [youtu.be/-RS4gFjLgYM](https://youtu.be/-RS4gFjLgYM) (Fivertix, 2,48 mil inscritos, mai/2026): **27,4 mil = 103× a mediana do canal (265)**. É prova de que o tema puxa sozinho, num canal minúsculo. Ninguém em pt fez a simulação sobre o relevo. O que existe em pt sobre Itaipu é turismo ou engenharia (Manual do Mundo 12,4 mi e 2,7 mi; TV Brasil 1 mi). Em en, o "e se" da Três Gargantas está feito há 6 anos.
- **Autocomplete:**
  - "o que aconteceria se a barragem de itaipu rompesse" (11ª sugestão do prefixo genérico "o que aconteceria se")
  - "e se itaipu rompesse"
  - "se a itaipu estourar"
- **Ângulo / roteiro (gancho):** começa pelo tamanho: 29 bilhões de m³ represados, e o vale estreito de basalto logo abaixo. Depois, o que o relevo faz com a onda:
  - Foz e Ciudad del Este de frente para o canal;
  - a garganta do Paraná segura e acelera a água;
  - a planície a partir de Corrientes espalha;
  - Yacyretá, a próxima barragem, entra na conta;
  - por fim, Rosário e Buenos Aires.

  Fecha com "por que isso quase não pode acontecer": monitoramento, tipo de barragem e histórico, o que dá o tom anti-alarmista. Os números (volume, tempos, alturas) são para conferir na etapa 1.
- **Material (estimativa: ~60% da tela real mais mapa 3D):**
  - (a) livre:
    - Commons: `Itaipu Dam` 313 arquivos, `Itaipu Reservoir` 41, `Paraná River` 376;
    - Copernicus DEM/SRTM de 30 m do vale até o estuário;
    - Sentinel-2 e Landsat (lago antes e depois de 1982, Sete Quedas submersa);
    - vazões da ANA e do ONS;
    - Agência Brasil (CC BY; conferir foto a foto).
  - (b) com crédito: banco de imagens da Itaipu Binacional, vídeos do vertedouro.
  - (c) TV.
- **Risco:** não achei estudo público de ruptura (dam break) de Itaipu nem de Yacyretá. O "até onde" precisa de um cenário nosso, com hidráulica simplificada sobre o relevo e o selo "CENÁRIO HIPOTÉTICO" (como a Régua faz), ou de um PAE oficial, se houver. É tema sensível (binacional, gera medo), então o roteiro precisa da seção "por que é improvável".

### #2 Um TSUNAMI pode atingir o Brasil?
- **Títulos:**
  - T1 "Um TSUNAMI pode atingir o Brasil?" (33 caracteres; o preferido do cético).
  - T2 "A ilha que pode mandar uma onda gigante até o Brasil" (o preferido do curioso).
  - Variante com o fato novo: "O dia em que um tsunami atingiu o Brasil (1755)".
- **Thumb:** globo escuro no Atlântico; La Palma grande, em vermelho, com o nome; anéis de onda chegando ao Nordeste.
  - O texto que o crivo testou foi "8 HORAS". Não está confirmado: a fonte dá 8–9 h só para a Flórida.
  - Alternativa já provada: **"JÁ ACONTECEU"** (1755).
- **Evergreen (3 números):**
  - [youtu.be/6utAunBKXV4](https://youtu.be/6utAunBKXV4), Naked Science, "Megatsunami Scenario – La Palma": 4,25 mi, 9,4 anos, 323× a mediana, 1,2 mil/dia na média da vida.
  - [youtu.be/-e4ugB-2go4](https://youtu.be/-e4ugB-2go4), Beto Fazanaro, "Tsunami pode atingir o Brasil" (pt): 586 mil, 2017, **2.306×** (9,3 mil inscritos).
  - [youtu.be/uHE9D0AB1Mo](https://youtu.be/uHE9D0AB1Mo), Geografia Irada (pt): 326 mil, 2021, **2.144×**.
  - Mais:
    - Fala Brasil, 1,69 mi (2018);
    - Lamartine Posella, 385 mil (2021);
    - Fatos Desconhecidos, [aDbqmIypeKs](https://youtu.be/aDbqmIypeKs), 635 mil (set/2026);
    - SpaceToday, [plt8QXsSTGQ](https://youtu.be/plt8QXsSTGQ), 332 mil (set/2026, 7,5×).

    O tema volta a cada notícia: 2017, 2018, 2021, 2023 e 2026.
- **Brecha pt-BR:** o tema não está vazio, mas a manada é reativa. Os vídeos de 2021 são gente falando sobre a erupção (transcrição em `manada/tsunami/`), e os de 2026 tratam do meteotsunami de SC. Ninguém mostra:
  - a onda se propagando sobre a batimetria real;
  - a plataforma continental, que muda a altura da onda na costa;
  - **o tsunami de 1755, que chegou a Tamandaré e Itamaracá (PE) e a Lucena (PB)**, com documentos no Arquivo Histórico Ultramarino. Fonte: Dourado et al. 2022, *J. South Am. Earth Sci.*; livro de A. Veloso (UnB).
- **Ângulo / roteiro:** são 3 perguntas, no molde do OMTR.
  1. Já aconteceu? Sim, em 1755.
  2. Pode acontecer de novo? Aqui entram La Palma, a dorsal e a falha de Gloria.
  3. O que a ciência diz hoje? Ward & Day (2001) previram 40 m no norte do Brasil, e trabalhos posteriores encolheram muito essa onda.

  O mapa 3D mostra por que o Nordeste fica mais exposto.
- **Material (estimativa: ~60% da tela):**
  - (a) livre:
    - Commons: `2021 Cumbre Vieja volcanic eruption` 152 arquivos, mais La Palma;
    - NASA Earth Observatory (erupção de La Palma);
    - GEBCO/ETOPO;
    - gravuras de Lisboa em 1755 (domínio público);
    - mapas e documentos de época.
  - (b) com crédito: fotos de jornal do meteotsunami de SC.
  - (c) TV.
- **Risco:** o cenário de megatsunami é contestado (citar as duas versões; Periáñez 2021 vê efeito pequeno longe da ilha). O tema é muito feito, então o diferencial tem que estar no título ou na thumb (1755). Não prometer número de horas sem cálculo.

### #3 Por que o Brasil não tem TRENS?
- **Títulos:**
  - T1 "Por que o Brasil não tem TRENS?" (31 caracteres; os 2 avaliadores escolheram este).
  - T2 "A serra que travou os trens do Brasil" (versão honesta de "matou").
- **Thumb:** Serra do Mar em relevo 3D real; um trilho em zigue-zague subindo o paredão; marca vermelha; texto curto **"A SERRA"** ou **"796 M"**. Os dois avaliadores pediram texto mais curto que "1.000 M DE PAREDE".
- **Evergreen (3 números):**
  - [youtu.be/2kb97WAAfxg](https://youtu.be/2kb97WAAfxg), Fatos Desconhecidos: 2,09 mi, 2022, 10,3×, 1,2 mil/dia na média da vida.
  - [youtu.be/AKJlXW988nY](https://youtu.be/AKJlXW988nY), BBC News Brasil: 1,13 mi, 2021, 8,8×.
  - [youtu.be/8NE7un_R5og](https://youtu.be/8NE7un_R5og), Ciência Todo Dia: 1,29 mi, abr/2025, 2,2 mil/dia na média.
  - Mais:
    - Tinocando, 853 mil (2024);
    - Elementar, 436 mil (2020);
    - Ideias Radicais, 233 mil (2018);
    - **Além dos Trilhos, [h21RFJQnZSo](https://youtu.be/h21RFJQnZSo), 103 mil = 90× a mediana, jan/2026, 11,9 mil inscritos.** O tema ainda puxa num canal pequeno.
- **Brecha pt-BR:** de ângulo, não de tema. As 3 transcrições da manada (`manada/trens/`) explicam por JK, indústria automobilística, bitolas e crise da RFFSA. A Serra do Mar aparece só de passagem, numa frase sobre Petrópolis. Ninguém mostra:
  - o paredão de 796 m em Paranapiacaba, que exigiu o sistema funicular inglês de 1867 (Serra Velha);
  - os rios do planalto, que correm para o interior (Tietê, Paraná) e não para o porto;
  - que por isso a malha virou um "pente" de linhas porto–interior que não se conectam.

  O relevo explica o desenho da malha; a política explica o abandono.
- **Material (estimativa: ~65% da tela, o melhor dos 3):**
  - (a) livre:
    - Commons: `Paranapiacaba` 870 arquivos, `Rail transport in Brazil` 487, `Serra do Mar` 102;
    - fotos da São Paulo Railway com mais de 70 anos (domínio público);
    - SRTM;
    - malha ferroviária da ANTT/DNIT (dado aberto).
  - (b) com crédito: acervos da ABPF e de museus ferroviários.
  - (c) TV.
- **Risco:** o relevo é só parte da resposta. O título e o roteiro não podem dizer que a serra é a causa única, senão vêm os comentários "foi o lobby rodoviário". O certo é usar isso: "todo mundo fala de JK; ninguém fala do paredão". O cético alertou para comentários políticos. É o tema mais feito dos 3, então a thumb de relevo precisa se destacar dos rostos e trens das concorrentes (`mosaicos/brasil-ferrovias/mosaico.jpg`).

### Reserva 1: Por que o MAIOR rio do mundo não tem nenhuma ponte?
- **Títulos:** T1 "Por que o MAIOR rio do mundo não tem nenhuma ponte?" / T2 "Nenhuma ponte em 6.400 km: o problema do Amazonas".
- **Thumb:** várzea alagada em 3D, ponte cortada com X vermelho, "ZERO PONTES". O curioso sugeriu a Ponte Rio Negro como "a única exceção?".
- **Evergreen:**
  - [QvFhmbuyeF8](https://youtu.be/QvFhmbuyeF8), Fala Sério: 2,65 mi, 2023, 5,6×, 2,2 mil/dia na média.
  - [4aGwPmVNW9k](https://youtu.be/4aGwPmVNW9k), BE AMAZED: 2,19 mi, 2023.
  - [ljQalgnGOzU](https://youtu.be/ljQalgnGOzU), Mundo Entrópico (Amapá): 433 mil, 2025, 8,9×.
- **Por que é reserva:** em out–nov/2026 saíram **8 clones pt, todos com < 1,3 mil views**. O tema está sendo martelado por canais de IA agora. Lucas Desenhando ainda fez 79,5 mil (3×) em set e Te Mostro no Mapa fez 10 mil (5,6×).
- **Ângulo nosso:** o pulso de cheia de 10–15 m (régua de Manaus da ANA: cheia de 2021, secas de 2023–2024) e as margens que andam. Só o relevo mais a série histórica mostram isso.
- **Material:** Commons `Amazon River` 226, `Ponte Rio Negro` 102, Landsat, ANA. Bom.
- **Momento para fazer:** guardar 2–3 meses até a onda de clones passar.

### Reserva 2: "O Brasil já tremeu 1.815 vezes" (por que o Brasil não tem vulcões nem terremotos?)
- **Títulos:** T2 "O Brasil já tremeu 1.815 vezes (e quase ninguém sabe)", o que os 2 avaliadores preferiram; T1 "Por que o Brasil não tem VULCÕES nem terremotos?".
- **Thumb:** placa sul-americana em 3D, Andes em vermelho, pontos de sismos no Brasil, **"1.815"** grande.
- **Evergreen:**
  - [CgJ9LOiWjg8](https://youtu.be/CgJ9LOiWjg8), Manual do Mundo, furacão: 2,59 mi, 2024, ~1,5 mil/dia hoje.
  - [qd1BoIti5mU](https://youtu.be/qd1BoIti5mU), Elcio Braga: 766 mil, 2020, 227×.
  - [QLCCtvkpPGs](https://youtu.be/QLCCtvkpPGs), Cortes do Inteligência (Sacani): 452 mil, 2023, 18,6×.
  - [4qCKK3I70TI](https://youtu.be/4qCKK3I70TI), Aulalivre: 100 mil, 2017, 638×.
- **Por que é reserva:** os 2 avaliadores deram "talvez". A pessoa "acha que sabe", e o Manual do Mundo fez terremotos em ago/2026 (1,47 mi). A versão evergreen do Caruaru da rodada 1 aproveita o catálogo da USP, que já foi testado.
- **Material:** é o mais fino em foto (Commons `Earthquakes in Brazil` tem 5 arquivos); quase tudo seria mapa.

## 3. Descartados mais tentadores (e o dado que derrubou)
| Pergunta | O que atraía | O que derrubou |
|---|---|---|
| Como era o Brasil quando o mar era 120 m mais baixo? | É evergreen: Atlas Pro 6 mi (2020); Geography Bible 3,5 mi (2024); pt "Era do Gelo no Brasil" 1,16 mi (mai/2026, Um Documentário). E é o tema mais "Em Relevo" de todos (batimetria) | Crivo NÃO/talvez: "o vizinho já ocupa esse lugar", e a faixa ocre vira borrão em 160 px. Fica perto do OMTR "Quanto do Brasil sobraria se o gelo derretesse" (15/11) |
| E se o Atlântico secasse? | RLL "Drained the Mediterranean" 6,9 mi (2017); xkcd 3,2 mi; autocomplete "e se o mar secasse" | O Mapa Não Mente fez **574 mil há 8 dias** ("Secamos o Atlântico"); crivo NÃO/NÃO ("clone direto") |
| O Amazonas já correu ao contrário? | PBS Eons 929 mil; geologia pura | Em pt, **6 de 6 vídeos de 2026 com < 1,2 mil views**: o tema não puxa clique em pt |
| Por que é impossível explorar a Amazônia profunda? / Rio Madeira | Kairus 2,9 mi em 39 dias; KROMO 3,3 mi em 44 dias | É onda, não evergreen: zero vídeos pt com ≥ 1 ano e ≥ 100 mil nesse ângulo, e a manada já está clonando |
| Encontro das Águas (por que não se misturam) | Manual do Mundo 5,9 mi (2019); pequenos com 151–377× | Crivo NÃO/talvez: "vi na escola", pouca lacuna |
| Fossa das Marianas / buraco mais fundo / Ponto Nemo | É evergreen enorme (Você Sabia 18,7 mi e 13,6 mi; RLL 48–50 mi) | Global, sem Brasil, dominado por gigantes; sem brecha |

## 4. Views/dia de hoje (evergreen vivo)
A tabela está em `evergreen.csv` (`views_dia_hoje` = diferença entre `snap1.json` e `snap3.json`, extrapolada para 24 h). Ressalva: o contador público do YouTube **atualiza em lotes**. No snapshot de 48 min, 73 dos 121 vídeos não mudaram. Por isso valem a janela maior (§4.1) e, para vídeos antigos, a média da vida.

### 4.1 Janela de 1,49 h (snap1 22:22 → snap3 23:51 UTC)
- 60 de 121 vídeos mudaram o contador; os 61 restantes ficaram parados. Quase todos os parados têm > 1 ano: o YouTube atualiza o contador público deles em lotes de horas. Para eles, "0" quer dizer "sem leitura", não "morto".
- **Para medir de verdade:** rode `tools/.venv/bin/python scripts/snapshot.py snap24h.json` daqui a ≥ 24 h e troque o `snap3.json` por ele no `scripts/evergreen.py` (custa 3 unidades de cota). O `snap1.json` é a base.

Leituras da janela nos vídeos-evidência do top 3 e das reservas (só os que mudaram):

| Pergunta | Vídeo | Idade | Views | Média da vida/dia | Hoje/dia (1,5 h) |
|---|---|---|---|---|---|
| itaipu-rompesse | [RjHWkCdZdOE](https://youtu.be/RjHWkCdZdOE) Video Simulation after 3 Gorges Dam Collapse | 6.3 anos | 901.314 | 391 | 65 |
| itaipu-rompesse | [DRyU5YjEmnY](https://youtu.be/DRyU5YjEmnY) 25 Enormes Rompimentos de Barragens Flagrados | 2.1 anos | 5.360.338 | 6.961 | 3.520 |
| itaipu-rompesse | [lYbFLBqJXVc](https://youtu.be/lYbFLBqJXVc) 10 Massive Dam Failures Caught On Camera | 4.1 anos | 23.354.868 | 15.477 | 2.648 |
| tsunami-brasil | [6utAunBKXV4](https://youtu.be/6utAunBKXV4) Megatsunami Scenario - La Palma Landslide | 9.4 anos | 4.249.876 | 1.237 | 48 |
| tsunami-brasil | [wefef21T-00](https://youtu.be/wefef21T-00) Especialistas revelam se Brasil corre risco d | 8.4 anos | 1.687.858 | 549 | 16 |
| tsunami-brasil | [plt8QXsSTGQ](https://youtu.be/plt8QXsSTGQ) TSUNAMI NO BRASIL? O QUE ACONTECEU EM SANTA C | 0.2 anos | 331.539 | 5.920 | 323 |
| br-sem-desastres | [CgJ9LOiWjg8](https://youtu.be/CgJ9LOiWjg8) Por que não tem FURACÃO no BRASIL? | 2.1 anos | 2.591.286 | 3.383 | 1.501 |
| br-sem-desastres | [QLCCtvkpPGs](https://youtu.be/QLCCtvkpPGs) POR QUE no BRASIL NÃO EXISTEM VULCÕES ATIVOS  | 3.1 anos | 451.733 | 397 | 48 |
| br-sem-desastres | [QuTzkzW8_Uw](https://youtu.be/QuTzkzW8_Uw) Super terremoto pode atingir o Brasil... | 0.2 anos | 480.471 | 5.789 | 48 |
| br-sem-desastres | [U26yGFF6lqI](https://youtu.be/U26yGFF6lqI) Existem terremotos no Brasil? #CiênciaUSP | 8.1 anos | 26.990 | 9 | 16 |
| amazonas-sem-ponte | [ljQalgnGOzU](https://youtu.be/ljQalgnGOzU) Por que NÃO existe uma ponte entre o AMAPÁ e  | 1.3 anos | 433.291 | 893 | 16 |
| brasil-ferrovias | [2kb97WAAfxg](https://youtu.be/2kb97WAAfxg) Por que o Brasil parou de investir em ferrovi | 4.6 anos | 2.091.941 | 1.233 | 129 |
| brasil-ferrovias | [ZR5X1ImYJKk](https://youtu.be/ZR5X1ImYJKk) por que o BRASIL NÃO tem FERROVIAS? | 2.2 anos | 852.603 | 1.057 | -65 |

Leitura: o gênero "barragem rompendo" segue vivo depois de anos: o vídeo de 4 anos ainda faz milhares de views/dia. Para tsunami, trens e pontes, a janela não pegou atualização dos vídeos antigos. A prova evergreen deles vem de outro lado: o mesmo tema fez sucesso em vários anos e em vários canais (§2: 2017→2026 no tsunami, 2018→2026 nos trens).

## 5. Arquivos
- `RELATORIO.md` (este arquivo) e `banco.csv` (22 perguntas: tipo, Brasil sim/não, status, brecha pt, colisão com o OMTR, crivo, motivo e as métricas evergreen agregadas).
- `perguntas.tsv` (30 perguntas e as consultas pt/int); `q/<pergunta>/{pt,int}/refs.csv` + `medianas.json`. O `busca/` fica fora do git.
- `evidencias.tsv`, `snap1.json`, `snap2-48min.json`, `snap3.json`, `evergreen.csv`, `evergreen_agg.json`, `medianas_extra.json`.
- `autocomplete/sugestoes.json` (88 prefixos).
- `crivo/CANDIDATAS.md`, `crivo/PARECER-curioso.md`, `crivo/PARECER-cetico.md`.
- `manada/{trens,tsunami,itaipu}/manada-*.txt` (transcrições).
- `mosaicos/<pergunta>/mosaico.jpg` (+ `-320`) do top 3 e das 2 reservas.
- `scripts/` (autocomplete, listar, filtra, snapshot, medianas_extra, evergreen).

## Fontes dos fatos citados
- Tsunami de 1755 no Brasil: Dourado et al., "Possible evidence of the 1755 CE transatlantic tsunami in Brazil", *J. South Am. Earth Sci.* 2022 ([aminer](https://aminer.org/pub/62d16faa5aee126c0fd85c68/possible-evidence-of-the-ce-transatlantic-tsunami-in-brazil)); [O Povo, 17/09/2021](https://www.opovo.com.br/noticias/brasil/2021/09/17/pesquisa-mostra-que-brasil-ja-foi-atingido-por-tsunami-ha-200-anos.html); ressalva em [Folha PE](https://www.folhape.com.br/noticias/tsunami-em-pernambuco/203270/).
- La Palma, Ward & Day 2001 e as críticas: [Wikipedia, Cumbre Vieja tsunami hazard](https://en.wikipedia.org/wiki/Cumbre_Vieja_tsunami_hazard); [Scientific American](https://www.scientificamerican.com/article/scientists-predict-a-mega/); Periáñez 2021 ([MDPI Geosciences 11/12/497](https://mdpi.com/2076-3263/11/12/497)); [TCC UFPR (Reese)](https://geologia.ufpr.br/wp-content/uploads/2018/11/Mauro-Reese-TCC.pdf).
- Serra do Mar, 796 m em Paranapiacaba, e o funicular de 1867: [UNESCO, lista indicativa 5878](https://whc.unesco.org/fr/listesindicatives/5878/); [Grace's Guide, São Paulo Railway](https://gracesguide.co.uk/Sao_Paulo_Railway).
- Estudos de ruptura de barragem (modelo de PAE) no rio Paraná: [Porto Primavera, Auren](https://www.aurenenergia.com.br/wp-content/uploads/2025/09/4638-PP-12-GL-810-RT-0001-R1.pdf). Não achei estudo público de Itaipu.
