# Em Relevo · temporada "Super El Niño no mapa" — proposta (fase 1) · 28/11/2026

Brief: `~/workspace/referencias/BRIEF-em-relevo-temporada-el-nino.md` (com o adendo "manter o formato, otimizar a retenção"). **Status: proposta, aguarda aprovação do Rodrigo.** Nada foi agendado, nada mudou no vídeo publicado, na fila nem nos timers. **Custo pago: US$ 0** (thumbs em código com dado NASA/NOAA; yt-dlp via WARP; Data API só leitura; crivos e pesquisa na cota do Max).

Arquivos desta pasta:
| arquivo | o quê |
|---|---|
| `mercado/MERCADO.md`, `refs.csv`, `mosaico-outliers.jpg`, `lado-a-lado-cosmos-x-nos.jpg`, `thumbs/` | o que está dando certo no tema (542 vídeos, 29 outliers, padrões de título/thumb, autocomplete, Cosmos × nós) |
| `retencao/RETENCAO.md`, `frames/`, `metricas-videos.json` | como 7 canais (4 gringos, 3 brasileiros) seguram a audiência × a curva do nosso 002 |
| `embalagem/EMBALAGEM.md` (+ r1, r2) e `crivo-r1/r2/r3-*.md` | os 6 vídeos com 3 pares título+thumb cada, 3 rodadas de crivo independente e o resultado |
| `thumbs/*.jpg` (+ `-320.jpg`), `thumbs/kit/` | amostras reais (3 do E1 + 1 do 002) e o código que as gera (US$ 0) |
| `mosaico-sugerido.jpg` | nossas amostras no meio das thumbs que performam, com título embaixo, como no sugerido |
| `dados-nino34.json` | o dado próprio do E1 (Niño 3.4 diário NOAA, 1982/1997/2015/2026) |
| `backlog-temporada-proposta.md` | os 6 temas prontos para o backlog (não carregados: ver §6) |

## 1. O que está funcionando agora (`mercado/MERCADO.md`)
- **"Brasil + consequência + tempo" vence, não o mapa:** 13 dos 20 maiores outliers pt têm o Brasil/lugar como sujeito, 9 têm "(Super) El Niño" + marco de tempo; pergunta sim/não é minoria. Metade dos outliers pequenos é corte do Sérgio Sacani (não replicável).
- **Thumb que pega:** satélite/globo com o Pacífico "em brasa" + 2–3 palavras (13/20; 17/20 saturadas). O nosso 002 tinha mapa vetorial plano escuro + "SÓ 2 °C?".
- **Cosmos Brutal 100 mil × nosso 163:** mesmo tema, mesma semana, canais minúsculos. Diferença = embalagem (globo fotorrealista + "DEZEMBRO CRÍTICO" + Brasil no título) e **distribuição** (o YouTube nos deu 595 impressões). O nosso CTR já é razoável (3,2%; 4,2% em 21–26/11): o gargalo é entrar na corrente com cadência e embalagem que o algoritmo teste.

## 2. Os 6 vídeos (2/semana, 3 semanas) e o título favorito
Calendário se aprovado até 30/11: sem. 1 = 30/11–06/12 · sem. 2 = 07–13/12 · sem. 3 = 14–20/12. Detalhes, evidência e obrigações de roteiro em `embalagem/EMBALAGEM.md`.

| sem. | vídeo | título favorito | crivo |
|---|---|---|---|
| 0 | **002 reembalado** (US$ 0, no Studio) | Super El Niño: por que falta chuva em Manaus e sobra em Santa Catarina | **aprovado** (r2) |
| 1 | **E1** Pacífico recorde | O Pacífico passou 1997 e 2015: o que o Super El Niño já faz com o Brasil | par A aprovado; B e C com correção (r3) |
| 1 | **E2** Roraima | Super El Niño: por que Roraima seca quando o resto da Amazônia chove | **aprovado 3/3** (r3) |
| 2 | **E3** Calor no Sudeste/CO | A frente fria que não chega: o Super El Niño no verão do Sudeste | 2/3 (r3) |
| 2 | **E6** Rio Iguaçu | O rio Iguaçu que passou dos 10 metros no El Niño de 1983 | 0/3 (fatos corrigidos no r3; a cheia de set–out/2026 já aconteceu, vira o gancho) |
| 3 | **E4** Vai faltar luz? | Vai faltar luz no Brasil com o Super El Niño? | 2/3 (r3) |
| 3 | **E5** Sertão | Por que o Sertão fica sem chuva quando o Pacífico esquenta | 2/3 (r3) |
| reserva | **E7** La Niña 2027 | (fim de janeiro, só com "La Niña Watch" da NOAA) | — |

**Crivo honesto:** 3 rodadas com revisores novos a cada rodada; 1ª: 1 de 21 pares; 2ª: 3 de 19; 3ª: 002 + E1-A + E2 inteiro + 7 pares avulsos. Pela regra, par reprovado na 3ª fica bloqueado; como é fase de proposta, **cada vídeo refaz a embalagem na etapa 1** (com thumbs reais e crivo próprio), partindo das correções já escritas (`EMBALAGEM.md`, última seção). Os erros pegos foram reais (fato errado de régua do Iguaçu, "seca primeiro" falso, previsão vendida como certeza, título que era manchete de TV): o crivo funcionou.

**Amarração da temporada (sem anunciar vídeo futuro):** "termômetro do Pacífico" com o Niño 3.4 do dia no 1º capítulo de todo episódio (assinatura + número fresco); callback de 1 frase + card para o episódio já publicado que explica o mecanismo; playlist "Super El Niño no mapa" e tela final com o anterior; mesma família de thumb.

**CTR ≥ 6%:** nos nossos canais, vencedor no sugerido faz 4–6,5% nas primeiras ~2 mil impressões e estabiliza em 3,4–4%. 6% é teto de vencedor, não média. Pares com mais chance (Hipótese): 002 (Manaus × SC + "MESMA CAUSA?"), E1-A, E2-C, E4-C, E5-B.

## 3. Estrutura dos vídeos (mesmo formato: motion 3D + imagem/vídeo real)
Esqueleto de 10–13 min, a partir do que segurou no 002 e do que os referência fazem (`retencao/RETENCAO.md` §5), levado à bíblia (`biblia/roteiro.md`, seção "Temporada El Niño — proposta"):

| tempo | o que acontece | visual |
|---|---|---|
| 0:00–0:15 | lugar + data + **cena física com gente** + o número | foto/vídeo real de chão → mapa A |
| 0:15–0:35 | contraste (2º lugar) + **consequência para você** | mapa em movimento contínuo |
| 0:35–0:50 | pergunta do título + **loop adiado** ("no fim eu mostro…") | troca A→B no corte; barra de capítulos sem narração |
| 0:50–1:30 | **1ª peça da resposta com número** (sem "mas antes", sem cardápio) | dado em 3D |
| 1:30–2:45 | mecanismo em ≤ 75 s amarrado a um lugar do hook | diorama/globo em movimento + 1 foto |
| 2:45–4:30 | revelação em degraus (recordes, termômetro novo) | régua 3D ao vivo |
| ~4:00 | **CTA ponte** (1 frase + botão 2 s) | sobre o mapa |
| 4:30–9:00 | região por região, cada uma com consequência + foto de chão + pergunta do espectador | A↔B a cada ~20 s; foto ≤ 60–90 s |
| 9:00–10:30 | o tempo/histórico | arquivo, satélite |
| 10:30–11:30 | A RESPOSTA + pagamento do loop | volta ao mapa do hook |
| 11:30–12:10 | "manda para quem mora em…" + inscrição | — |

## 4. Como otimizar a retenção (adendo do Rodrigo)
Amostra: The Last Day (5,3 mi), RealLifeLore (2,4 mi), UnderTheHeadline (4,1 mi), El Mecanismo (2,3 mi, es) × CanalSingularidade (2,2 mi), Sou curioso?! (1,1 mi), Cosmos Brutal (100 mil). **Onde o 002 cai:** 0:44–2:41 perde 24 pontos (a lista falada das 4 perguntas, o "mas antes, é preciso entender", a aula da "piscina", com câmera parada em 2 crossfades); depois cai só ~1 pt/min; degraus menores quando responde o título (42%), "a última pergunta" e o quadro de cortiça. Ritmo de corte **não** separa os hits; o que todos têm é cena física no hook, promessa paga no fim e algo novo a cada 15–20 s.

Melhorias baratas, em ordem de impacto (todas cabem no formato atual):
1. Cortar a ponte: nada de cardápio falado nem "mas antes"; 1ª resposta com número até 1:30.
2. Loop adiado no hook, pago no último minuto e meio (os 2 hits pt/es fazem isso aos 0:48–0:50).
3. Câmera nunca parada até 2:00 (trocas só no corte).
4. Mecanismo em ≤ 75 s, depois da 1ª revelação, amarrado a um lugar do hook.
5. Não fechar a pergunta do título antes de ~75%; ao fechar uma pergunta, abrir a próxima.
6. ≥ 2 imagens reais de chão com pessoas nos primeiros 15 s.
7. "Você" e uma consequência pessoal até 0:30 e uma por capítulo (002: 0,3 "você"/min; hits pt: 1,2–1,3).
8. Não anunciar o fim ("a última pergunta", cortiça longa no final).
9. CTA de inscrição como ponte aos ~30–35%.
10. Imagem real a cada ≤ 60–90 s (vídeo de domínio público NASA/NOAA quando houver).
11. 0,5–1 s sem trilha antes das revelações.

## 5. Novo padrão de thumb (2 linhas) e a reembalagem do 002
**Padrão:** satélite fotorrealista claro e saturado (ou fundo claro) com **1 herói de dado real em brasa** (NOAA/NASA), **Brasil sempre contornado em branco**, 1–2 palavras Anton amarelas com contorno grosso; sem IA, US$ 0. Teto por playlist: 1 "globo com língua quente" e 1 "Brasil laranja × azul" no ar ao mesmo tempo.
**002:** título "Super El Niño: por que falta chuva em Manaus e sobra em Santa Catarina" + thumb `thumbs/r002-mesma-causa.jpg` (Brasil de satélite com a chuva medida pela NASA em out–nov: Amazônia abaixo da média, PR/SC acima, "MESMA CAUSA?"). Aprovado no crivo r2. Antes de trocar, anotar impressões/CTR do dia para medir antes × depois.

## 6. Backlog e pendências
- **Backlog:** **não carreguei** os 6 temas no `youtube.backlog`: o `backlog.py agendar` (rotina seg/qui) distribui automaticamente todo item `proposto` do Em Relevo nas noites livres. Os 6 estão em `backlog-temporada-proposta.md` com o comando pronto; carregar só depois do sim do Rodrigo (e decidir se o canal volta ao `noturna.env`).
- **Granizo (id 28, agendado hoje):** o canal está fora da noturna desde 17/11 e o Rodrigo recusou o tema → sugiro **descartar**. Os ids 30–33 (litoral RS, neve, cânions, geada negra) são evergreen sem corrente → **tirar a data** durante a temporada. O id 29 (calor) é absorvido pelo E3.
- **006 Caraguatatuba (pronto, não publicado):** desastre histórico, o tipo que falhou (003: CTR 1%). Não publicar no meio da temporada (dividiria o teste das 48 h); se a temporada passar no critério de 15/01, subir como catálogo; senão, arquivo.
- **007 Vendavais PR (roteiro pronto):** quente vencido (evento de novembro) → não produzir; os dados do Simepar entram como capítulo do E6 (Sul).
- Achados de dado (já no relatório de portfólio): título do 004 truncado no ar; "matou" no título do 003.
- **Critério da temporada** (decisão de portfólio de 28/11): continua se CTR ≥ 3,5% no sugerido em ≥ 2 dos primeiros 4 **e** (1 vídeo ≥ 10 mil em 14 d ou média ≥ 3 mil); corte antecipado se os 2 primeiros tiverem CTR < 2% com ≥ 1.000 impressões; encerra em 15/01/2027.
