# Por que o YouTube não entrega (impressões) e o que fazer — 11/11/2026

Brief: `~/workspace/referencias/BRIEF-entrega-youtube.md`. Custo: **US$ 0**. Data API: **~870 de 2.000 unidades** (casos 645 + diagnóstico 223). Nada foi alterado no YouTube, no banco, em `canais/`, `tools/` ou `skills/`.
Detalhe e links completos: [notas-oficiais.md](notas-oficiais.md) (55 afirmações oficiais), [notas-comunidade.md](notas-comunidade.md) (19 teorias), [casos-hit.md](casos-hit.md) (14 canais), [diagnostico-canais.md](diagnostico-canais.md) (nossos 4 canais). [O] = observado · [I] = inferido. Páginas da Central de Ajuda consultadas em 11/11/2026.

## Resumo (o que realmente pesa)
1. **O YouTube avalia cada vídeo pela resposta de uma amostra pequena.** Canal novo não tem histórico, então ele usa o tema e o metadado para escolher essa amostra. Se ela clica e assiste, o vídeo escala; se não, para ali. Não existe sandbox nem gatilho fixo de impressões (Beaupré, 01/09/2026).
2. **Conta, IP, aparelho, agendamento, tags, selo de IA e monetização não mudam o alcance.** O YouTube nega cada um oficialmente, e os nossos próprios canais confirmam: historia-ptbr e dossie-es, na mesma conta e no mesmo aparelho, recebem home e sugeridos normalmente.
3. **O Em Relevo não tem problema de embalagem, tem problema de distribuição.** 0 views da home, 0 de sugeridos e 7 impressões; um CTR ruim exigiria centenas de impressões para aparecer. Os suspeitos são o **canal reaproveitado**, que tinha conteúdo antigo de outro tema e não tem tópico atribuído, e a **estreia com notícia de tragédia**, em que o YouTube dá prioridade a CNN e emissoras. Antes de concluir, falta descartar no Studio uma **restrição ou reivindicação** (vídeo 1 com 33 trechos de terceiros).
4. **Os hits de canal novo têm um padrão:** o hit é o **vídeo nº 1** (13 de 14 casos), sobre um tema ou molde que **outro vídeo já tinha provado** dias ou semanas antes (9 de 10). Título com contraintuição e número, thumb de um conceito só, 12–26 min. Do vídeo 2 em diante as views caem 10–100×. É loteria do primeiro teste, com o bilhete escolhido a dedo.
5. **historia-ptbr e dossie-es estão recebendo o teste normal.** O gargalo deles é CTR e retenção da amostra, ou seja, thumb, título e primeiros 30 s.

## Teorias: veredito
| Teoria | Veredito | Evidência curta | Fonte (data) |
|---|---|---|---|
| IP/VPN/proxy no upload | **Mito** | Recomendação depende de quem assiste; teste algum isola IP | [Vidpros 07/02/2026](https://vidpros.com/upload-location-matters/) |
| Vários canais na mesma conta/aparelho | **Mito** (alcance) · **Fato** (risco) | Recurso oficial (até 50 canais). Nossos canais irmãos têm tráfego. Mas punição grave por spam atinge os canais ligados | [Fliki 28/10/2024](https://fliki.ai/blog/youtube-shadowban) |
| Canal reaproveitado/troca de nicho "queima" | **Plausível** | Único A/B achado: canal adormecido 0 impressões × canal novo 4 mi (n=1). [O] Em Relevo sem `topicDetails`; historia-ptbr (reaproveitado, mas vazio) funciona | [r/PartneredYoutube 28/01/2026](https://reddit.sentinel-team.org/posts/1qouqxm/snapshots/2026-01-28T02%3A11%3A20.926346Z) |
| Apagar vídeos antigos "limpa" o canal | **Mito** | YouTube: não apague, isso corta a ligação com o público; vídeo fraco não pune o canal | [Beaupré/SEJ 25/03/2024](https://searchenginejournal.com/youtube-warns-channels-against-deleting-videos/512126) · [Ajuda 16559651](https://support.google.com/youtube/answer/16559651) |
| "Sandbox" de canal novo | **Mito** (sem fonte) | Não há fonte oficial; o que existe é o teste com amostra | [Beaupré 01/09/2026](https://www.youtube.com/watch?v=rHLjxrbXmmY&t=1927s) |
| Conta "envelhecida" | **Mito** | Só vendedor de automação defende; vários hits vêm de canal parado, sem prova de causa | [casos-hit](casos-hit.md) |
| Agendar / subir privado e esperar 24–48 h | **Mito** | Ritchie: 24–48 h = 24–48 s. Exceção útil: esperar a **verificação de direitos** terminar | [SEJ 12/11/2025](https://www.searchenginejournal.com/youtube-debunks-24-48-hour-upload-delay-recommendation/560613/) |
| Primeira hora decide | **Mito** | Não decide pelas primeiras horas nem pelas primeiras 1.000 pessoas; vídeos crescem meses depois | [Beaupré 01/09/2026](https://www.youtube.com/watch?v=rHLjxrbXmmY&t=1927s) |
| Compartilhar no WhatsApp "confunde o algoritmo" | **Mito** | A fonte de tráfego afeta principalmente ela mesma; externo é neutro (também não liga a distribuição) | [Ritchie/SEJ 20/02/2025](https://www.searchenginejournal.com/does-google-traffic-affect-youtube-recommendations-what-to-know/540280/) |
| Shorts atrapalham o longo | **Mito** (direto) · ajuda pouco | Histórico separado desde 2022; estudo de 19 mil vídeos: sem penalidade | [notas-comunidade #7](notas-comunidade.md) |
| Tags | **Fato:** peso mínimo | "Papel mínimo"; tag em excesso na descrição = spam | [Ajuda 146402](https://support.google.com/youtube/answer/146402) |
| Idioma do metadado / legenda | **Plausível** (busca) | Ajuda a indexar; sem dado de recomendação. [O] historia-ptbr com pt-PT recebe tráfego | [Ajuda 87604](https://support.google.com/youtube/answer/87604) |
| Categoria / país do canal | **Mito** | País do canal não afeta recomendação | [Ajuda 141805](https://support.google.com/youtube/answer/141805) |
| Vídeos em lote | **Mito** (2–3/dia) · **risco** (volume duplicado) | Sem limite de recomendação por canal; 10 canais com os mesmos Shorts foram a 0 | [Fliki 2024](https://fliki.ai/blog/youtube-shadowban) |
| Selo de IA/conteúdo alterado reduz alcance | **Mito** | "Não limita audiência nem monetização"; punição é **não** marcar quando obrigatório | [Ajuda 14328491](https://support.google.com/youtube/answer/14328491) |
| Monetização / selo amarelo muda alcance | **Mito** | "O sistema não sabe quem monetiza". Exceção: violento/gráfico pode ter menos recomendação | [Ajuda 141805](https://support.google.com/youtube/answer/141805) |
| Trocar título/thumb "reseta" | **Mito** | Sem re-ranking; o Testar e comparar existe para isso | [Creator Insider](https://recapio.com/digest/mythbusting-does-changing-your-title-or-thumbnail-re-rank-your-video-by-creator-insider) |
| Feito para crianças / restrição de idade / bloqueio | **Fato** | Corta recomendação ou visibilidade; aparece na coluna Avisos/Restrições | [Ajuda 9668091](https://support.google.com/youtube/answer/9668091) · [9684541](https://support.google.com/youtube/answer/9684541) |
| Trechos de terceiros (reutilizado) | **Fato** (monetização) · **plausível** (alcance) | Crédito não é licença; pode gerar reivindicação ou bloqueio por país; o YPP julga o canal inteiro | [Ajuda 1311392](https://support.google.com/youtube/answer/1311392) |
| Notícia/tragédia em tempo real | **Fato** (ranking) | Em notícia de última hora e desastre, busca e "A seguir" sobem fontes de autoridade (prateleira Breaking News) | [Ajuda 9057101](https://support.google.com/youtube/answer/9057101) · [Blog 4 Rs](https://blog.youtube/inside-youtube/the-four-rs-of-responsibility-raise-and-reduce) |
| Carona em tema em alta | **Plausível** (forte) | 9 de 10 hits vieram de tema provado antes; **exceto** notícia trágica | [casos-hit](casos-hit.md) |
| Copiar título/thumb de hit | **Plausível** · risco | Revelados (3 canais com o molde do "Brasil Oculto") fizeram 343–491 mil; cópia literal pode virar denúncia | [casos-hit](casos-hit.md) |
| Canais IA/faceless suprimidos | **Fato** (monetização/derrubada em massa) · **plausível** (alcance) | "Inautêntico" desde 15/07/2025; 16 canais derrubados em jan/2026; carta do CEO 21/01/2026 | [Tubefilter 21/01/2026](https://www.tubefilter.com/2026/01/21/neal-mohans-2026-letter-to-creators-a-lot-of-ai-a-tiktok-shop-competitor-and-beautifully-produced-tv-to-compete-with-netflix/) |

## Casos "1 vídeo, 300 mil+" (views em 11/11)
| Canal | Vídeos | Hit | Views | Gatilho [I] |
|---|---|---|---|---|
| Chão do Sul (pt) | 6 | #1, 22 min | 699 mil | carona no Canal Top10, 2 dias antes |
| RS/PE/MG Revelado (pt) | 6–7 | #1, 23–25 min | 343–491 mil | molde do "Brasil Oculto" |
| Professor Antares (pt) | 5 | #1, 8 min | 634 mil | "todos os tipos de X", perene |
| Umbral (es) | 9 | #1, 19 min | 629 mil | Cristo Redentor, já provado em pt |
| Naturaleza Secreta (es) | 9 | #1, 16 min | 2,39 mi | Marianas, em alta em en |
| Hindcast (en) | 8 | #1, 16 min | 1,82 mi | medo nuclear no noticiário |
| Gloam (en) | 3 | #1, 14 min | 2,49 mi | hack da Binance, 1 dia depois |
| How They Make Billions (en) | 2 | #1, 12 min | 595 mil | SpaceX no IPO |
| Prima Historian (en) | 4 | #1, 26 min | 451 mil | Israel + "Entire History" |
| SkyFury (en) | 5 | 1º longo, 21 min | 8,57 mi | Fukushima, reativado por desastre |

**Padrão:** o vídeo nº 1 sobre um **tema já provado** (outro idioma ou outro canal, nos últimos 30 dias), explicador longo com capítulos, título contraintuitivo com número e thumb de um conceito só (vários com **mapa 3D com seta**). Muitos canais estavam **parados e vazios** antes, não reaproveitados com outro conteúdo. Comentários elogiam narração "não IA".
**Não dá para copiar:** viés de sobrevivente (centenas de clones com mediana < 1 mil), o vídeo 2 não repete o hit, e cobrir evento em 24–48 h não cabe na nossa esteira.

## Diagnóstico dos nossos canais (01–11/11)
| Canal | Home | Sugeridos | Busca | Leitura |
|---|---|---|---|---|
| historia-ptbr | 174 | 169 | 19 | teste normal; CTR/retenção fracos (Egito 325, Índia 184 views) |
| dossie-es | 21 | 205 | 23 | teste normal; Mossad pegou sugeridos (299 views) |
| **Em Relevo** | **0** | **0** | 2 | **sem distribuição** |

Em Relevo [O]: canal `UCKoQhYctv1sAwTM0Rl1H9SA` (@emrelevobr), criado em 13/01/2024. Teve 746 views na vida, com pico em abr–mai/2026; os vídeos antigos foram apagados ou estão privados. `topicDetails` vazio (os outros canais têm Knowledge/Society). O vídeo 1 foi ao ar como "O que está acontecendo com o clima no Sul do Brasil?", sem "tornado" no título, sem legenda e com **22 links** na descrição. Os dois vídeos estão com idioma do metadado **pt-PT**. Não é feito para crianças (no canal), não tem restrição de idade nem bloqueio regional visível na API. Existe um **homônimo @emrelevo** (criado em 25/06/2026, "dado do IBGE em mapa").

### Causas de "zero impressões", em ordem de checagem
| # | Causa | Provável? | Como testar |
|---|---|---|---|
| 1 | Verificação de direitos em andamento, ou reivindicação/bloqueio no vídeo 1 (33 trechos) | média | Studio > Conteúdo > coluna **Restrições/Avisos** > Direitos autorais |
| 2 | Aviso ou strike herdado da fase antiga do canal | média | Configurações > Canal > **Qualificação de recursos**; **Monetização**; e-mails do Studio |
| 3 | "Feito para crianças" no vídeo (declarado só é visível ao dono) | baixa | Detalhes do vídeo > Público; Configurações avançadas |
| 4 | **Canal reaproveitado frio**, sem tópico e com público antigo de outro tema | **alta** | Analytics > Público ("o que seu público assiste"); vídeo 2 em 48 h–7 d |
| 5 | **Estreia com tragédia/notícia** (fontes de autoridade na frente) | **alta** (vídeo 1) | Busca deslogada: o topo é só de veículos? O vídeo 2 (menos "breaking") recebe home/sugeridos? |
| 6 | Título genérico, pt-PT, sem legenda, 22 links | baixa | Explica busca fraca, não home = 0 |

**Teste natural em andamento:** o vídeo 2 (El Niño) não tem trecho de terceiros, tem legenda e é menos "notícia". Se até **18/11** (7 dias) ele não passar de ~100 impressões e continuar com 0 de home e de sugeridos, com o Studio limpo (causas 1–3), o problema é o canal.

### Manter, limpar ou canal novo?
- **Limpar não adianta**: os vídeos antigos já saíram do ar e o YouTube desaconselha apagar.
- **Critério:** o dele (3 vídeos ou ~2 semanas com < ~500 impressões/vídeo em 7 dias → canal novo) vale, mas o caso atual está 50× abaixo disso. Proposta: **decidir em 18/11** com o vídeo 2. Se ele tiver < 100 impressões e 0 de home/sugeridos, e o Studio estiver limpo, ir para o **canal novo já**, sem esperar o 3º vídeo.
- **Canal novo:** criar na mesma conta (não há prova de que conta separada ajude) e deixar vazio até a estreia. O 1º vídeo é o mais importante do canal: tema **perene e provado**, não tragédia em curso. Antes de subir lá, deixar o vídeo correspondente privado no canal velho, para não haver duplicata pública.

## Plano de ação (impacto ÷ esforço)
1. **Rodrigo, 5 min no Studio:** fazer os prints da lista abaixo, que fecham as causas 1–3.
2. **Se houver reivindicação no vídeo 1:** cortar ou substituir o trecho no Editor do Studio, ou deixá-lo privado. Daqui para a frente, no Em Relevo, só trechos CC BY/domínio público até o canal ter tração. Hoje a regra é "crédito sem pedir autorização", e crédito não é licença.
3. **Decidir o Em Relevo em 18/11** pelo critério acima. Se for canal novo, a estreia é um tema perene provado em outro idioma ou canal nos últimos 30 dias (ex.: "Por que o Sul tem tornados", formato explicador, sem notícia de vítimas).
4. **Tema do 1º vídeo de todo canal novo** (Negócios, Em Relevo 2.0): pela regra "provado nos últimos 30 dias em outro idioma/canal + sem versão longa boa no nosso idioma". É o padrão de 9 dos 10 hits.
5. **historia-ptbr e dossie-es:** o problema é a amostra. Trabalhar thumb e título (COROA × TURBANTE; título contraintuitivo com número) e os primeiros 30 s. Usar o Testar e comparar em todo vídeo. Ver os mesmos números do Studio por vídeo (CTR e retenção das primeiras 48 h).
6. **Metadado zero-custo:** mudar o idioma padrão de upload para **pt-BR** (Configurações > Padrões de upload) nos canais pt, enviar a legenda do vídeo 1, pôr o termo buscado no título ("tornados") e deixar só links essenciais na descrição (créditos com nome, sem 22 URLs).
7. **Quente sem tragédia:** no Em Relevo, o "quente" só depois de o canal ter público. Preferir ângulo explicativo e perene (o que é, por que acontece) a "o desastre de ontem".
8. **Lançar no banco** (orquestrador): channel_id do Em Relevo, vídeo 1 (`G26KHotlMIw`) e vídeo 2 (`YqNMNhFCPpM`), e os `youtube_id` de Roma, Rússia, KGB, Masones e Cosa Nostra. Se o Rodrigo quiser, ele roda `tools/auth.py em-relevo` para a coleta diária ler o canal.
9. **Proteção contra "inautêntico":** manter variação real de roteiro e visual entre vídeos e canais, e nunca subir o mesmo vídeo em vários canais no mesmo dia (para outro idioma, faixa de áudio extra no mesmo vídeo).
10. **Longo prazo (decisão dele):** separar canais em contas Google diferentes só reduz o risco de punição em cadeia, não melhora o alcance. Baixa prioridade.

## O que pedir ao Rodrigo do Studio
Canal **Em Relevo**:
1. **Conteúdo > Vídeos**, sem filtro: print com Visibilidade, **Restrições**, Data e Views. Mostra os antigos (tema e data) e qualquer reivindicação.
2. Vídeo 1 > **Direitos autorais/Verificações**: tem reivindicação? De quem? Bloqueia ou só monetiza?
3. **Configurações > Canal > Qualificação de recursos** e **Configurações avançadas** (público, país).
4. **Monetização**: status ou aviso de "conteúdo reutilizado".
5. **Analytics > Alcance** dos vídeos 1 e 2: impressões, CTR e **origens de tráfego das impressões** (onde as 7 apareceram), em 48 h e 7 dias.
6. **Analytics > Público**: "o que seu público assiste" e "canais que seu público assiste".
7. O canal **@emrelevo** (homônimo) também é dele?

**historia-ptbr e dossie-es** (por vídeo, 48 h e 7 dias): impressões, **CTR**, origens de tráfego e retenção nos 30 s. Comparar com o Egito, que recebeu home.

## O que NÃO fazer
- Comprar canal "envelhecido", views, inscritos ou usar sub4sub/proxy "para sair do zero": viola os termos (spam/engano) e não ajuda.
- Apagar em massa vídeos antigos achando que limpa o canal.
- Subir o mesmo vídeo em vários canais, ou duplicado no mesmo canal, ao mesmo tempo.
- Usar vídeo de TV/emissora ou trecho longo de terceiros (Content ID; 3 strikes derrubam o canal).
- Copiar literalmente a thumb ou o título de concorrente (risco de denúncia por spam ou engano). Usar o molde, não a cópia.
- Deixar de marcar "conteúdo alterado" quando a IA mostrar pessoa real ou evento realista falso. Imagem estilizada e voz própria não precisam.
- Encher a descrição de tags ou links (conta como spam).
- Concluir pelo CTR com 7–15 impressões: é ruído.
