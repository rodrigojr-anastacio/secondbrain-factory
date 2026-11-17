# ETAPA 1 PRONTA — 005-tarawa (17/11/2026, Opus)

**youtube.videos id 46** (status `roteiro`, título = T1). Custo pago da etapa 1: **US$ 0** (yt-dlp via WARP; Data API ~125 unidades; search.list 0; detector ~US$ 0 em créditos API). Teto do vídeo (etapa 2): **US$ 4**.

## Ângulo (ANGULO.md)
Os dois lados no mesmo chão: a manada (6 vídeos transcritos) conta os fuzileiros desaparecidos; nós contamos os 4.690 japoneses e coreanos enterrados nas mesmas crateras e o que acontece quando a busca americana os encontra. **Detector de cópia: 1/100** (`SIMILARIDADE.md`). **Crivo de ângulo: APROVADO na r1** (61% de anedotas próprias; meta 40%).

## Embalagem (crivo independente APROVADO na r3; registrada em `youtube.embalagem_variantes`)
| par | título | padrão do título | thumb (padrão) | texto |
|---|---|---|---|---|
| A | Why Is America Digging Up Japanese Soldiers on Tarawa? (54) | Why Is [país] Digging Up X? (controle) | `objeto-simbolo`: duas plaquetas (americana retangular, japonesa oval) enroscadas na mesma camada de areia, em corte, brilho ciano; rótulos pequenos U.S./JAPAN no código | SAME HOLE |
| B | The Soldiers America Wasn't Looking for on Tarawa (49) | The X They Weren't Supposed to Find (D adaptado) | `cena-acao`: vista de cima de escavação, mão com luva e pincel descobrindo capacete japonês Type 90 **sem insígnia**, ≥ 45% do quadro, luz natural (sem ciano), seta vermelha | WHOSE? |
| C | What's Still Under Tarawa Besides the Marines? (46) | What's Still Under X? (padrão B) | `antes-depois`: mesmo trecho de praia de Betio, 1943 (palmeiras partidas, cratera, LVT destruído) × hoje (casas de zinco, varal), cortina amarela; sem pessoas | 1943 · NOW |
- Rodadas: r1 3/6 (reprovou T3 "Half the DNA From Tarawa's Digs Isn't American", Thumb B documento grifado, Thumb C "4,690" sobre a ilha); r2 5/6 (reprovou Thumb B equipe peneirando quintal); r3 6/6. Prompts-base no `EMBALAGEM.md`.
- **Promessa:** sob Betio os dois lados de 1943 estão nas mesmas covas; os papéis oficiais mostram como, e por que a busca americana pelos seus 374 traz japoneses e coreanos (124 de 243 perfis de mtDNA do Tarawa Project são asiáticos), e o que acontece com eles.
- **Onde o roteiro paga (tempos estimados a 168 ppm):** 243/124 no B01a–b (~0:05–0:18); linha do DPMO "buried in bomb craters and existing trenches" lida e grifada no B01c (~0:25); pergunta do T1 ~0:33; Nomura (T2) já no B02 (~0:35–1:20); 374 + "commingled" + "in the thousands" (T3) no B03 (~1:24–2:10); Allen + 4 japoneses no B13 (~9:05); artigo lido no B14 (~9:50); Nomura no B16 (~11:20); Choi no B17 (~12:10); EntaoAgora (thumb C) no B18 (~13:20); números do outro lado reconciliados no B19 (~14:00); fecho volta ao 124 no B20.

## O que está pronto
| Arquivo | Conteúdo |
|---|---|
| `BRIEF.md`, `ANGULO.md`, `ref/` (fora do git) | pauta, manada transcrita, ângulo |
| `EMBALAGEM.md`, `CRIVO.md`, `embalagem/` | pesquisa (PESQUISA.md, refs.csv, mosaicos), r1–r3, `variantes.json` |
| `SCRIPT.md` | roteiro final em inglês, 20 seções, **2.581 palavras** (~15:20 de fala; vídeo ~16:00 com pausas; 19 palavras abaixo do piso da bíblia, aceito pelo crivo de ângulo). 3 plantas: 124 (B01→B14/B20), Unknown X-1 (B09→B10), os 129 coreanos (B05→B17) |
| `FATOS.md` / `SOURCES.md` | 65 fatos + 14 reconferidos (R1–R14) com trecho literal e status; bloco → fonte, marcação [P]/[M] |
| `SIMILARIDADE.md`, `CRIVO-ANGULO.md`, `roteiro-crivo/` | detector 1/100; crivo de ângulo r1 APROVADO |
| `qa/split_blocos.json` (fora do git), `blocos-voz.json` | 71 blocos de voz; `VOZ_SUBS` (Betio → "Bay-sho", Kiribati → "Kiribass", Choi, números grandes, a citação do mtDNA por extenso) em `tools/split_blocos.py` |
| `roteiro.py` → `STORYBOARD.md`, `storyboard.json`, `blocos.json`, `cenas.json` | **216 planos, validação OK**: material real 86,0%, 0 imagem IA, 7 docs grifados / 13 citações lidas literalmente, 10 Cartelas (QUOTED/RECORD), 2 EntaoAgora, 3 mapas (6 planos), 50 números, 19 trechos de filme NARA, 18 Duplas. `cenas.json` = `[]` |
| `midia/` (fora do git, ~115 MB) + `midia.csv` + `licencas.md` + `tools/gera_midia_csv.py` | 26 fotos de época, 17 filmes NARA recortados, 24 fotos atuais DVIDS/Commons, 11 documentos (DPMO p1/p2 renderizados do PDF oficial, Stockman 1947 cap. 5 e Apêndice C, Taylor 2019 p5/p10, DPAA casualties, Across the Reef p46/48/51), 2 mapas de 1943. Folha de contato conferida pelo agente de acervo: sem corpo/ossada |
| `tools/docs_pos.json` | posição exata das frases grifadas nos PDFs (PyMuPDF), usada no `G` do `roteiro.py` |

## O que a etapa 2 precisa saber
1. **3 thumbs, uma por conceito** (A = T1, B = T2, C = T3), prompts no `EMBALAGEM.md`. Nada de ossada/caveira/corpo; capacete e plaquetas **sem insígnia nem letras** (texto e rótulos U.S./JAPAN no código). Prévia 320×180 de cada.
2. **Mapas:** copiar `midia/mapa_base_ne50m_land.geojson` do 004 para `midia/`. Os 3 mapas (`pacifico`, `volta`, `nagasaki`) são em escala oceânica/regional; no `build.py`, conferir `mn` (zoom mínimo) para `pacifico`/`volta` (Betio é um ponto no meio do oceano) e `nagasaki` (Kyushu).
3. **Docs:** todos são páginas reais (PDF oficial do DPMO; páginas web oficiais impressas pelo Chromium: Stockman/HyperWar, Taylor, DPAA). Grifos exatos (não estimados). A página do MHLW (japonês) saiu sem fonte japonesa e foi descartada: as falas do ministério estão em Cartela QUOTED (traduzidas). `doc_taylor2019_*`: artigo de cientistas federais na revista Forensic Anthropology; se houver dúvida de licença no Content ID, trocar por Cartela QUOTED (o texto é o mesmo).
4. **Filmes:** 720×480 (NARA 75861/75866/77026); conferir margens/timecode na contact sheet. Trechos ≤ 7 s por plano (B04d tem 8,6 s: o build corta).
5. **Reuso 55,6%** (fotos de escavação/repatriação voltam; 18 Duplas automáticas quebram sequências de KenBurns > 11 s: `quebra_kenburns()` no `roteiro.py`). Se o pré-QA achar repetitivo, há reservas no `midia.csv`: `foto_locomotivas_trilho_japones`, `foto_placa_to_tokio_hdsn`, `foto_tanque_tipo95_nara64411`, `foto_tanque_japones_palma_dpla`, `foto_esquadrilha_sbd_sobre_atol`, `foto_pby_decola_hawkins_field`, `foto_barcaca_costa_guard_tarawa`, `hoje_repatriacao_embarque_c17_5793635`, `hoje_repatriacao_set2019_5793633`, `doc_across_the_reef_p51_tarawa_hoje`.
6. **`foto_quebra_mar_red_beach3_nara532385.jpg`**: homem deitado sob pano em primeiro plano; **não usar** (não está no storyboard).
7. **Voz:** Fish "Narrator" (s2.1-pro, por frase, como 002–004). Conferir no Whisper: Betio, Kiribati, Tarawa, Sasebo, Shibasaki, Masatoshi/Sadayuki Nomura, Choi Byeong-yeon, Scovill, Roecker, "mtDNA"/"haplogroups", "POW/MIA".
8. **Sem gancho de próximo vídeo**; créditos só na descrição (do `midia.csv`/`licencas.md`); voz sintética declarada; título/descrição/tags sem dead/death/killed/bodies.
9. **Capítulos estimados** (recalcular com a voz): 0:00 Hold on to that number · 0:35 A brother in Nagasaki · 1:24 Anyone can go · 2:13 The island before · 3:03 The men who built it · 3:33 Seventy-six hours · 4:53 Little or nothing · 5:52 Then came the Seabees · 6:34 Unknown X-1 · 7:30 Returned to the Japanese government · 8:21 Three sides, not two · 9:05 Four and one · 9:41 The project for one island · 10:33 How do you tell them apart · 11:23 A brother's sample · 12:16 Tarawa number 46 · 13:18 Then and now · 14:03 What's still under it · 14:45 One hundred twenty-four.
10. **QA da promessa:** na `legendas.srt`, "243"/"124" ≤ 0:30, pergunta do T1 ≤ 0:40, "374" e "commingled" ≤ 2:15, Nomura ≤ 1:30, Allen/Choi nomeados; cada thumb final contra o seu conceito.
11. **Para o Rodrigo conferir (candidatos):** o número do laboratório (B01), a linha do DPMO (B01c), o "little or nothing" de 1947 (B08a), Choi (B17).

## Checklist da bíblia (roteiro.md)
- [x] Hook abre com documento real (artigo do DPAA) + número; 2 revelações no 1º minuto (124/243; a linha do DPMO). A 3ª (os nomes do outro lado em detalhe) depois de 1/3.
- [x] Pergunta do título literal ~0:33.
- [x] 3 plantas pagas; fecho volta ao número do hook.
- [x] ≥ 4 documentos lidos e grifados (7); ≥ 1 então × agora (2); ≥ 3 números (50); ≥ 2 mapas (3).
- [x] Toda afirmação em `SOURCES.md`; material só PD (ver ressalva do Taylor no item 3).
- [x] Ângulo próprio: SIMILARIDADE 1/100, CRIVO-ANGULO APROVADO, ≥ 40% fora da manada.
- [~] 2.581 palavras (piso 2.600; −19).

## Pendências (menores, contornadas)
- População de Betio (~18.400, censo 2020) só via fonte secundária (NSO não abriu): o roteiro diz "about eighteen thousand".
- Choi: data exata/cerimônia da repatriação (dez/2023) não achadas; o roteiro diz só "December 2023".
- Mortos americanos: 990/1.021/1.149 conforme a fonte; o roteiro diz "more than a thousand" e "3,301 Marine casualties" (Apêndice B).
- Lockwood e Scovill vêm do historiador Geoffrey Roecker (Missing Marines): atribuídos na tela ("via G. Roecker").
