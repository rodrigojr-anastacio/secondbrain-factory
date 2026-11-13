# ETAPA 1 PRONTA — 003-gettysburg (13/11/2026, Opus)

**youtube.videos id 36** (status `roteiro`). Custo da etapa 1: **US$ 0** (só web pública). Teto do vídeo: US$ 6.

## O que está pronto
| Arquivo | Conteúdo |
|---|---|
| `SCRIPT.md` | Roteiro final em inglês nativo, 18 seções, **2.665 palavras** (~15:51 de fala a 168 ppm; vídeo ~16:40 com pausas). 3 títulos, plantas (fuzil, sapatos, 19 de novembro) e onde são pagas. |
| `FATOS.md` / `SOURCES.md` | 43 fatos com trecho literal e status; bloco → fonte. Correções de pauta no fim do FATOS. |
| `qa/split_blocos.json`, `blocos-voz.json` | 76 blocos de voz (≤ 48 palavras). `VOZ_SUBS` vazio (ver pronúncia abaixo). |
| `roteiro.py` → `STORYBOARD.md`, `storyboard.json`, `blocos.json`, `cenas.json` | **179 planos**, validação OK: material real 85,4%, 0 imagem IA no corpo, 8 documentos grifados / 11 citações lidas literalmente, 5 EntaoAgora, 5 mapas, 37 Números. `cenas.json` = `[]`. |
| `midia/` (fora do git, 79 arquivos, ~140 MB) + `midia.csv` + `licencas.md` | Fotos de 1863 (LoC via Commons, até 3840 px), as 4 páginas de texto do Sketch Book (pranchas 36/37/40/41, 4400×3400, do Internet Archive), capturas NARA/LoC/NPS, chapa de Brady (NARA 111-B-4975), foto de Josephine Cobb (NARA 64-NA-1595), retratos de Gardner e Lincoln (8/11/1863), mapa de Ditterline (1863), "hoje" (Highsmith/LoC, Army National Guard 2015, U.S. Navy 2013, NPS Then & Now, CC0). `tools/gera_midia_csv.py` regenera o CSV e as licenças. |
| `THUMBS.md` + `thumbs/cenas.json` | 3 conceitos A/B/C pareados aos títulos, prompts prontos (sem corpo, sem rosto, sem texto). |
| `BRIEF.md` | Resumo do vídeo. |

**Títulos (A/B/C, pareados com as thumbs):** A "The Gettysburg Photos You Weren't Supposed to See" · B "Why Is the Same Dead Soldier in Two Gettysburg Photos?" · C "What Happened to the Real "Harvest of Death"?"

## O que a etapa 2 precisa saber
1. **Sem filme.** Gettysburg 1863 só tem foto. O `roteiro.py` permite KenBurns/Dupla/DocGrifo até 14 s seguidos (os demais tipos 12 s). Rode `python3 roteiro.py` de novo depois do `build.py` (com `qa/tempos.json`) para checar com os tempos reais.
2. **Componente novo `Dupla`** (duas fotos reais lado a lado, rótulo curto embaixo de cada uma, Ficha opcional, `selo` opcional): criar no `src/componentes.jsx` (base: copiar `src/` e `tools/` do 002). 22 planos usam.
3. **Mapas:** `invasao` (Natural Earth, escala regional, como no 002). `campo`, `rose` e `reynolds` usam como **base o mapa de Ditterline de 1863** (`midia/mapa_ditterline_1863.jpg`, campo `arq` do plano): georreferenciar com 3 pontos de controle (cidade, Round Top, Culp's Hill) e animar pontos/linha sobre ele. `toca` é esquema de 2 pontos ("~40 YARDS", Selo SCHEMATIC), sem base cartográfica.
4. **Grifos estimados à vista** (`G` no `roteiro.py`, caixas x,y,l,a): conferir nos stills e ajustar. `bliss_world` está vazio: marcar a linha "The world will little note…" na página do meio da cópia Bliss (`doc_discurso_bliss.jpg`) ou manter só página/zoom (a Cartela QUOTED seguinte mostra a frase).
5. **Lincoln:** posição na chapa inteira `foto_multidao_lincoln_1863.jpg` = (0,418; 0,424), zoom forte 3,2× no B14d. **Não use** `foto_multidao_lincoln_crop.jpg` (o recorte do Commons tem uma seta vermelha moderna).
6. **Fotos de mortos:** sem close de rosto/ferimento (regra do brief). Os `detalhe:` em fotos de mortos são só no fuzil (0,42; 0,52) e no muro (0,33; 0,28) da `foto_toca_gardner_1863.jpg`. O pré-QA deve reprovar qualquer close de rosto.
7. **Reuso 49%** (vídeo só de fotos; a foto do hook volta de propósito no B08/B18). Se o pré-QA achar repetitivo, há reservas no `midia.csv`: `foto_mortos_federais_1jul`, `foto_centro_campo`, `foto_meade_qg`, `foto_john_burns`, `hoje_lrt_2015`, `hoje_lrt_loc`, `mapa_gilbert_1922`, `doc_discurso_nicolay_p1/p2`.
8. **Voz:** Fish "Narrator" (`0327fdb5da9e4fd782899a8058c8ae2b`, s2.1-pro, por frase, como o 002). Conferir no Whisper: Frassanito, O'Sullivan, Lamon, Heiser, Devil's Den, "thirty-six/thirty-seven". Se errar, pôr grafia fonética em `VOZ_SUBS` (`tools/split_blocos.py`).
9. **Sem gancho de próximo vídeo:** o fecho só tem o CTA genérico da bíblia ("If you want the next one, subscribe"), sem tema futuro. Nada a remover.
10. **Créditos só na descrição** (bloco SOURCES & CREDITS a partir do `midia.csv`/`licencas.md`). Josephine Cobb: só a NARA 64-NA-1595; a NAID 12167664 é foto do *New York Times* (fora).
11. **Capítulos estimados** (recalcular com a voz real): 0:00 The photo everyone knows · 0:46 The other plates · 1:46 Three days in July · 2:36 The man who quit Brady · 3:26 Ten seconds of stillness · 4:31 The field by the Rose farm · 5:21 A young man on the slope · 6:15 Forty yards · 7:09 The rifle · 8:05 The words beside the pictures · 8:58 Two armies, one row of dead · 10:01 Why lie? · 10:46 November 19th · 11:40 Find the President · 12:35 Two minutes · 13:24 What's still out there · 14:12 The wall is still there · 15:00 Count the plates.
12. **Para o Rodrigo conferir (candidatos; tempos reais pela legendas.srt):** hook com a foto e o fuzil (B01); as pranchas 40 × 41 lidas lado a lado (B10); "rebels" × "our own men" (B11); o zoom em Lincoln na multidão (B14).

## Checklist da bíblia (roteiro.md)
- [x] Hook com objeto real + tarefa; 2 revelações no 1º minuto.
- [x] Pergunta do título dita literalmente em ~0:58.
- [x] 3 plantas pagas; o fecho volta à foto do hook.
- [x] ≥ 4 documentos lidos e grifados (8); ≥ 1 então × agora (5); ≥ 3 números grandes; ≥ 2 mapas (5).
- [x] Toda afirmação em `SOURCES.md`; material só PD/CC0 (`licencas.md`).
- [x] 2.600–2.900 palavras (2.665); capítulos a montar na descrição.
