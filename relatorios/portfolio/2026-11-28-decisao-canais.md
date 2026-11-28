# Decisão de portfólio: historia-ptbr, Clearance Required e Em Relevo (28/11/2026)

Brief: `~/workspace/referencias/BRIEF-portfolio-canais-decisao.md`. Só análise e recomendação: nada mudou em canal, backlog, bíblia, banco, fila ou timers. Custo pago: US$ 0.
Método: um subagente por canal (Opus, em paralelo), cada um com diagnóstico de dados + mercado via WARP. Os relatórios completos estão em `2026-11-28-dados/` (`historia-ptbr.md`, `lugares-guerra-en.md`, `em-relevo.md`; brutos do historia em `brutos-historia/`). Este arquivo é a síntese e a decisão, com conferência própria no banco.
Fontes: `youtube.alcance_diario` (impressões e CTR pela Reporting API, até 26/11), `analytics_*` (Analytics API, até 25/11), `metricas_video` (28/11), `studio_video` (último export por canal: historia 20/11, em-relevo 14/11, clearance só 1 dia do Midway; **falta CTR do Studio dos vídeos recentes**), `financas.consumo`, `canais/dossie-es/analises/2026-11-27-diagnostico.md`, `pesquisa/archive-in-minutes/IDIOMA.md`.

---

## 0. Resposta curta

| canal | recomendação | por quê | critério / prazo |
|---|---|---|---|
| **historia-ptbr** | **(c) adaptar**: parar a série de países hoje; teste "como era viver / você não sobreviveria", bonequinhos, Brasil no centro, **1 vídeo/semana** | Países = loteria de 1 hit por canal em pt (até o modelo en caiu); v2 morreu no teste de CTR das 48 h; o nicho "vida no passado" cresce em pt em 2026 e reaproveita o estilo | 4 vídeos até **10/01/2027**: passa se 1 fizer ≥ 3 mil views em 7 d com CTR ≥ 4% no lançamento e a mediana ≥ 800 em 7 d; senão **encerra** (fica no ar, sem produção) |
| **Clearance Required (en)** | **(a) encerrar** o formato; subir o 005 Tarawa (já pago) como último teste grátis | CTR 1,6% em 4.622 impressões: o YouTube distribuiu e ninguém clicou; o critério de corte da própria proposta já foi batido (média 51 views); o nicho viveu de 1 vídeo do canal-modelo | Tarawa até **14/12/2026**: só reabre (teste de 4 vídeos de "lugares restritos", tema largo) se tiver CTR ≥ 3% em ≥ 1.000 impressões ou 1.000 views em 14 d. Senão, fim |
| **Em Relevo** | **(c) adaptar**: temporada curta "Super El Niño no Brasil", **1 vídeo/semana**, + reembalar o vídeo do El Niño (grátis) | O conteúdo segura (El Niño: 59% de retenção em 12 min, CTR 3,2%, único que cresce sozinho); o que matou foi tema sem público atual + thumb escura; El Niño é evento longo e previsível (pico dez–fev) com vídeos de 1–2 mi em canais pequenos | 4 vídeos até 31/12; continua se CTR ≥ 3,5% no sugerido em 2 dos 4 **e** (1 vídeo ≥ 10 mil em 14 d ou média ≥ 3 mil); **corte antecipado** se os 2 primeiros tiverem CTR < 2% com ≥ 1.000 impressões; senão **encerra em 15/01/2027** |

**Noites liberadas:** dos 16 vídeos/semana do desenho original da noturna, ficam **Dossier 4 + historia 1 + Em Relevo 1 = 6**. A sobra **não** vai para mais Dossier por volume (o diagnóstico de 27/11 mostra que o gargalo dele é o CTR no teste, não a cadência). Vai para **(1)** caprichar na embalagem do Dossier (o portão comprovado) e **(2)** uma fase 1 sem custo de **canal novo no molde do Dossier**: refazer a matriz de idioma de 04/11 com dados de novembro entre **fr** (2º colocado, concorrência 9/10) e **pt** (3º; roteiro KGB pt já pronto; o Rodrigo revisa). Inglês segue eliminado (101 clones). Decisão de abrir é do Rodrigo, depois da fase 1.

---

## 1. O quadro geral (conferido no banco)

| canal | vídeos no ar | views | inscritos | impressões | CTR médio | gasto pago (USD) | USD por view |
|---|---|---|---|---|---|---|---|
| dossie-es | 14 | ~78 mil | 285 | 269.361 | **3,69%** | 146,13 | 0,002 |
| historia-ptbr | 15 | 2.088 | 21 | 18.473 | 3,42% (v1 puxa; v2 ~2,4%) | 126,77 | 0,061 |
| em-relevo | 5 | 406 | 3 | 4.213 | 2,18% | 4,01 | 0,010 |
| lugares-guerra-en | 5 | 255 | 0 | 4.622 | **1,64%** | 8,52 (5,74 do bolso) | 0,033 |
| lotr-fr (stand-by) | — | 28 mil (2024) | 291 | 2.907 | 5,30% | 0,50 | — |

O custo principal dos três canais fracos não é dinheiro (Codex derrubou imagem para ~US$ 0; voz ~US$ 1), e sim **noites da fábrica, cota do Max e atenção**. Esse é o custo de oportunidade que pesa.

A regra que vale nos 4 canais, agora com 4 amostras independentes: **o YouTube dá a cada vídeo novo um lote de 400–3.000 impressões nas primeiras 48 h; CTR < 2% nesse lote encerra a distribuição**. Dossier: Medellín 0,54%, Núremberg 1,6%. historia: URSS 0,2%, EUA 0,7%, Inglaterra 1,3%. Clearance: todos < 2,5%. Em Relevo: Seca 1877 0,99%. Retenção boa não salva vídeo que não passou desse portão.

## 2. historia-ptbr
**Diagnóstico.** 26 dias, 15 vídeos, US$ 6 por inscrito (Dossier: centavos). v1 (001–005, títulos-fórmula "A história INTEIRA / N ANOS de X") teve mediana de 163 views em 7 d e CTR 4,5%; v2 (006+) teve mediana de 17 e CTR 2,4%. Os títulos-pergunta com paradoxo ou acusação ("prometeram o que NÃO cumpriam", "por que faltava comida", "importava reis") ficaram em 0,2–1,3% sobre 430–2.500 impressões. A exceção (Rússia "Chamaram um VIKING…", 7,4%) tem nome concreto e cena. Retenção também abaixo do Dossier: 55–70% a 5% do vídeo (Dossier 81%), 22–43% na metade (Dossier 57%).
**Ressalva crítica:** não é só título. França e Alemanha saíram com o título-fórmula da v1 e receberam 190–290 impressões em 7 d, e Roma só 74 (lançada 1 dia antes da Rússia). Parte do problema é tema (país europeu moderno, já com dono: Genius, History in Minutes) e lançamentos colados que dividem o teste.
**Mercado.** Em pt, "história inteira de país" é loteria: "História em minutos" (homônimo, 6 mil inscritos) fez 275 mil e 206 mil e depois < 26 mil, e mudou de assunto; Crônicas de Ferro fez Irã 1,5 mi e depois 5–8 mil, e mudou para "vida medieval"; 3 clones de outubro mortos. ~3 de ~37 vídeos do formato em pt passaram de 100 mil. O canal-modelo em inglês caiu para 2–3 mil por vídeo em novembro. RPM pt de história US$ 1–2,8 (**Hipótese**, tabela da fábrica). Levar países para en/es não resolve (en tem dono; em es o público de história já é do Dossier).
**Opções.** (a) encerrar: zera custo, perde o estilo dos bonequinhos que o Rodrigo gosta. (b) pausar: mesmo efeito, sem aprendizado. (c) adaptar para "como era viver": nicho em alta em pt em 2026 (6 canais com < 7 mil inscritos fizeram 196–808 mil), o bonequinho falando com "você", com humor, se diferencia da enxurrada de reconstrução realista por IA; custo ~US$ 1–3/vídeo. (d) manter países: os dados dizem que repete o resultado.
**Recomendação: (c)**, com 5 temas de exemplo e evidência:

| tema | evidência (vídeo de 2026) |
|---|---|
| Como era atravessar o Atlântico numa caravela em 1500 | 334 mil |
| A corte portuguesa chega ao Rio (1808): como era viver lá | 790 mil |
| Você não sobreviveria a um inverno medieval | 333 mil e 566 mil |
| Um dia na vida de um soldado romano | 228 mil, canal de 1,4 mil inscritos |
| Por que o Brasil fala português | 808 mil, canal de 6,5 mil inscritos |

Regras do teste: hook com cena física nos 15 s; título com fato concreto, nunca pergunta-paradoxo; 12–15 min; **nunca dois lançamentos colados**. Nome do canal colide com o homônimo: trocar antes é decisão do Rodrigo. Cuba (privado) e Argentina (não subiu) já estão pagos: publicar com título-fórmula serve de controle grátis.

## 3. Clearance Required (lugares-guerra-en)
**Diagnóstico.** 5 vídeos (13–21/11), 255 views, 0 inscritos, CTR 1,6% em 4.622 impressões (sugerido 1,3%; Bikini 1,1%), % visto 27–40% em vídeos de 15–17 min. **Não foi falta de distribuição**: cada vídeo recebeu 400–1.600 impressões de teste e caiu para < 10/dia. 5 vídeos bastam para condenar: a Cosa Nostra demorou 10 dias para explodir, mas tinha CTR de 4–8% desde o início; aqui nenhum passou de 2,5%.
**Mercado.** O sub-nicho escolhido vive de 1 hit: o canal-modelo fez 6,3 mil, 900, 23 mil e 13 mil nos 4 mais novos; Civil War Fine Print fez 1,4 mi uma vez e depois 0,6–9 mil; o concorrente mais parecido (Hollow Cairn) tem mediana 771. O nicho largo é enorme, mas os vencedores fazem outra coisa (gravação no local, listas animadas, explicadores de tema largo de 11–15 min). O nosso (arquivo + documento + voz calma + só guerra americana) é o mais "de museu". Dossier em inglês segue eliminado (101 clones; até o Archive in Minutes cai para 3,5–7,5 mil). RPM en US$ 4–8 (**Hipótese**), irrelevante sem tração.
**Recomendação: (a) encerrar.** Último teste sem custo: publicar o 005 Tarawa e, se CTR < 2% nas ~1.000 primeiras impressões, trocar a thumb uma vez. Se passar (CTR ≥ 3% em ≥ 1.000 impressões ou 1.000 views em 14 d até 14/12), aí sim um teste de 4 vídeos de "lugares restritos" de tema largo (Runit Dome 9,4 mi na ABC; Fort Drum 4,7 mi; Area 51 3,3 mi; Kaho'olawe 1 mi na Vox; Diego Garcia). O mais provável é não passar: a vaga do inglês volta para o `playbooks/novo-canal.md`, atrás de um formato em que dê para chegar primeiro.

## 4. Em Relevo
**Diagnóstico.** 5 vídeos (11–18/11), 406 views, 3 inscritos, CTR ponderado 2,2%. Seca 1877: 0,99% em 1.814 impressões no sugerido, aparecendo ao lado de "Brasil Urgente" e política (o YouTube não sabia para quem mostrar). El Niño 2026: CTR 3,2% no sugerido, 59% de retenção em 12 min, apareceu ao lado de notícias de El Niño e subiu de 20 para 163 views entre 21 e 28/11 sem vídeo novo. Mesmo tema, mesma semana: o Cosmos Brutal (844 inscritos) fez 100 mil com globo saturado e "DEZEMBRO CRÍTICO"; nós, 163 com mapa escuro e "SÓ 2 °C?". **Problema de tema e de embalagem, não de conteúdo.** 5 vídeos não julgam o formato, mas condenam a linha "desastre histórico / evergreen sem público atual".
**A "perspectiva certa" que os dados sugerem:** o canal foi pensado pelo que sabemos fazer (relevo, dado NASA, desastre do passado); o espectador clica numa pergunta urgente sobre algo que já está acompanhando. **O mapa é a resposta, não a promessa.**
**Hipóteses do Rodrigo, avaliadas:** (i) gancho de evento: confirmado, mas exige entrega em 24–72 h, que a fábrica não tem; a exceção viável é o Super El Niño (meses, previsível; canais de 3–6 vídeos fizeram 1,1–2,2 mi). (ii) "Por que o estado X é assim": a onda pt de outubro saturou (Explica no Mapa caiu de ~1 mi para ~2 mil em 5 semanas). (iii) en/es: teto e RPM melhores (El Mecanismo, es, é quase um Em Relevo e cresce), mas seria canal novo sem embalagem provada. (iv) Shorts de mapa: evidência fraca (os que explodem são ficção de guerra).
**Recomendação: (c)**, temporada El Niño. Pausar (o estado atual) é a pior opção: não decide, não aprende, e a janela de dezembro–fevereiro passa.

| tema | evidência |
|---|---|
| Onde o El Niño bate primeiro no Brasil | O POVO 423 mil, Cosmos Brutal 100 mil |
| Por que o El Niño seca o Norte e afoga o Sul | 2,2 mi; JeanGrafia 150 mil e 146 mil |
| Toda vez que veio um Super El Niño: 1983, 1998, 2015 | Primo Rico 1,33 mi, BBC 1,47 mi |
| O verão mais quente: o calor que vem com o El Niño | Band 337 mil, Fatos Desconhecidos 1,15 mi |
| O que o satélite mostra do El Niño agora | Sou curioso?! 1,1 mi |

Se passar, o passo seguinte é a versão es. Se encerrar, o motor 3D (relevo + NASA) é ativo para um canal en/es futuro.

## 5. Custo de oportunidade e o que fazer com as noites
- **Capacidade real:** o gargalo da noturna é a cota de imagem do Codex (um vídeo de cada vez, Dossier → História) e a semana do Max (`conhecimento/capacidade-fila.md`). Tirar 3 noites do historia, as 4 do Clearance (já pausadas) e reduzir o Em Relevo a 1/semana libera ~10 vagas/semana.
- **Não colocar no Dossier por volume:** o diagnóstico de 27/11 não comprovou ganho com cadência; o que derrubou Medellín, Núremberg e Yakuza foi CTR no teste (e, na Yakuza, arquivo trocado). A folga do Dossier deve ir para embalagem e QA (conferir 1ª frase do arquivo no ar).
- **Canal novo no molde do Dossier** é o melhor uso das vagas, porque é o único formato da fábrica com hit comprovado. Ordem da matriz de 04/11: es (feito) → **fr 6,30** (empate técnico, concorrência 9/10, RPM melhor que pt; o Rodrigo não lê francês, revisão mais difícil) → **pt 5,65** (demanda menor, mas roteiro pronto e revisão fácil). Próximo passo: fase 1 sem custo (refazer demanda/concorrência com dados de novembro e uma amostra), o Rodrigo aprova, depois produz. O lotr-fr não muda a conclusão; só é argumento a favor do fr (canal fr com 291 inscritos e CTR 5,3% mostra que há público francófono alcançável, mas é outro nicho).
- **Prioridade sugerida das noites:** Dossier 4 (com embalagem reforçada) > Em Relevo 1 (janela do El Niño fecha em fevereiro) > historia 1 > fase 1 do canal novo (pesquisa; não ocupa noite de produção).

## 6. Decisões do Rodrigo (nada foi executado)
1. Tirar a série de países do historia-ptbr da noturna (agendados 28/11–06/12: Ucrânia, México, Otomano, Grécia, Vikings, Itália) e aprovar o teste "como era viver" (e o nome novo do canal).
2. Encerrar o formato do Clearance: descartar os 6 temas agendados (inclui Runit hoje; só não roda pela pausa no `noturna.env`) e publicar o 005 Tarawa.
3. Aprovar a temporada El Niño no Em Relevo e a reembalagem do vídeo do El Niño.
4. Autorizar a fase 1 (US$ 0) do canal novo no molde do Dossier (fr × pt).

## 7. Achados de qualidade de dados (para corrigir depois; não mexi)
- `youtube.videos.publicado_em` vazio em vários vídeos no ar do historia (a comparação v1 × v2 da bíblia exclui esses vídeos).
- Em Relevo: título no ar do vídeo 4 truncado ("O El Niño causou seca no Nordeste e..."); Seca 1877 ainda com "matou" no título, contra a bíblia; backlog mostra Granizo agendado para hoje com o canal fora da noturna; 006 (pronto) e 007 (com roteiro) parados.
- Clearance: backlog ainda com 6 temas agendados apesar da pausa.
- Export do Studio defasado (historia 20/11, em-relevo 14/11): falta CTR do Studio dos vídeos recentes; os números de CTR acima são da Reporting API.
