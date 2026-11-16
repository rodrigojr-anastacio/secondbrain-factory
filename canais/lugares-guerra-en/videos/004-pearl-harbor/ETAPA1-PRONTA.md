# ETAPA 1 PRONTA — 004-pearl-harbor (15/11/2026, Opus)

**youtube.videos id 42** (status `roteiro`, título = T1). Custo pago da etapa 1: **US$ 0** (yt-dlp via WARP, Data API 35 unidades, search.list 0). Teto do vídeo (etapa 2): **US$ 4**. Publica qua 18/11/2026.

## Embalagem (crivo independente, APROVADO na r3)
- **T1 (título A, thumb A):** "Why Are There Still Bullet Holes at Pearl Harbor?" (49 car.) — aprovado em r1, r2 e r3.
- **T2 (título B, thumb B):** "The Pearl Harbor Wall Tourists Aren't Allowed to See" (52 car.) — r1 reprovou "Why Can't You Visit Most of Pearl Harbor?" ("most" sem número, resposta óbvia); r2 reprovou "Why Can't You Visit Pearl Harbor's Scarred Barracks?" (resposta "é base" óbvia); r3 aprovou o padrão documento/revelação.
- **Thumb (conceito):** close da fachada art déco do antigo quartel de Hickam com diagonal de 6 crateras grandes (brilho ciano fino no fundo), sombra de avião de hélice dos anos 1940 cruzando a parede; texto **"ON PURPOSE"** + selo RESTRICTED. r1 reprovou "NEVER FIXED" + portão; r2/r3 aprovaram. Detalhes e prompt em `THUMBS.md`.
- **Promessa:** as marcas de 7/12/1941 foram deixadas de propósito num quartel que hoje é o QG da Pacific Air Forces, atrás de um portão que o público não cruza sozinho; o vídeo mostra onde estão, por que ficaram e por que não se chega perto.
- **Onde o roteiro paga (tempos estimados a 168 ppm):** frase-âncora B01b–c (~0:15–0:25); pergunta de T1 literal ~0:28 (fim do B01c); de quem é a parede + "~2 miles from the dock" B02a–b (~0:38–0:55); o que mais está atrás do portão B03 (até ~2:20); motivo oficial ("a constant reminder to never again be caught unprepared") B08a (~5:15); 2ª camada (formulário NHL) B09 (~5:50–6:50); fecho volta à parede B18 (~14:40).

## O que está pronto
| Arquivo | Conteúdo |
|---|---|
| `BRIEF.md`, `EMBALAGEM.md`, `CRIVO.md`, `embalagem/` | pauta, pesquisa (refs.csv, medianas, mosaico), 3 rodadas do crivo (`crivo-r1..r3.md`, `EMBALAGEM-r1/r2.md`) |
| `SCRIPT.md` | roteiro final em inglês, 18 seções, **2.604 palavras** (~15:30 de fala; vídeo ~16:10 com pausas). 3 plantas: "count the marks" (B01→B18), algo atrás do vidro (B03→B11, a bandeira), "unprepared" (B05→B08/B18) |
| `FATOS.md` / `SOURCES.md` | 88 fatos com trecho literal e status (+ correções da pauta); bloco → fonte |
| `qa/split_blocos.json`, `blocos-voz.json` | 71 blocos de voz (≤ 48 palavras). `VOZ_SUBS` com horas e "P.O.W. M.I.A." por extenso |
| `roteiro.py` → `STORYBOARD.md`, `storyboard.json`, `blocos.json`, `cenas.json` | **190 planos, validação OK**: material real 85,2%, 0 imagem IA, 4 docs grifados / 5 citações lidas literalmente, 9 Cartelas QUOTED, 5 EntaoAgora, 3 mapas, 36 Números, 12 trechos de filme NARA. `cenas.json` = `[]` |
| `midia/` (fora do git, 83 arquivos, ~308 MB) + `midia.csv` + `licencas.md` + `tools/gera_midia_csv.py` | fotos 1940–41 (NARA 80-G, NHHC, USAF via Commons PD), hoje (DVIDS PD, Navy, HABS/HAER LoC), 7 docs, 7 filmes NARA 428-NPC recortados (2 em 1080p). Folha de contato `midia/_contato.jpg` conferida: sem corpo/ferido |
| `THUMBS.md` | A/B/C pareadas, mesmo texto "ON PURPOSE", prompt-base |
| `src/`, `tools/` | copiados do 003 (Dupla + Filme já existem em `componentes.jsx`; `build.py` trata Filme ≤ 7 s) |

## O que a etapa 2 precisa saber
1. **Thumb a partir do conceito aprovado** (`THUMBS.md`): A = T1, B = T2, C = variação de enquadramento; **o texto é sempre "ON PURPOSE"** (texto novo = sem crivo). 3º título do pacote = variação de T1/T2.
2. **Distância "about two miles"** (B02b, B17c, Mapa2D `porto`): coordenada do Hale Makai é aproximada (`FATOS.md` F81). Conferir antes do build; se der > 2,5 mi, trocar por "a few miles" no SCRIPT e no mapa (e rodar `split_blocos.py` + `roteiro.py`).
3. **Docs sem scan = Cartela QUOTED.** As 3 "recomposições tipográficas" (`doc_lei_…`, `doc_dvids_…`, `doc_dpaa_…`) **não** são documento escaneado: não usar como DocGrifo (o roteiro já não usa). Os 4 DocGrifo reais: despacho NARA 596244, NHL capa e pág. 2, FAQ do NPS. **Grifos estimados à vista** (`G` no `roteiro.py`): conferir nos stills.
4. **Filmes**: trechos por plano ≤ 7 s (regra do build). `filme_ford_hangares_…_nara76169` e `filme_pearl_navios_…_nara76169` têm timecode RTC no quadro: cortar/cobrir (crop) ou trocar trecho. `filme_casco_emborcado` não é usado (não confirmado se é Utah ou Oklahoma). `filme_ford_hangar_escombros` B14a cobre "That night…" com imagem diurna de 1941: aceitável como ilustração, sem Ficha de "night".
5. **Mapas**: `porto` (B02b), `oahu` (B06b, pousos dos 12 B-17), `memorial` (B12f: Arizona/Utah/Visitor Center em amarelo, **QG da PACAF em vermelho = fora do memorial**). Natural Earth é grosseiro para o porto: usar contorno de Pearl Harbor em escala de bairro (ou foto aérea PD `hoje_ford_island_aerea_2023` como base com pontos, Selo "POSITIONS APPROXIMATE").
6. **Regras de imagem**: nada de corpo, ferido, restos ou exumação (B16 usa só cerimônias, memorial e mapas). Sem insígnia do sol nascente em close (fotos japonesas 80-G-30550/30553 são vistas aéreas).
7. **Reuso 51%** (a parede do hook volta de propósito: `REUSO_LIBERADO`). Se o pré-QA achar repetitivo, há reservas no `midia.csv`: `foto_ford_avioes_queimando_1941`, `foto_ford_apron_ataque_1941`, `foto_ford_hangar_destruido_os2u_1941`, `foto_hickam_80g32846`, `hoje_torre_s84_habs_1992`, `hoje_hickam_ninho_corvo_b`, `hoje_hickam_memorial_1991`.
8. **Voz**: Fish "Narrator" (`0327fdb5…`, s2.1-pro, por frase, como 002/003). Conferir no Whisper: Hale Makai, Hickam, Oahu, Kahuku, Hawai'i, Higa, "B-17s", "P.O.W. M.I.A.".
9. **Sem gancho de próximo vídeo** (fecho só com o CTA genérico). **Créditos só na descrição** (a partir do `midia.csv`/`licencas.md`). Voz sintética declarada. Título/descrição/tags sem dead/death/killed (o roteiro fala "lost").
10. **Capítulos estimados** (recalcular com a voz real): 0:00 Count the marks · 0:31 The wall tourists aren't allowed to see · 1:24 Behind the gate · 2:23 The biggest barracks · 3:09 7:55 · 3:54 Twelve bombers, no ammunition · 4:37 The most bombed building on Oahu · 5:11 A constant reminder · 5:50 The paper behind the wall · 6:52 A birthmark · 7:37 The flag in the lobby · 8:30 Why the gate stays shut · 10:04 The island in the middle · 10:58 The honest part · 11:43 A bus, three days a week · 12:46 Eighty-five years · 13:39 What the tourist sees · 14:38 Count them again.
11. **QA da promessa** (`EMBALAGEM.md` › Obrigações): na `legendas.srt`, frase-âncora ≤ 0:30, pergunta de T1 ≤ 0:50, "de quem é a parede" ≤ 1:00, "reminder" entre 4:00 e 6:00.
12. **Para o Rodrigo conferir (candidatos; tempo real pela legendas.srt):** a parede do hook (B01), o despacho "NOT DRILL" (B05b), a bandeira 1941 × hoje (B11c), o formulário NHL lido (B09b).

## Checklist da bíblia (roteiro.md)
- [x] Hook abre com objeto real (a parede, foto oficial) + tarefa ("Count the marks"); 2 revelações no 1º minuto (de propósito; não se chega perto). A 3ª (a bandeira) só anunciada no B03 e paga no B11.
- [x] Pergunta do título dita literalmente em ~0:28.
- [x] 3 plantas pagas; fecho volta à parede do hook.
- [x] ≥ 4 documentos lidos e grifados (4); ≥ 1 então × agora (5); ≥ 3 números grandes (36); ≥ 2 mapas (3).
- [x] Toda afirmação em `SOURCES.md`; material só PD (`licencas.md`; japonesas com justificativa).
- [x] 2.600–2.900 palavras (2.604); capítulos a montar na descrição.

## Pendências (menores, contornadas)
- `af.mil` e `pacaf.af.mil` bloqueiam a VPS (Akamai): citações oficiais lidas via Wayback; DPAA lido via DVIDS. Sem captura de tela dessas páginas → Cartela QUOTED.
- Hickam NHL: mês da designação diverge (set × out/1985): o roteiro diz só "1985".
- Mortos em Hickam: 121 (NHL/NPS 1984) × 189 (Air Force, memorial de 1991): o roteiro atribui "the Air Force counts 189".
