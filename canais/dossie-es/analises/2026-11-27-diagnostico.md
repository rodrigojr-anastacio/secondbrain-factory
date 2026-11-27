# Dossier en Minutos: diagnóstico da queda e plano de ajustes (27/11/2026)

Só leitura e análise: nada foi mudado no canal, no backlog, na bíblia nem nos vídeos. Custo pago: US$ 0.
**Fontes:** Analytics API (dados até 24/11, atraso de ~3 dias), Reporting API em `youtube.alcance_diario` (impressões e CTR por origem, até 25/11), export do Studio de 27/11 e 24/11 (`youtube.studio_video`), yt-dlp via WARP (títulos das fontes de sugerido, busca do tema, download de 144p da Yakuza no ar). Brutos e scripts em `2026-11-27-dados/` (`puxar.py`, `dados.json`, `grafico.py`). Gráfico: `2026-11-27-retencao.png`. Crivo da proposta da Yakuza: `2026-11-27-crivo-yakuza.md`.

## 0. Achado principal: o vídeo da Yakuza no ar é o arquivo do GRU
- `Donlim7AJMg` ("YAKUZA: la mafia que tenía su nombre en la puerta") dura **13:48 (827,9 s)**. O render da Yakuza tem **13:25 (804,6 s)**. O do GRU tem **827,9 s**.
- Baixei a versão 144p do vídeo no ar (via WARP) e comparei os quadros em 0, 3, 10, 25, 40, 400 e 800 s: **são idênticos aos do `015-gru/entrega/video.mp4`** (Bruxelas 1941, o "empresario uruguayo"…). Quem clica em "Yakuza" ouve "Bruselas, mil novecientos cuarenta y uno…".
- Isso explica sozinho a **retenção de 24,5% (3:22 de média)**: todos os outros 13 vídeos do canal estão entre 48,6% e 66%. O roteiro, o hook e o ritmo da Yakuza **nunca foram testados**.
- Conferi os outros 13 vídeos: a duração no ar é a última legenda do render + ~3 s em todos (CIA 11:47, Mossad 13:43, FBI 13:17, Cosa Nostra 14:33, KGB 14:06, Masones 14:11, SS 14:29, Inquisición 14:17, Gestapo 14:06, Medellín 14:05, Templarios 12:39, MI6 13:50, Núremberg 13:49). **Só a Yakuza está trocada.**
- O GRU privado (`7fvdCeXaag0`, 13:48) tem a duração do GRU: provavelmente o mesmo arquivo subiu duas vezes.
- **Risco para os próximos:** GRU (13:48), MKUltra (~13:49) e Gulag (~13:50) têm quase a mesma duração. Conferir só a duração não basta: é preciso ver a primeira frase.

## 1. O que é a "queda" do canal
| | 23/11 | 24/11 | 24→27/11 (Studio, média/dia) |
|---|---|---|---|
| views do canal/dia | 17.795 | 15.823 | ~9.000 (+27.126 em 3 dias) |
| impressões/dia | 62.806 | 54.378 | ~34.000 (25/11: 32.917) |
| Cosa Nostra impressões/dia | ~42.400 | ~43.200 | ~26.400 (+79.110 em 3 dias) |
| KGB / SS impressões/dia | 7.498 / 8.204 | 5.116 / 3.168 | ~2.100 / ~1.550 |

- **A Cosa Nostra não caiu, mas a onda está perdendo força.** Ela ganhou +21 mil views em 3 dias (contra ~12 mil/dia em 23–24/11) e responde por 77% das views do canal em 28 dias (47.363 de 77.882). KGB e SS, que ganhavam audiência por estarem ao lado dela, também perdem força. O canal está em queda porque essa onda está passando: views/dia caíram ~45% do pico.
- O CTR do canal ficou estável em 3,5–3,7% de 21 a 25/11: a embalagem dos vídeos grandes não piorou.
- O problema de fundo: **nenhum vídeo novo desde a Gestapo (16/11) pegou a onda** para substituí-la.

## 2. Por que os vídeos novos não pegam: o teste no sugerido
Todo vídeo novo recebe nas primeiras 48 h um lote de impressões em **vídeos sugeridos**, ao lado da Cosa Nostra e dos clones "Archivo en Minutos". O CTR nesse teste decide se o YouTube continua mostrando o vídeo:

| vídeo (título no lançamento) | impressões no sugerido (teste) | CTR no sugerido | views em 7 d |
|---|---|---|---|
| SS (fórmula) | 5.073 (7 d) | **6,43%** | 2.318 |
| Gestapo ("GESTAPO: …") | 2.665 (7 d) | **4,20%** | 1.149 |
| KGB (fórmula) | 694 (7 d) | 4,32% | 613 (e explodiu no 7º dia) |
| Inquisición (fórmula) | 507 (7 d) | 5,33% | 370 |
| Masones (fórmula) | 311 (7 d) | 7,07% | 67 |
| Mossad (fórmula) | 3.123 (48 h) | 2,27% | 356 |
| **Medellín** (fórmula + subtítulo) | **2.983 (48 h)** | **0,54%** | 244 |
| **Núremberg** (fórmula) | **939 (48 h)** | **1,60%** | 141 (48 h) |
| **Yakuza** (T1 "YAKUZA: …") | **1.078 (~7 h)** | **0,83%** | 113 (Studio) |
| Templarios ("Cómo…") | 82 | 4,88% | 118 |
| MI6 ("Cómo…") | 81 | 7,41% | 179 |

Leitura:
- **CTR abaixo de 2% no teste encerra a distribuição.** Medellín recebeu quase 3 mil impressões no 1º dia, teve 0,54% e não recebeu mais nada (250 impressões entre 24 e 27/11). Núremberg e Yakuza seguiram o mesmo caminho. SS e Gestapo passaram de 4% e foram para a vizinhança da Cosa Nostra (SS: 20% dos sugeridos 7 d vieram da Cosa Nostra, 58% do "La historia COMPLETA de la Gestapo" do Archivo en Minutos).
- **Templarios e MI6 tiveram CTR bom, mas quase não foram testados** (~80 impressões): o YouTube não os viu como vizinhos da bolha (religiosas/ordens e um caso britânico). Esses dois vídeos não falharam pela embalagem: nunca chegaram a ser mostrados a quem assiste a bolha.
- De onde vêm os sugeridos dos vídeos que pegaram: os nossos (Cosa Nostra ↔ KGB ↔ SS ↔ Gestapo) e os clones do **Archivo en Minutos** (Gestapo 319 mil, MI5 62 mil, Mosad 18 mil, SS 5,5 mil) e "militares informados" (Guerra Fria na América Latina, 104 mil). Público: homens 45+ (~70%), MX, AR, ES, VE, PE, US.
- Quase todas as views são de não inscritos, por sugerido + navegação. A leitura do orquestrador ("os novos são vistos quase só por recorrentes") está certa: os recorrentes são os espectadores da Cosa Nostra, alcançados pela navegação (home) e pelas telas finais. Nos vídeos novos que falharam, as telas finais + página do canal são 35–56% das views (MI6 56%, Templarios 36%, Núremberg 31%).

## 3. Retenção (mesma métrica, desde a publicação)
![retenção](2026-11-27-retencao.png)
- Cosa Nostra, KGB, SS, Gestapo, Medellín, Inquisición, MI6: curva parecida, 85–87% a 5% do vídeo, 59–66% na metade, ~47–54% no fim. **Roteiro e formato estão bons** (retenção relativa 0,46–0,57 contra vídeos do mesmo tamanho).
- **Núremberg é a exceção real:** 78% já a 2% (~17 s) e 72% a 5%, contra 88–91% dos outros. No ponto da queda, a narração diz "Para ese crimen, inventó una palabra. Se leyó en voz alta el primer día del juicio…": é um hook sobre uma palavra, abstrato, enquanto o da Cosa Nostra (juramento com sangue no santo, 0:00–0:25) e o da KGB (o guarda-chuva na ponte de Waterloo) são cenas físicas. Núremberg também é um **evento**, tema que a bíblia já marca como fraco.
- **Yakuza:** não há curva útil (o arquivo errado + só ~2 dias de dados; a API ainda não tem linhas dela). O hook do render certo segue a estrutura da Cosa Nostra e da KGB: lugar e data, a cena do ataque a Itami em 0:03, "Esta es TODA la historia de la Yakuza" em 0:25 e a promessa 184.000 → 17.600 em 0:31. Pela estrutura, ele não é o problema.

## 4. Hipóteses
| hipótese | a favor | contra | veredito |
|---|---|---|---|
| (a) bolha da Cosa Nostra / público errado | Os sugeridos vêm da Cosa Nostra/KGB/SS e dos clones Archivo en Minutos; temas fora da bolha (Templarios, MI6) quase não foram testados (~80 impressões) | Medellín (máfia, vizinho direto) foi testado com 3 mil impressões e falhou na embalagem; Inquisición (religiosa) teve 5,3% e pegou carona | **Parcial.** A bolha define *onde* o vídeo é testado; o que decide é o CTR nesse teste. Regra de `temas.md` (24/11) continua válida |
| (b) embalagem (CTR) | Os 3 que morreram tiveram CTR de 0,5–1,6% no teste do sugerido, contra 4,2–7,1% dos que pegaram; CTR na navegação (público do canal) segue alto (Yakuza 7,45%) | Templarios/MI6 tinham CTR bom e também não cresceram (falta de teste, não de clique) | **Confirmada: principal causa** dos lançamentos fracos desde 18/11 |
| (c) cadência alta canibalizando | 4 lançamentos em 6 dias (20–25/11) no pico da Cosa Nostra; cada um teve só um lote pequeno de teste | Gestapo saiu 2 dias depois da SS e Inquisición 1 dia depois, e as duas pegaram; os inscritos são poucos (~350), então canibalizar inscritos pesa pouco | **Não comprovada.** Secundária; só dá para medir espaçando |
| (d) fórmula "TODA la historia…" × aposto | Fórmula no lançamento: Cosa Nostra, KGB, SS, Inquisición, Masones com 4,3–8,5% no teste | Fórmula também em Medellín (0,54%) e Núremberg (1,6%); Gestapo com aposto teve 4,2%; o crivo mostrou que a fórmula já existe e flopou no tema Yakuza em es (Era Span 66 views; Pioneros y Leyendas 1.731, 0,38×) | **Inconclusiva.** Quem decide é o tema reconhecível para o público da bolha, não o molde. Obs.: vários títulos no ar já não são os do lançamento (SS "La Orden Negra…", KGB "…del Sótano de Lubianka al Piolet de México", CIA, Mossad, FBI, Medellín, Gestapo); o efeito disso não aparece separado nos dados |
| (e1) **erro de upload** | Yakuza = arquivo do GRU (quadros idênticos) | — | **Confirmada.** Explica a retenção de 24,5% |
| (e2) fim natural da onda | Impressões do canal: 62,8 mil (23/11) → 32,9 mil (25/11); KGB/SS caem junto com a Cosa Nostra | — | **Confirmada.** É a "queda" que o Rodrigo vê no total |

## 5. Ajustes propostos (não executados), por impacto e facilidade
| # | ajuste | por quê | esforço |
|---|---|---|---|
| 1 | **Yakuza: deixar `Donlim7AJMg` privado e subir o `014-yakuza/out/video.mp4` (13:25) como vídeo novo**, com os pares abaixo | O vídeo no ar é o GRU; não há como trocar o arquivo de um vídeo publicado. Só 113 views se perdem | Baixo (Rodrigo, no Studio) |
| 2 | **Conferência pós-upload:** no Studio, duração = a do pacote **e** os primeiros 10 s = a 1ª frase da `legendas.srt` (anotar as duas no topo do `youtube.txt`) | GRU, MKUltra e Gulag têm ~13:48 cada; só a duração não pega a troca | Baixo (mudança na skill `pacote-youtube`, com aprovação) |
| 3 | **Regra das 48 h:** se o vídeo tiver CTR < 2% nas primeiras ~1.000 impressões de sugerido (Reporting API), trocar a thumb (e, se preciso, o título) no 2º dia | O teste do sugerido decide o vídeo; Medellín, Núremberg e Yakuza morreram no 1º dia | Médio (rotina de leitura + decisão dele) |
| 4 | **Próximos temas: vizinhos da bolha com o nome no começo do título dizendo o que é** ('Ndrangheta → "mafia de Calabria"), como já está em `temas.md` e `titulo.md` (24/11). Evitar eventos (Núremberg) e temas fora da bolha até haver uma 2ª família com impressões | Os temas que pegaram são organizações temidas ao lado da Cosa Nostra/Gestapo; Templarios/MI6 nem foram testados | Baixo (já é a regra) |
| 5 | **Hook com cena física nos primeiros 15 s** (sangue no santo, guarda-chuva), nunca uma ideia abstrata | Núremberg perdeu 22% da audiência em 17 s com hook de "palavra" | Baixo (bíblia `roteiro.md`, com aprovação) |
| 6 | **Espaçar lançamentos: 1 vídeo a cada ~48 h** e não lançar 2 na mesma semana fora da bolha | Teste limpo de cada vídeo; hipótese (c) não comprovada, mas é barato testar | Baixo |
| 7 | Medellín e Núremberg: **não trocar agora** | Medellín já trocou título e thumb (rosto do Escobar + "EXTRADICIÓN") e está com ~80 impressões/dia: a embalagem nova não reabriu o teste. Núremberg tem o problema no hook e no tema, e trocar a embalagem não conserta isso. Melhor gastar a energia nos próximos lançamentos | — |

### Proposta para a Yakuza (reupload)
| par | título | thumb |
|---|---|---|
| A | **"YAKUZA: la mafia japonesa que trabajaba para el poder"** (53 caracteres; pago em 0:27–0:31 "la mafia que no se escondía, porque trabajaba para el poder") | v2 A (costas tatuadas + katana), com "YAKUZA" grande **em cor papel** e na fonte pincelada (Yuji Boku, como manda a bíblia para tema asiático), sem o 組, mantendo o "¿LEGAL?" |
| B | "Cómo la Yakuza pasó de trabajar para Japón a ser su enemiga" (mantido) | v2 B (184.000 riscado, sol nascente) |
| C | "Japón, 1992: la Yakuza tuvo que esconder su nombre" (mantido) | v2 C (ruela de lanternas, cartão rasgado) |

- **Crivo (r1, 27/11):** Par A original ("YAKUZA: TODA la historia de la mafia japonesa en 13 minutos") **REPROVADO**: a fórmula já existe no tema em es e não rendeu (Era Span 66 views; Pioneros y Leyendas 1.731, 0,38× da mediana) e o Bebas ia contra a bíblia. Pares B e C **APROVADOS**. O Par A acima é a **correção pedida pelo próprio revisor** e não passou por uma 2ª rodada. Ressalva dele: A e B têm o mesmo homem tatuado de costas; não aproximar mais a A da B.
- Por que "mafia japonesa": é o termo dos maiores vídeos do tema em es (Vida de un Gángster 785.897; Black Mango 662.407) e cumpre a regra de 24/11 (dizer o que a organização é para o público da Cosa Nostra). "YAKUZA" abre o título, então o assunto fica claro em menos de 1 s.
- O que **não** muda: o vídeo (13:25), o roteiro e as thumbs B/C.

## 6. Como validar (o que medir e quando)
| ajuste | métrica | meta | quando |
|---|---|---|---|
| Yakuza reupload | CTR no sugerido nas primeiras 48 h (Reporting) · retenção média · views em 7 d | ≥ 2,5% · ≥ 55% · > 1.149 (Gestapo na mesma idade) | 48 h e 7 d após subir |
| Conferência pós-upload | vídeos com duração/1ª frase diferentes do pacote | 0 | todo upload |
| Regra das 48 h | CTR do sugerido antes × depois da troca de thumb | dobrar o CTR ou chegar a ≥ 2% | 3 d após a troca |
| Bolha (já em `temas.md`) | impressões em 7 d de 'Ndrangheta, Mafia rusa, ODESSA, Garduña × Templarios/MI6/Núremberg | ≥ 3× | 7 d após cada um |
| Hook físico | retenção a 5% do vídeo | ≥ 85% (Núremberg: 72%) | 3 d após publicar |
| Espaçamento 48 h | impressões no teste por vídeo | > 1.000 no sugerido em 48 h | 4 próximos lançamentos |

**Limites:** dados da Analytics API até 24/11 e da Reporting API até 25/11; Yakuza só pelo Studio e por ~7 h de Reporting. Não sabemos qual variante do "Testar e comparar" está vencendo (a Data API devolve o título A). O CTR do teste do sugerido como portão de distribuição é **Hipótese** forte (3 de 3 que caíram abaixo de 2% morreram; 4 de 5 acima de 4% com > 300 impressões cresceram; Masones, a exceção, ficou em 504), a confirmar com os próximos 4 lançamentos.
