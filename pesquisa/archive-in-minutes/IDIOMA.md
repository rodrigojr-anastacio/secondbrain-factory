# IDIOMA: em que língua abrir o canal "Dossiê" (história INTEIRA de organizações em N minutos)

Data: 2026-11-04 · Brief: `~/workspace/referencias/BRIEF-dossie-idioma.md` · Agentes: orquestrador (Claude Code, Opus) + Tendências (subagente, Opus).
Dados: `idioma/NOTAS.md` (demanda e concorrência em 12 idiomas), `idioma/dados/resumo_idiomas.json`, `idioma/scripts/`, `idioma/voz/` (vozes Fish por idioma). Base anterior: `LEVANTAMENTO.md` (anatomia do formato; a recomendação de idioma dele, pt-BR, **fica substituída por este relatório**).
Legenda: **[O]** observado (busca do YouTube via WARP, YouTube Data API, Fish API, amostras geradas) · **[I]** inferido ou estimativa (sempre em faixa).

---

## Resumo executivo

**Recomendação: espanhol (es), com o francês (fr) em 2º.** O canal vira `dossie-es`, com o nome sugerido **Dossier en Minutos** (`@dossierenminutos`, livre). O piloto é **"TODA la historia de la CIA en 11 minutos"**, com roteiro nativo em espanhol pronto. Voz sugerida: Fish "Dio Historias" (`ac594943984a47e7a827416eb263c7b1`, acento neutro). O canal já criado pelo Rodrigo (`UCVCYqeuCwTWC7Lqez_qeWRA`) só precisa trocar nome, handle e idioma no Studio.

| Idioma | Demanda (30%) | Concorrência (25%) | RPM (20%) | Viabilidade (15%) | Risco (10%) | **Nota** | Situação |
|---|---|---|---|---|---|---|---|
| **es** | 7,5 | 6 | 4 | 8 | 6 | **6,35** | **1º, recomendado** |
| **fr** | 5 | 9 | 6 | 5 | 6 | **6,30** | **2º** (empate técnico; vence se o RPM pesar mais) |
| pt | 3,5 | 8 | 2,5 | 10 | 6 | 5,65 | 3º |
| de | 2 | 8 | 8 | 3 | 5 | 5,15 | demanda fraca fora da Stasi |
| it | 1,5 | 8 | 6 | 4 | 6 | 4,85 | só a máfia tem demanda |
| en | 10 | **1** | 10 | 9 | 5 | 7,10 | **eliminado** (saturação: 101 canais no molde) |
| ru | 9 | 9 | **0** | 3 | 2 | 5,60 | **eliminado** (sem receita de anúncio na Rússia) |
| hi | 6 | 9 | **1** | 3 | 5 | 5,20 | **eliminado** (RPM) |

**Por que es, em 5 linhas:**
1. **Prova direta do formato em es [O]:** o Atlas del Tiempo, com 735 inscritos, trocou países (96–3,4 mil views) por organizações em 28/10 e fez Mossad 33,1 mil e KGB 30,6 mil em uma semana. Nenhum outro idioma tem isso.
2. **Demanda de 2026 é o dobro da do fr e o triplo da do pt [O]:** são 102 vídeos acima de 100 mil views nos 12 temas em es, contra 51 em fr e 32 em pt.
3. **Vaga parcial [O]:** há 13 canais no molde em es, mas 12 têm mediana de 17 views. O único com tração (Atlas) é pequeno, e o Atlas mostrou que ainda dá para entrar tarde com qualidade.
4. **O RPM é baixo, mas melhor que o do pt [I]:** US$ 1–3,2, com Espanha (22%) e EUA (9%) puxando a média.
5. **O Rodrigo lê espanhol:** a revisão do roteiro e do pacote é viável. Em francês, não seria.

**Por que o inglês perde, mesmo com a maior nota bruta:** a demanda em inglês é enorme, mas já tem dono. Desde 09/2026 surgiram 91 clones do molde, e só 2 canais passam de 5 mil views de mediana: o Archive in Minutes (146 mil) e o Ziro (16,6 mil), justamente **os primeiros a chegar** [O]. Dos ~89 que entraram depois do Archive, nenhum passou de 5 mil. Entrar agora seria ser o 92º clone. Por isso a matriz tem uma **trava**: concorrência ≤ 2 elimina o idioma, como já dizia a regra "não ser o 16º clone" do `playbooks/novo-canal.md`. Sem a trava, o inglês ganharia na soma (7,10) só por demanda e RPM, que ele não consegue capturar.

**Custo deste job:** **US$ 0,43** (Fish US$ 0,04 em 7 amostras de voz; fal.ai US$ 0,38 em 12 imagens de teste), tudo em `financas.consumo` com `ref_id` = 7 (piloto CIA). Teto do brief: US$ 0,50 em voz e US$ 2 em imagens. Cota da API: ~1.250 unidades e nenhum `search.list`.

**Decisões do Rodrigo**
1. Aprovar o espanhol.
2. Renomear o canal no Studio: nome, handle `@dossierenminutos` e idioma espanhol (`canais/dossie-es/identidade.md`).
3. Ouvir e escolher a voz entre 3 finalistas (`canais/dossie-es/testes/voz/LEIA.md`).
4. Dar o OK para o piloto da CIA (teto de US$ 9).

---

## 1. Método
- **Demanda e concorrência [O]:** 360 buscas sem cota (yt-dlp via WARP), em 12 idiomas e por relevância e "este ano por views", com os temas escritos nativamente. Depois, `videos.list` e `channels.list` de 4.485 vídeos e 430 canais. Detalhes em `idioma/NOTAS.md` §Método. A amostra serve para **comparar idiomas**, não mede o mercado inteiro.
- **C4** = KGB, CIA, Mossad e Gestapo, os 4 temas buscados em todos os idiomas. **Molde exato** = canal com "história INTEIRA/COMPLETA de <organização> em N minutos" em ≥ 40% dos vídeos. **Clone** = molde exato que começou a partir de 09/2026.
- **RPM [I]:** tabela de referência da fábrica (`playbooks/garimpo-tendencias.md`: história US$ 4–8 em en; fatores pt 0,25–0,35×, es 0,25–0,4×, fr 0,5–0,7×), cruzada com o país dos canais de demanda [O] e com fontes públicas de CPM/RPM por país e idioma. As fontes divergem muito (são blogs de fornecedores e de distribuição musical), mas concordam na ordem de grandeza: en > de > fr > es (Espanha > México) > pt. Exemplos: Dynamoi (Espanha US$ 4,00 contra México US$ 3,17 contra EUA US$ 7,83 em Art Tracks), AIR Media-Tech (de US$ 4,89, fr US$ 3,38, pt ~US$ 0,91, es de US$ 0,91 a US$ 2,50) e Youviral (América Latina muito abaixo de EUA/CA/GB/AU). Links na seção 7.
- **Viabilidade [O]:** vozes públicas do Fish listadas por idioma (`idioma/voz/fish_*.json`: 53 resultados em es, 52 em fr); 7 amostras do hook em es geradas e conferidas com Whisper (`canais/dossie-es/testes/voz/`); 12 imagens de teste do piloto es (`canais/dossie-es/testes/ESTILO-es.md`).

## 2. Por idioma

### en (inglês): eliminado por saturação
- **Demanda [O]:** a maior. Mediana do top-10 (C4) de 1,78 mi; 298 vídeos de 2026 acima de 100 mil nos 12 temas; público US 49% e GB 20%.
- **Concorrência [O]:** 101 canais no molde, 91 clones desde 09/2026, com mediana de **25 views**. Só o Archive (146 mil) e o Ziro (16,6 mil) passam de 5 mil, e os dois chegaram primeiro.
- **RPM [I]:** US$ 4–8. Nazismo e violência podem levar a anúncio limitado.
- **Alcance:** global.
- **Viabilidade [I]:** a melhor de todas (vozes en de primeira linha, QA fácil).
- **Leitura:** fica fora. Reavaliar daqui a 2–3 meses, quando os clones morrerem [I].

### es (espanhol): 1º
- **Demanda [O]:** mediana do top-10 (C4) de 401 mil; 41 vídeos C4 de 2026 acima de 100 mil (102 nos 12 temas).
  - Temas fortes: **cartel (2,99 mi), máfia (1,63 mi), FBI (1,21 mi), CIA (1,10 mi), SS (814 mil), Templários (583 mil), Mossad (430 mil), KGB (372 mil)**.
  - Fracos: Stasi (18 mil) e MI6 (16 mil).
- **Concorrência [O]:** 13 canais no molde, todos de 06/10 a 03/11; 12 com mediana de 17 views.
  - Atlas del Tiempo: 735 inscritos e mediana de 11,2 mil nos vídeos de organização.
  - Fora do molde: Te lo Pinto (ES, 595 mil inscritos) fez a KGB (139 mil) e pode voltar ao tema.
  - **4 clones novos só em 03/11** [O]: a janela é de dias a semanas [I].
- **RPM [I]:** US$ 1–3,2 (0,25–0,4× o do en). Espanha (22% da demanda) e EUA hispânico (9%) pagam mais que a América Latina.
- **Alcance [O/I]:** México 22%, Espanha 22%, EUA 9%, Argentina 6% e o resto da América Latina. É o 2º maior público do YouTube entre os idiomas avaliados [I].
- **Risco [I]:** cartéis e nazismo têm risco alto de anúncio limitado, por isso entram depois do 5º vídeo. CIA e América Latina geram comentários polarizados, que pedem fonte oficial dos EUA em cada acusação.
- **Viabilidade [O]:**
  - **voz:** 7 vozes Fish nativas testadas, Whisper 0,93–0,95, sem tag falada, 124–186 palavras/min. Kokoro tem es como reserva grátis;
  - **imagens:** sem idioma (o texto vai no código);
  - **revisão:** o Rodrigo lê espanhol (português é língua próxima). Os falsos amigos ficam com a 2ª leitura de LLM e o Whisper (`canais/dossie-es/estilo.md`).
- **Leitura:** é o melhor equilíbrio. A vaga é parcial e está fechando.

### fr (francês): 2º
- **Demanda [O]:** mediana do top-10 (C4) de 623 mil, a maior depois do en. Mas a demanda está concentrada em TV e canais grandes (Investigation, LCI, HugoDécrypte), e só 16 vídeos C4 de 2026 passaram de 100 mil (51 nos 12 temas).
  - Fortes: Legião Estrangeira (1,87 mi), máfia (1,70 mi), cartel (1,14 mi), Templários (793 mil), Mossad (759 mil).
  - Fracos: Stasi, MI6 e Gestapo.
- **Concorrência [O]:** 1 clone (Récits d'Archives: 620 inscritos, melhor vídeo com 360 views). Há vaga total, mas também **não há prova** de que o molde em quadrinho funcione em fr.
- **RPM [I]:** US$ 2–5,6. É o melhor fora do en entre os idiomas viáveis; o público é 93% FR.
- **Alcance [I]:** França, Bélgica, Suíça, Quebec e África francófona (esta com RPM baixo). Mercado menor que o es.
- **Risco [I]:** parecido com o do es. A lei francesa sobre símbolos nazistas exige o mesmo cuidado que já temos.
- **Viabilidade [O/I]:** há vozes Fish fr (52 na lista; não testadas) e o `lotr-fr` já opera em fr (com Kokoro). Mas o Rodrigo **não revisa** francês: o QA ficaria só no Whisper e no LLM.
- **Leitura:** é a 2ª opção e a **melhor 2ª língua do mesmo canal**. As imagens e a pesquisa servem para as duas línguas (ver §5).

### pt (português): 3º
- **Demanda [O]:** mediana do top-10 (C4) de 229 mil (57% da do es), com 32 vídeos de 2026 acima de 100 mil.
  - Fortes: Mossad (405 mil), CIA (335 mil), SS (271 mil).
  - Praticamente sem demanda: Stasi (1,2 mil), MI6 (2,2 mil) e máfia (6 vídeos).
- **Concorrência [O]:** 3 clones com 0–15 inscritos; o melhor vídeo teve 54 views. Um deles se chama "Dossiê Completo".
- **RPM [I]:** US$ 1–2,8; o público é 87% BR.
- **Viabilidade:** máxima (a fábrica e o Rodrigo trabalham em pt).
- **Leitura:** a vaga é real, mas a demanda e o RPM são os menores dos três primeiros. Pela regra do Rodrigo, o pt só ganha se compensar, e não compensa. O roteiro KGB em pt fica guardado em `canais/dossie-es/arquivo-ptbr/`.

### de (alemão), it (italiano), pl (polonês)
- **de [O]:** mediana do top-10 (C4) de 44,7 mil. A Stasi é a exceção (409 mil; Simplicissimus com 1,91 mi). Há 6 clones, com o melhor vídeo em 553 views.
  - RPM alto [I], mas a revisão é inviável e há risco legal com símbolos nazistas (§86a StGB) [I].
- **it [O]:** mediana do top-10 (C4) de 33,1 mil; só a máfia tem demanda (1,01 mi). Há 2 clones, um deles "Dossier in Minuti".
- **pl [O]:** mediana do top-10 (C4) de 171 mil, com Gestapo e KGB fortes. Há 3 clones de 03–04/11, um deles copiando o subtítulo do Archive. RPM baixo-médio [I].

### Exploratórios: ru, hi, ar, tr, ja
- **ru [O]:** a maior demanda fora do en (mediana do top-10 de 1,48 mi; 68 vídeos C4 de 2026 acima de 100 mil) e 1 clone com 0 views.
  - Fica **eliminado** porque o YouTube suspendeu os anúncios para usuários na Rússia em 03/2022 [I, política conhecida; não reconsultada hoje]. Há também risco legal para o conteúdo sobre serviços secretos russos.
- **hi [O]:** mediana do top-10 de 626 mil, puxada por CIA e Mossad na pauta atual. O espaço é de mídia grande, e o RPM é o mais baixo [I]. Eliminado.
- **ar [O]:** Mossad forte (1,98 mi), mas o tema é politizado e o RPM baixo-médio [I].
- **tr e ja [O]:** sem demanda relevante.

## 3. Matriz de decisão
**Pesos padrão** (agora também em `playbooks/novo-canal.md`):
- Demanda 30%: views e quantidade de vídeos de 2026 do tema no idioma, mais a prova do formato no idioma.
- Concorrência 25%: canais no molde, clones e as medianas deles. 10 = vazio; 0 = dono forte + dezenas de clones.
- RPM 20%: faixa estimada do nicho × fator do idioma e do país.
- Viabilidade 15%: voz nativa no Fish testada, revisão (o Rodrigo lê o idioma?), QA.
- Risco 10%: anúncio limitado, risco legal e político no idioma.

**Travas** (eliminam o idioma, seja qual for a soma): concorrência ≤ 2 (molde saturado, com dono e clones mortos) **ou** RPM ≤ 1 (mercado sem receita).

**Desempate** (diferença < 0,3): a ordem de preferência do Rodrigo, **en → es → pt → fr → de**, e depois a prova do formato no idioma.

| Idioma | Demanda | Concorrência | RPM | Viabilidade | Risco | Nota | Trava |
|---|---|---|---|---|---|---|---|
| en | 10 | 1 | 10 | 9 | 5 | 7,10 | **concorrência** |
| es | 7,5 | 6 | 4 | 8 | 6 | **6,35** | — |
| fr | 5 | 9 | 6 | 5 | 6 | 6,30 | — |
| pt | 3,5 | 8 | 2,5 | 10 | 6 | 5,65 | — |
| ru | 9 | 9 | 0 | 3 | 2 | 5,60 | **RPM** |
| hi | 6 | 9 | 1 | 3 | 5 | 5,20 | **RPM** |
| de | 2 | 8 | 8 | 3 | 5 | 5,15 | — |
| ar | 5 | 10 | 2 | 2 | 2 | 4,90 | — |
| it | 1,5 | 8 | 6 | 4 | 6 | 4,85 | — |
| pl | 4 | 7 | 3 | 3 | 6 | 4,60 | — |

**Como dei cada nota [I]:**
- **Demanda:** 10 = en.
  - es leva 7,5: 102 vídeos de 2026 acima de 100 mil e a prova do Atlas.
  - fr leva 5: a mediana é alta, mas vem da TV, e não há prova do formato.
  - pt leva 3,5.
- **Concorrência:**
  - es leva 6: 13 no molde, mas só 1 vivo e pequeno; Te lo Pinto à espreita.
  - fr leva 9 e pt leva 8: clones mortos, e em pt um usa nome parecido com o nosso.
  - en leva 1.
- **RPM:** proporcional à faixa estimada (en 4–8 = 10; de ~3–8 = 8; fr 2–5,6 = 6; es 1–3,2 = 4; pt 1–2,8 = 2,5).
- **Viabilidade:** pt 10, en 9, es 8 (revisão possível), fr 5 (sem revisão humana), de/pl/hi 3.
- **Risco:** 6 é o padrão; de leva 5 (§86a); ru e ar levam 2 (legal e político).

**Sensibilidade [I]:**
- **Pesos iguais** (20% cada): es 6,30, fr 6,20, pt 6,00. O es continua 1º.
- **RPM 30% e demanda 20%:** fr 6,40, es 6,00. **O fr passa à frente.**
- **Viabilidade de fr = 7** (revisor nativo contratado): fr 6,60, também à frente.
- **Leitura:** es e fr estão em **empate técnico**. O es vence pela prova direta do formato, pelo mercado maior, pela revisão que o Rodrigo consegue fazer e pela ordem de preferência dele (es antes de fr).

## 4. Projeção (estimativa, em faixa) [I]
- **es:** se pegar como o Atlas (mediana de ~11 mil nos vídeos de organização com 735 inscritos), os 3 pilotos rendem 5–30 mil views cada. Com 10–20% das views do Archive (280–560 mil/mês) × US$ 1–3,2, são **US$ 280–1.800/mês** depois do YPP. Para 4.000 h com vídeos de 11–13 min e 40% de retenção, são precisas ~46–55 mil views.
- **fr (comparação):** a demanda de 2026 é ~0,5× a do es, então 140–280 mil views/mês × US$ 2–5,6 = **US$ 280–1.570/mês**. O teto de receita é parecido com o do es, com menos clones e sem prova do formato.
- **pt (comparação):** ~0,3× a demanda do es × US$ 1–2,8 = **US$ 90–470/mês**.
- **Critério do teste es** (o mesmo do LEVANTAMENTO, ajustado): depois de 3 vídeos e 14 dias do 1º, média ≥ 3 mil views/vídeo **ou** 1 vídeo ≥ 15 mil, com % assistido ≥ 35% → INVESTIR. Média abaixo de 500 → trocar de tema antes de trocar de idioma (Mossad e FBI) e só depois testar fr.

## 5. Recomendação e plano
1. **es agora**, no canal já criado: renomear para "Dossier en Minutos" (`@dossierenminutos`), com idioma espanhol. Blueprint completo em `canais/dossie-es/`: `canal.yaml`, `estilo.md`, `backlog.md` (20 temas para o mercado es), `identidade.md` e o piloto `videos/001-cia/` (BRIEF, SCRIPT nativo, SOURCES, THUMBS).
2. **Piloto: CIA**, e não KGB. A CIA tem a maior demanda em es entre as agências (mediana do top-10 de 1,10 mi contra 372 mil da KGB) e um ângulo América Latina que ninguém no molde usa (Guatemala 1954 no hook e no fecho). A KGB em es já tem Te lo Pinto, Atlas e a maioria dos clones. Os seguintes são **Mossad** (o melhor do Atlas) e **FBI** (1,21 mi, sem ninguém no molde).
3. **fr como 2ª língua, não como 2º canal do zero [I]:** as imagens (sem texto), a pesquisa, as fontes e a estrutura do roteiro servem para qualquer idioma. Uma versão fr de um vídeo es custa ~US$ 0,20 de voz + reescrita nativa + render. Se o es pegar, abrir o `dossie-fr` (ou faixas de áudio multilíngues no mesmo vídeo, que o YouTube permite) com os temas fortes em fr (Legião Estrangeira, máfia, Mossad, Templários).
4. **pt fica arquivado** (`canais/dossie-es/arquivo-ptbr/`), com o roteiro KGB pronto, caso o Rodrigo queira a versão BR depois.

## 6. Limitações
- A amostra vem das buscas (até 30–40 resultados por consulta), não do universo. As views foram coletadas em 04/11 e mudam rápido.
- RPM sem dado nosso (o `lotr-fr` tem 54 views e o `historia-ptbr` 6–17, sem monetização). As fontes públicas de RPM por país e idioma são blogs de fornecedores, com números divergentes.
- O país dos canais não é o país de quem assiste.
- As vozes fr não foram ouvidas nem testadas (não era o idioma escolhido). O timbre das vozes es precisa do ouvido do Rodrigo; o Whisper só mede inteligibilidade.
- A queda de anúncios na Rússia e o §86a na Alemanha vêm de conhecimento de política, não reconsultado hoje.

## 7. Fontes externas de RPM/CPM (consultadas em 2026-11-04)
- [Dynamoi: YouTube RPM by Country 2025](https://dynamoi.com/learn/statistics/youtube-rpm-by-country-2025) · [Spain YouTube RPM](https://dynamoi.com/learn/youtube-music-promotion/youtube-rpm-spain) · [Mexico YouTube RPM](https://dynamoi.com/learn/youtube-music-promotion/youtube-rpm-mexico)
- [AIR Media-Tech: most popular languages on YouTube / CPM by language](https://air.io/en/audience-growth/what-are-the-most-popular-languages-on-youtube) · [AIR: boost revenue with translation](https://air.io/en/how-video-translation-can-boost-revenue-from-youtube-ads)
- [BeMultilingual: languages with the highest CPM](https://bemultilingual.ca/blog/most-popular-languages-on-youtube-languages-with-the-highest-cpm-and-what) · [Milx: how much YouTube pays in different languages](https://milx.app/trends/how-much-does-youtube-pay-in-different-languages)
- [Youviral: cuánto paga YouTube por 1000 vistas](https://youviral.app/blog/cuanto-paga-youtube-por-1000-vistas) · [Fluxnote: YouTube CPM Latin America by country](https://fluxnote.io/guides/youtube-cpm-latin-america-by-country) · [Awisee: YouTube CPM rates by country and category](https://awisee.com/blog/youtube-cpm-rates)

## Sugestões para `conhecimento/` (não editei; outro job está nesses arquivos)
- **anti-padroes.md:** "os clones chegam a todos os idiomas em ~3 semanas". Em 04/11, o molde do Archive já tinha clones em es (13), de (6), pl (3), pt (3), it (2), hi (2), fr (1) e ru (1). Fonte: `idioma/NOTAS.md`. A vantagem de idioma dura dias, não meses.
- **titulos.md:** a ordem de temas não se transfere entre idiomas. Stasi e MI6 têm 114 mil e 109 mil no Archive (en), mas mediana do top-10 de 18 mil/16 mil em es e 1,2 mil/2,2 mil em pt. Fonte: `idioma/NOTAS.md`, 2026-11-04.
- **roteiros.md:** no mesmo canal em es (Atlas del Tiempo), organizações renderam 10–40× mais que países (KGB 30,6 mil e Mossad 33,1 mil contra 96–3,4 mil). Fonte: `idioma/NOTAS.md` §3.
- **imagens (anti-padroes.md):** nenhum modelo de imagem acerta a posição dos pinos no mapa (nano-banana e flux/dev, 04/11). Os pinos vão no código. Fonte: `canais/dossie-es/testes/ESTILO-es.md`.
