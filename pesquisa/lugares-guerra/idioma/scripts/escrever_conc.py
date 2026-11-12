import json, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R = os.path.dirname(BASE)
T = open(BASE + "/dados/tabelas.md").read(); S = json.load(open(BASE + "/dados/stats.json")); DEM = json.load(open(BASE + "/dados/demanda_en.json"))
def k(n): return f"{int(n):,}".replace(",", ".")
FEITO = {"iwo jima": "WTS (4,5 mi)", "omaha": "WTS (341 mil + Normandy 119 mil)", "cheyenne": "WTS (4,9 mil, flop)", "okinawa": "WTS (Hacksaw 94 mil)"}
NAOMIL = {"chernobyl": "não militar (ref.)", "alcatraz": "prisão (não guerra)", "area 51": "militar secreto, não guerra"}
rows = []
for t, d in sorted(DEM.items(), key=lambda x: -x[1]["top10_med"]):
    obs = FEITO.get(t) or NAOMIL.get(t) or ""
    rows.append(f'| {t} | {d["n"]} | {k(d["top10_med"])} | {k(d["lug_top10_med"])} | {d["gt100k"]} | {d["gt100k_ano"]} | {d["gt1m"]} | {d["why_n"]} | {k(d["top1"])} · {d["top1_t"][:42]} [{d["top1_c"][:18]}] | {obs} |')
DEMT = "| Tema | Vídeos (≥4 min, en) | **Mediana top-10 (bruta)** | Mediana top-10 (só lugar) | ≥100 mil (total) | ≥100 mil (últimos 12 m) | ≥1 mi | Títulos why-can't/still | Nº 1 | Já feito |\n|---|---|---|---|---|---|---|---|---|---|\n" + "\n".join(rows)
s = S["stats"]
NTAB = len(set(sum([S["ids"][x] for x in ("a","b","cw","c")], []))) + 2
txt = f"""# CONCORRÊNCIA e DEMANDA: canal de "lugares / arquivos de guerra" (Where They Stood + Civil War Fine Print)

Data: 2026-11-12 · Agente: Tendências (etapa 1, 3b-concorrência e demanda en do `playbooks/novo-canal.md`) · Dados brutos: `pesquisa/lugares-guerra/dados.json` e `idioma/dados/` · Scripts: `idioma/scripts/`.
Legenda: **[O]** observado (YouTube Data API, busca do YouTube via yt-dlp + WARP) · **[I]** inferido ou estimativa. Idade do canal = 1º vídeo lido (ou criação, quando só li os 100 vídeos mais novos).

---

## Resumo executivo

1. **A fórmula do Where They Stood (WTS) tem dono e clones mortos [O].** Em 5 semanas surgiram **{s['b_wts']['n']} canais** copiando o título/tema do Iwo Jima ({s['b_wts_puros']['n']} deles abertos depois de 27/09). Mediana das medianas: **{s['b_wts_puros']['mediana_das_medianas']} views**; só **{s['b_wts_puros']['com_melhor_ge_10k']}** canal passa de 10 mil no melhor vídeo; **0** passam de 5 mil de mediana. Quase todos repetem **o mesmo lugar** (14 títulos da mesma pergunta sobre Iwo Jima).
2. **Mas a família "por que X ainda está lá / por que não pode visitar" já tem 3 canais de verdade com tração, e o WTS não foi o primeiro [O]:** Forgotten Fleet (7,27 mi de views em 254 dias, 15,2 mil inscritos, mediana 10,8 mil, hits de 1,16 mi, 777 mil, 583 mil, 15 posts em 30 d), Ship Tales (1,55 mi em 48 dias, 1,07 mil inscritos; "Why Did America Raise Pearl Harbor's Other Battleships" 943 mil) e Insight Ship (USS Utah 469 mil). Mais IT'S HISTORY (894 mil inscritos; "Why Cheyenne Mountain is Totally Forbidden" 313 mil em 2025). O formato vem funcionando desde 2024 com tema "lugar/navio dos EUA"; o WTS acertou o tema mais famoso.
3. **Teto do nicho (c) [O]:** Yarnhub 18,7 mi views/mês (3,42 mi inscritos), Mark Felton 4,2 mi/mês, Kings and Generals 4,8 mi/mês, Operations Room 1,1 mi/mês; canais novos de guerra com tração: Warlines (2,33 mi em 141 d), WW2 Vellob (2,0 mi), Frontline Echoes (1,46 mi em 110 d). Ou seja: o nicho paga e cabe canal pequeno novo, mas a mediana típica de canal novo bom é **~1–10 mil**, não 1 mi.
4. **Civil War Fine Print (CWFP) é cedo demais para julgar [O]:** 5 dias, 1 longo de 882 mil e o 2º longo com 5 mil; 1 Short de 209 mil. Só 2 clones diretos (o melhor com 62 views). O gênero "fotos que você não deveria ver" existe em compilação de 100+ fotos (canais Mystery in History, com 7,6 mi de views, e Past in Pictures, com 1,0 mi), que não é o molde do CWFP.
5. **Demanda en por tema (34 temas, §4) [O]:** o ranking bruto é dominado por documentário de batalha de TV. Tirando batalha/ataque/vlog ("só lugar"), os que importam são **Diego Garcia (836 mil de mediana, 12 vídeos ≥100 mil), Iwo Jima (785 mil; já tomado), Falklands (714 mil), Pearl Harbor (414 mil, 9 ≥100 mil no último ano), Omaha (383 mil; WTS), Bikini (207 mil)**. Midway e Wake "só lugar" são fracos (96 mil e 104 mil), mas têm vídeos-teto de 3,3 mi e 17 mi.
6. **Risco de hit único [O] (§5):** WTS = 87% das views em 1 vídeo (Iwo Jima; foi o **vídeo nº 2**, não o nº 1), mas a **mediana sem o hit é 29,4 mil** e 7 de 10 vídeos passam de 25 mil; CWFP = 79% das views totais (99% dos longos) em 1 vídeo. Compatível com o padrão do `entrega-youtube-2026-11/RELATORIO.md` (tema já provado + queda de 13–150× depois), com uma diferença: o WTS não caiu a zero.
7. **Cota gasta: 1.085 unidades, 0 `search.list`** (videos.list 132 + channels.list 87 + playlistItems/videos 866; 440 buscas via yt-dlp/WARP sem cota; WARP funcionou o tempo todo).

---

## 1. Método
- **Buscas [O]:** 440 consultas no yt-dlp (WARP, 0 cota), 25–30 resultados cada: 108 de concorrência (fórmula, clones WTS, clones CWFP, nicho), 170 de demanda (34 temas × 5 consultas: "why can't you visit <tema>" em relevância e "este ano por views", "<tema> today", "<tema> documentary" em 2 ordens) e 162 de idioma. 6.381 vídeos únicos lidos com `videos.list`; 4.296 canais com `channels.list`; **301 canais** com os 100 vídeos mais novos lidos (`playlistItems` + `videos.list`) para views/mês e mediana. As tabelas abaixo trazem **{NTAB} canais** (os demais {301-NTAB} ficam em `dados.json`).
- **Views/mês [I]:** canal < 1 ano = views ÷ idade × 30 (superestima canal com 1 hit: ver §5); canal antigo = views dos longos dos últimos 90 dias ÷ 3, só dentro dos 100 vídeos mais novos (**piso**). **Mediana** = só vídeos ≥ 4 min. Idade pelo 1º vídeo lido; "+" nos vídeos = só os 100 mais novos.
- **Classificação [I]:** por regex no título (fórmula: "can't visit / off limits / what's still under-at / why is X still there / sealed since…") + lugar de guerra; a classificação é minha e há zonas cinzentas (ex.: Dann e Frames of the Past entram como clone por 1 título).
- **Limites:** busca do YouTube devolve amostra (top ~30 por consulta), não o universo; canais sem nenhum título na amostra ficam de fora.

## 2. Mapa de concorrência

{T}

Resumo por grupo [O]: (a) fórmula exata (< 1 ano, {s['a']['n']} canais): mediana das medianas {k(s['a']['mediana_das_medianas'])}, {s['a']['com_melhor_ge_100k']} com vídeo ≥ 100 mil, {s['a']['com_mediana_ge_5k']} com mediana ≥ 5 mil · (b1) clones WTS ({s['b_wts']['n']}): mediana das medianas {s['b_wts']['mediana_das_medianas']}, {s['b_wts']['com_melhor_ge_100k']} com vídeo ≥ 100 mil (os 3 são canais de navio ou de outro assunto, não clones puros), mediana de inscritos {s['b_wts']['mediana_inscritos']} · (b2) CWFP e parentes ({s['b_cwfp_e_parentes']['n']}): ignorar a mediana, o grupo mistura listas de fotos.

**Leituras [I]:**
- **Quem faz bem não é clone do Iwo Jima**: Forgotten Fleet, Ship Tales, Insight Ship e IT'S HISTORY fazem "por que X ainda está lá" com tema **diferente** a cada vídeo (navios de Pearl Harbor, Bismarck, PT-109; cidades dos EUA). Sugere que o motor é **curiosidade de uma pergunta concreta + lugar/objeto famoso dos EUA**, não o título exato do WTS.
- **Clone com título literal fracassa** (mediana {s['b_wts_puros']['mediana_das_medianas']}; o melhor clone literal do Iwo Jima, WW2 Sitrep, tem 910 views; o melhor com outro lugar, Long After The Guns em Wake Island, 6,2 mil) [O]; hipótese: anti-spam do YouTube para conteúdo repetido e canais de 0–3 inscritos sem ritmo.
- **Teto realista de canal novo bom [I]:** Forgotten Fleet e Ship Tales chegam a ~0,9 mi views/mês com 1–15 mil inscritos, **mas** a mediana deles é 10,8 mil e 1,7 mil: a receita vem dos 3–4 hits de 0,5–1,2 mi por canal.
- **Ritmo:** Forgotten Fleet 15 vídeos em 30 d; Ship Tales 23; WTS 11 em 38 d. Quem tem tração posta quase diário [O]. Nosso ritmo humano de 3/semana é menor [I].

## 3. Ângulo "documentos" (Civil War Fine Print)
- **CWFP [O]:** 6 vídeos em 5 dias; longo 1 = 882 mil (14 min, retratos/fotos de época, título "The Pictures of Lincoln's Death You Weren't Supposed to See"); longo 2 = 5 mil ("What Happened to the Man Who Hosted General Lee's Surrender?"); Shorts 5 mil, 11,6 mil, **209 mil** ("They Stripped the Room Where the Civil War Ended") e 3,2 mil. Mediana dos Shorts 8,3 mil.
- **Clones diretos [O]:** The Union And Confederacy (copiou o título do Lincoln em 11/11: 62 views; canal com 16 vídeos e 78 inscritos) e Shrapnel ("Why Weren't You Supposed to See These Pictures of Lincoln's Death?", 7 views). Cloaked History ("History Lied About Lee's Surrender", 235 mil, 3,6 mil inscritos, fev/2026) é parente anterior, mediana 389.
- **Buscas do gênero [O]:** "Photos you weren't supposed to see" devolve compilações antigas (WhoRemembers 4,5 mi, Mystery in History 229 mil) e o clickbait "100+ photos"; "declassified documents" devolve listas de segredos da CIA (Visual Venture 1,07 mi); "the telegram that changed history" devolve Zimmermann (Extra History 662 mil). **Não há** um canal de longos com 1 documento por vídeo além do CWFP [O, na amostra].
- **Leitura [I]:** o CWFP prova que "1 documento/foto + 1 pessoa real" vende; o 2º longo (5 mil) mostra que a **escolha do tema (Lincoln) carrega**. É a mesma lição da fórmula do WTS: o tema pesa mais que o hook.

## 4. Demanda em inglês por tema (34 temas)
Filtro: vídeos ≥ 4 min, não ao vivo, título cita o tema, idioma en; pool de 5 consultas por tema. "Só lugar" tira batalha/ataque/guerra/vlog/documentário de batalha, para medir a demanda pelo **lugar hoje**, que é a do formato. Últimos 12 m = desde 12/11/2025.

{DEMT}

**Leituras:**
- **Bruta × "só lugar" [O]:** Midway cai de 2,92 mi para 96 mil, Wake de 714 mil para 104 mil e Guadalcanal de 1,39 mi para 283 mil: quase tudo é documentário de batalha. O formato "lugar hoje" **precisa** de pergunta (acesso/proibição), não só do tema; por isso o hit do WTS foi o único com "Can't Visit".
- **Prova do "why/still" [O]:** títulos com essa forma têm teto alto em Pearl Harbor/navios (Forgotten Fleet 1,16 mi, 777 mil, 583 mil; Ship Tales 943 mil; Insight Ship 469 mil; IT'S HISTORY 313–408 mil em Cheyenne e North Brother).
- **Vagas [O]:** temas com 0 títulos "why can't/still" no top da amostra: Corregidor, Tinian, Okinawa (fora o Hacksaw), Peleliu, Guadalcanal, Kwajalein, Gettysburg, Antietam, Appomattox, Andersonville, Camp Century.
- **Top-10 por demanda bruta (todos os temas, incluindo não-guerra):** Area 51, Chernobyl, Alcatraz, Hiroshima, Midway, Omaha, Iwo Jima, Falklands, Okinawa, Guadalcanal. **Só militares/guerra, excluindo os já feitos pelo WTS:** Hiroshima (5,05 mi bruta, mas é documentário da bomba, não "lugar hoje"; o filtro não a separa), Midway, Falklands, Guadalcanal, Pearl Harbor, Lincoln, Gettysburg, Diego Garcia, Wake, Bastogne.
- **Pesos reais [I]:** a mediana do top-10 de temas gigantes (Area 51, Alcatraz) vem de MrBeast/Mark Rober, não do formato.

## 5. Risco de hit único

| | Vídeos longos | Views totais | % do nº 1 | Mediana | Mediana sem o nº 1 | Média sem o nº 1 | ≥ 25 mil (sem o nº 1) |
|---|---|---|---|---|---|---|---|
| **WTS** (40 dias) | 11 | 5,22 mi | **86,9%** (Iwo Jima 4,54 mi) | 29,7 mil | **29,4 mil** | 68,6 mil | 7 de 10 |
| **WTS sem os 2 maiores** | 9 | 0,35 mi | – | – | 29,2 mil | 38,4 mil | 6 de 9 |
| **CWFP, longos** (5 dias) | 2 | 0,89 mi | 99,4% | 443 mil (n=2) | 5,0 mil (n=1) | – | 0 de 1 |
| **CWFP, todos** (longos + 4 Shorts) | 6 | 1,12 mi | 79,0% | 8,3 mil (Shorts) | 5,0 mil | – | – |
| Clones WTS puros (mediana de {s['b_wts_puros']['n']} canais) | – | – | 52% (mediana do share do nº 1) | 28 | – | – | – |

- **Fatos [O]:** o hit do WTS foi o **vídeo nº 2** (publicado 1 dia depois do 1º), não o nº 1; o tema (Iwo Jima) já tinha 26 vídeos "só lugar" ≥ 100 mil (demanda provada); os outros 10 vídeos do WTS somam 686 mil, e o 3º (Omaha, 341 mil) caiu 13× do hit; o 8º (Normandy, 119 mil) 38×; os 3 vídeos mais recentes (≤ 7 d) ainda estão acumulando (27 mil, 7 mil, 29,7 mil), então a mediana sem o hit é um **piso**.
- **Contra o padrão do relatório de 11/11 [O × I]:** o `entrega-youtube-2026-11/RELATORIO.md` diz "o hit é o vídeo nº 1, sobre tema já provado, e do vídeo 2 em diante as views caem 10–100×". O WTS **cumpre**: tema provado (Iwo Jima 785 mil de mediana, formula com precedente em IT'S HISTORY e Forgotten Fleet) e queda de 13–150× do hit. **Difere** em dois pontos: hit foi o nº 2, e o piso é alto (29 mil de mediana em 10 vídeos, com 3,7 mil inscritos), bem acima da mediana de 28 views dos clones. Interpretação [I]: o canal não é só um bilhete de loteria: a "fórmula geral" (pergunta + lugar dos EUA + 20 min com mapa) entrega ~30 mil por vídeo; o hit é o prêmio.
- **Como usar na decisão [I]:** projetar a nossa versão pelo **piso (~10–30 mil por vídeo)**, não pelas 4,5 mi. Na faixa 10–20% do WTS sem hit (3–6 mil por vídeo) a monetização sai do zero só depois de 1.000 inscritos e 4.000 h. O critério de §3b do playbook (3 vídeos, média ≥ 3 mil em 14 dias ou 1 vídeo ≥ 15 mil) continua adequado.
- **Atenção:** o CWFP tem 5 dias; o 882 mil pode ser o mesmo "bilhete" do WTS (vídeo nº 1/nº 2 que explode, resto cai). Reavaliar em 14 dias.

## 6. Limitações
- Busca por yt-dlp devolve ~30 resultados por consulta; contagens de clones são **pisos**.
- Views/mês de canais com 1 hit superestima (WTS 3,9 mi/mês = 87% de 1 vídeo); para canais antigos é piso (só 100 vídeos).
- Classificação por regex + curadoria minha; idiomas em `IDIOMA.md`.
- Não assisti vídeos novos nesta etapa (etapa 2, anatomia, é de outro job: `pesquisa/lugares-guerra/ANATOMIA.md`).
- RPM e receita não foram recalculados aqui (ver `IDIOMA.md` §RPM e `pesquisa/tendencias/2026-11-12-analise.md`).
"""
open(R + "/CONCORRENCIA.md", "w").write(txt)
print(len(txt))
