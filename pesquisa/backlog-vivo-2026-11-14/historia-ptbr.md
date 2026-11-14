# Backlog vivo: historia-ptbr, carga inicial (14/11/2026)

Dados completos (evidências com link, riscos, ângulo) em `historia-ptbr.json`. Custo: US$ 0 (só yt-dlp via WARP e banco; 0 unidades da Data API).

| # | Tema | Título candidato | D | E | U | Nota | Janela | Evidência principal |
|---|---|---|---|---|---|---|---|---|
| 1 | Estados Unidos | Como 13 colônias viraram a maior potência do mundo? | 8 | 9 | 6 | **7,6** | 30/11 | Genius 545,7 mil em 36 d; em pt só o Legados da História tem vídeo curto (96,9 mil, 42× os inscritos) |
| 2 | Portugal | Como um país minúsculo dividiu o mundo ao meio? | 7 | 9 | 6 | **7,2** | 01/12 (Restauração) | "O Dia em que Portugal se Mudou para o Brasil" 773,6 mil, canal com 109 inscritos (03/2026) |
| 3 | URSS | URSS: o país que sumiu do mapa sem perder uma guerra | 8 | 6 | 6 | **6,6** | 30/11 | Archive in Minutes 133,6 mil (17/10); Prof. HOC pt 303,9 mil; clone pt Rússia 255 mil |
| 4 | Inglaterra / Reino Unido | Como uma ilha chuvosa passou a mandar em 1/4 do mundo? | 7 | 9 | 4 | **6,3** | evergreen | Genius Império Britânico 235,5 mil; busca pt 2026 med. 188 mil |
| 5 | Argentina | A Argentina já foi mais rica que a França. O que houve? | 7 | 8 | 4 | **6,1** | evergreen | Vogalizando pt 586 mil (08/2026); ângulo rico→pobre provado em pt (Plano Piloto 854 mil) |
| 6 | Espanha | Como a Espanha dominou o mundo e perdeu tudo? | 6 | 9 | 4 | **6,0** | evergreen | Academia Play (es) 662,5 mil (06/2026); sem vídeo novo pt no molde |
| 7 | Cuba | Espanha, EUA, URSS: por que Cuba nunca ficou sozinha? | 6 | 8 | 4 | **5,8** | evergreen | BBC Brasil 298,6 mil (05/2026); busca pt 2026 med. 242 mil |
| 8 | Vikings | Como os vikings chegaram da Rússia à América? | 7 | 6 | 3 | **5,0** | evergreen | Reconstrução Histórica pt 420,7 mil (04/2026, 6× os inscritos) |

**Método.** 5 fontes: (1) os últimos 40 vídeos de History in Minutes, Genius History, CountryCorns, clone pt "História em minutos" (08/2026), History Easy Guide, História Inteira e A HISTORIA EM MINUTOS, por yt-dlp via WARP em 14/11, com data e views dos vídeos citados conferidas um a um; (2) concorrentes pt/es de fora do molde achados na busca; (3) demanda: `ytsearch20` de "história de X" via WARP, com e sem o filtro "este ano", mediana das top-10 com ≥ 4 min (a `youtube.palavras_chave` de 11/11 só tem mediana para Brasil, Japão e Egito, que já foram feitos; para os outros temas há só autocomplete: Jerusalém, Império Britânico, Ucrânia), mais as medianas de 12 meses de `pesquisa/proximos-temas-2026-11`; (4) `youtube.garimpo_videos` (Archive URSS 133 mil, Israel 316 mil/1,14 mi) e benchmark/gap de 14/11; (5) nossos números (`metricas_video`: Egito 380, Índia 251, China 146, Brasil 53, Irã 23, Rússia 17, Roma 2). Peso maior: tema que um vídeo pt (ou o Genius) está rodando agora e potência moderna/europeia com gancho no presente, que é o que funciona em pt (gap §1). Antigas e Ásia flopam em pt. Notas: demanda = busca + views da referência; encaixe = rende eras ligadas até hoje sem repetir vídeo nosso; urgência = referência quente, data ou sessão com vídeo recém-publicado; nota = (D×E×U)^(1/3). Os títulos usam padrões de tensão porque a fórmula "A história INTEIRA de X" colide (EUA: Legados e BTN; Portugal: Impérios AD e HQ). A embalagem e o crivo decidem. Os hooks estão marcados [I, conferir].

**Limitações.** A busca via WARP é uma amostra, com vídeos em espanhol misturados nos resultados pt (Argentina, México, Espanha) e títulos traduzidos automaticamente pelo yt-dlp. Para Espanha e Vikings, a mediana de 12 meses com filtro de história (13/11) saiu bem mais baixa (24 mil e 10 mil) que a de 2026 sem filtro: a demanda pt é incerta. Views de 14/11, lidas uma vez.

**O que ficou de fora e por quê.**
- **Israel / Jerusalém:** é a maior demanda medida (busca pt 2026 med. 251 mil; CountryCorns 1,14 mi; Prima Historian 316 mil). Ficou de fora porque o backlog manda evitar: a demanda vem do conflito atual e da Bíblia, com risco alto de anúncio e polarização.
- **Ucrânia:** clone pt 25 mil, HiM 180 mil, Te lo Pinto 230 mil. Guerra em curso, mesma regra "evitar" do backlog.
- **Venezuela:** urgência real (g1 "captura de Maduro" 1,46 mi; busca 2026 med. 468 mil, quase tudo vlog e notícia). Política atual polarizante, e o vídeo do clone sobre Maduro fez só 892 views. Reavaliar se o Rodrigo quiser.
- **México:** a busca é alta (723 mil), mas quase tudo em espanhol. Em pt só há o HQ (10,7 mil) e o Globalizando (297 mil, antigo). Nota ~5,0.
- **Grécia:** 5,0, empatada com Vikings. Demanda pt de escola e mitologia (Tinocando 1,87 mi), e o "até hoje" fica fraco. Os Vikings ficaram na frente porque fazem sessão com Rússia e França.
- **Império Otomano / Turquia:** pt 2026 med. 26 mil (Explore o Mundo 97 mil); "Turquia" é dominada por viagem e Arca de Noé. Nota 4,9.
- **Itália:** Genius 31,7 mil (o piso dele) e sobreposição com Roma. **Coreia:** HiM 1,4 mil e CountryCorns 499 (flop). **Austrália:** clone pt 2,4 mil.
- **Iugoslávia:** Bello Mundo 168,8 mil e War Stories 726 mil (en), mas o fim da história é uma guerra com crimes em massa: risco de anúncio, 4,7.
- **Reinos africanos** (Mali, Congo; janela de 20/11, Consciência Negra): pt 2026 med. 0,5–1,5 mil. Só "Mansa Musa" tem demanda, e ela é em inglês.
- **1ª/2ª Guerra Mundial** (HEG 238 mil e 108 mil): fora do nicho da bíblia (países/impérios), só com OK do Rodrigo.
