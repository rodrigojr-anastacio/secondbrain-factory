# Backlog — História em minutos

Título padrão: "A história INTEIRA de X em N minutos" (N = duração real). IDs = `youtube.videos.youtube_id`.

<!-- backlog-vivo:inicio (gerado por tools/rotinas/backlog.py; não edite à mão) -->

## Backlog vivo (24/11/2026 17:47)

Fonte da verdade: tabela `youtube.backlog` (DDL `tools/db/schema_backlog.sql`); esta seção é espelho, gerada por `tools/rotinas/backlog.py md`. Reordenação seg/qui depois do garimpo (rotina `backlog`); a produção noturna (`tools/rotinas/noturna.py`) produz 1 vídeo por canal nas noites de sáb, dom, seg e ter (20:00), pegando o 1º item agendado; a data abaixo é a **noite de produção**; quem escolhe o dia de ir ao ar é o Rodrigo (a fábrica só sugere a janela). Nota = (demanda × encaixe × urgência)^(1/3). Item em produção ou além é congelado.

### Noites de produção (próximos 14 dias)

| noite | pode ir ao ar | tema | status |
|---|---|---|---|
| ter 24/11 | sex ou sáb | — (vaga) | |
| sáb 28/11 | dom ou seg | Império Otomano | agendado |
| dom 29/11 | seg ou qua | Grécia Antiga | agendado |
| seg 30/11 | qua ou sex | Vikings | agendado |
| ter 01/12 | sex ou sáb | Itália | agendado |
| sáb 05/12 | dom ou seg | — (vaga) | |
| dom 06/12 | seg ou qua | — (vaga) | |
| seg 07/12 | qua ou sex | — (vaga) | |
| ter 08/12 | sex ou sáb | — (vaga) | |

### Temas (ordem da fila)

| id | tema | nota (D·E·U) | status | noite (ao ar) | janela do tema | evidência principal |
|---|---|---|---|---|---|---|
| 47 | Império Otomano | 5.5 (7·8·3) | agendado | sáb 28/11 (dom ou seg) | perene | [yt-dlp ytsearch "história do Império Otomano": BBC News Brasil 537.938 views](https://www.youtube.com/watch?v=lRyzKUXDqoA) |
| 48 | Grécia Antiga | 5.5 (7·8·3) | agendado | dom 29/11 (seg ou qua) | perene | [yt-dlp ytsearch "história da Grécia Antiga completa": Tinocando TV 1.920.645 views](https://www.youtube.com/watch?v=l4cy3ni-4dE) |
| 17 | Vikings | 5.0 (7·6·3) | agendado | seg 30/11 (qua ou sex) | perene | [Reconstrução Histórica (pt, 70,6 mil insc.): 'Os Vikings | Como Desapareceu o Povo Mais Temido do Mundo' 420.711 views (22/04/2026; 6× os inscritos)](https://youtube.com/watch?v=4BmrcZ-TEtQ) |
| 49 | Itália | 4.7 (5·7·3) | agendado | ter 01/12 (sex ou sáb) | perene | [yt-dlp ytsearch "história da Itália Roma": EconoSimples 332.954 views](https://www.youtube.com/watch?v=qZiew5iz6MM) |

Prontos/publicados recentes: Portugal (publicado, ter 17/11); União Soviética (URSS) (pronto, qui 19/11); Inglaterra / Reino Unido (pronto, sex 20/11); Espanha (pronto, sáb 21/11); Cuba (pronto, dom 22/11); Argentina (pronto, seg 23/11)

<!-- backlog-vivo:fim -->


| # | Tema | Status | Data | ID |
|---|---|---|---|---|
| 001 | A história INTEIRA do Egito em 17 minutos | publicado (republicado; o upload original `s-D5Sk7prJI` saiu do ar) | 2026-11-03 | g847Td0Plsk |
| 002 | A HISTÓRIA COMPLETA da Índia em 19 minutos | publicado | 2026-11-03 | MV5SSjoccqE |
| 003 | A história INTEIRA do Irã em 18 minutos | pronto v2, aguardando publicação (youtube.videos id 5; videos/003-ira/entrega/) | 2026-11-05 | — |
| 004 | A história INTEIRA da China em 16 minutos | pronto, no Drive, aguardando publicação (youtube.videos id 10; videos/004-china/entrega/) | 2026-11-05 | — |
| 005 | A história INTEIRA do Brasil em 17 minutos | pronto, no Drive, agendar seg 09/11 (youtube.videos id 12; videos/005-brasil/entrega/) | 2026-11-07 | — |
| 006 | A história INTEIRA de Roma em 17 minutos | pronto, no Drive, aguardando publicação (youtube.videos id 13; 1º da bíblia v2; videos/006-roma/entrega/) | 2026-11-09 | — |
| 007 | A história INTEIRA da Rússia em 17 minutos | pronto, no Drive, aguardando publicação (youtube.videos id 16; 2º da bíblia v2; videos/007-russia/entrega/) | 2026-11-09 | — |
| 008 | A história INTEIRA da França em 15 minutos | **pronto** 13/11 (15:16, checklist v2 13/14, US$ 9,41 fal+Fish; youtube.videos id 33; `videos/008-franca/entrega/`, falta subir ao Drive); publica dom 15/11 | 2026-11-15 | — |
| 009 | A história INTEIRA da Alemanha em 17 minutos | etapa 1 pronta 13/11 (roteiro v2 checklist APROVADO, 2.179 palavras, 215 imagens planejadas; youtube.videos id 37; `videos/009-alemanha/ETAPA1-PRONTA.md`); etapa 2 pronta 13/11 (17:22, −15,2 LUFS, 0 telas pretas, thumbs A/B/C, `entrega/`; `videos/009-alemanha/ETAPA2.md`); publica seg 16/11 | 2026-11-16 | — |
| 010 | Japão: T1 "O Japão COPIAVA todo mundo. Por que ninguém o conquistava?" / T2 "Como o MAR protegeu o Japão (até o dia em que parou)" | PRONTO 14/11 (etapa 2: vídeo 15:23 entregue no Drive, thumbs A/B/C, custo ~US$ 1,7; publicação a confirmar). Etapa 1 pronta 14/11 (1º com embalagem + crivo antes do roteiro: aprovado na r2; roteiro v2 checklist APROVADO, 2.006 palavras, ~16 min, 218 imagens planejadas pelo Codex; youtube.videos id 40; `videos/010-japao/ETAPA1-PRONTA.md`); publica qua 18/11 (data a confirmar) | 2026-11-18 | — |

## Próximos: ordem recomendada em 09/11/2026 (`pesquisa/proximos-temas-2026-11/RELATORIO.md`)
| Ordem | Tema | Evidência [O] | O que medir (vs. Egito/Índia: ~1 mil impressões, CTR 3,7–4%, 42–45% visualizado) |
|---|---|---|---|
| 006 ✔ (pronto 09/11) | **Roma** | Maior demanda pt: med. top-10 (12 m) 544 mil, 21 vídeos > 100 mil; porta aberta (Arquivos do Velho Mundo, 3,3 mil insc., 425 mil); no molde curto em pt o melhor tem 24,9 mil; liga com o Egito. Hook: Breno e o "ai dos vencidos" (Lívio 5.48) | impressões no dia 7 (meta > 2 mil), % tráfego de Pesquisa, CTR, % visualizado |
| 007 ✔ (pronto 09/11) | **Rússia** | Clone "História em minutos" (08/2026, 5 mil insc.) fez 235 mil em 21 dias, ~120× o Japão do mesmo canal; HiM en 43 mil. Risco: guerra atual (fechar em ~1991–2000, neutro). Hook: "nossa terra é grande e rica, mas não há ordem nela" (862) | impressões no dia 7, % tráfego de Sugeridos (Hipótese: Rússia vem por navegação) |
| 010 ✔ (etapa 1 em 14/11) | Japão | Med. 12 m 138 mil; Genius en **1,0 mi** (`ecnCTOzIivE`, 14/10/2026; medido 14/11); História do Mundo (05/2026) 106 mil; mas o clone fez só 2 mil. Liga com a China | — |
| depois | Portugal (sessão com o Brasil, med. 159 mil), França (clone 167 mil), Alemanha (178 mil) | | |
| evitar | Ucrânia e Israel (demanda é da guerra atual), Otomano e Britânico (19–27 mil em pt), Mongóis (53 mil) | | |

### Histórico (temas que performaram nas referências; views em 04/11/2026)
- Roma (Genius History 364 mil; HiM 19 mil) · Japão (CountryCorns 115 mil) · Rússia (HiM 42 mil) · Ucrânia (HiM 178 mil) · Império Britânico · Jerusalém
- Fora deste canal: organizações/serviços secretos (Gestapo, KGB, Mossad…), em avaliação para um canal novo.
