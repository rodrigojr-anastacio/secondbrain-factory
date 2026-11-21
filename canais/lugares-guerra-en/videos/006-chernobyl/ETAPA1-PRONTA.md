# ETAPA 1 PRONTA — 006-chernobyl (21/11/2026, Opus)

**youtube.videos id 55** (status `roteiro`, título = T1). Custo pago da etapa 1: **US$ 0** (yt-dlp via WARP; Data API ~20 unidades; search.list 0; detector US$ 0). Teto do vídeo (etapa 2): **US$ 6**.

## Ângulo (ANGULO.md §8)
O relógio documental de 67 h 36 min 20 s, do botão AZ-5 (01:23:40 de 26/04/1986) ao boletim TASS no Vremya (21:00 de 28/04): cada marca do relógio é um papel ou uma gravação real, e o relógio para no anúncio ao mundo, não na explosão. **Detector de cópia: 3/100** (`SIMILARIDADE.md`). **Crivo de ângulo: APROVADO na r2** (r1 reprovou: ocupação de 2022 sem fonte própria, transições B08→B09 e B13 parecidas com o TheDanocracy, roda-gigante e arco "100 anos" fracos → corrigidos; r2: 50% de anedotas próprias pela régua estrita, meta 40%).

## Embalagem (crivo independente APROVADO na r3; registrada em `youtube.embalagem_variantes`)
| par | título | padrão do título | thumb (padrão) | texto |
|---|---|---|---|---|
| A | Chernobyl Burned for Days Before the World Knew (47) | "<X> Before the World Knew" (Be Smart 4,8×, AVC 3,9×) | `numero-estatistica`: 2 cartões flip amarelos "6" "7" + "HOURS" sobre a sala de controle quase invisível; sem ":" | 67 HOURS |
| B | Why Was Chernobyl's Alarm First Raised in Sweden? (49) | "Why … in Y?" (TheDanocracy ~294×, DW 5,2×) | `mapa-lugar`: Europa vetorial no código, **terra escura**, pluma amarela com contorno até a Suécia ciano, terminando num **sapato** SVG grande sobre Forsmark | ON A SHOE |
| C | The Bus Order Pripyat Wasn't Told About (39) | bíblia D adaptado (CWFP ~88×, History X 59×) | `antes-depois`: roda-gigante de Pripyat dividida 1986 (nova) × hoje (ferrugem); palavra **horizontal** na divisória; selo RESTRICTED | "TEMPORARY" |
- Rodadas do vídeo: **r1** 2/3 (reprovou par A: cabeça "What Happened at Chernobyl" = BBC + 4 da família; "67:36" lido como mm:ss; obrigações vagas); **r2** 2/3 (par A, item 2: "Burned" × "fogo apagado às 05:00" sem obrigação de separar os dois fogos); **r3** 3/3. Antes, na fase de proposta: 3 rodadas (`embalagem/proposta-2026-11-21/`), onde o T3 "Why Were 1,125 Buses…" caiu.
- **Promessa:** entre o botão AZ-5 e o boletim TASS passaram 67 h 36 min; o vídeo roda esse relógio com os papéis e gravações reais de cada hora (despacho dos bombeiros, a ordem das 20:00 e os 1.125 ônibus às 04:00, a rádio de Pripyat "temporária", Forsmark e o sapato emprestado, a CIA no dia 29) e mostra por que a zona "temporária" continua fechada.
- **Onde o roteiro paga (tempos estimados pelo `roteiro.py`):** áudio real do despacho 0:00–0:08 (A1); frase-âncora "Between that button and the moment Moscow told the world, sixty-seven hours and thirty-six minutes went by." **~0:21** (B01b); os dois fogos "The fires on the roof were out by five… graphite core kept burning… American satellite photographed the heat" **~0:29–0:37**; planta C literal "At eight o'clock on Saturday night, the order… The city spent the rest of that night without being told." **~0:40–0:50** + rádio real "временную эвакуацию" (A2); planta B "The first public alarm outside the Soviet Union went off in Sweden, on Monday morning." **~0:56**; frase do título dita literalmente ~1:25 (B02b). C pago em B07 (ordem das 20:00 grifada ~7:21, 1.125 ônibus ~7:46) + A4 (anúncio real, ~40 s) + B08; B pago em B09 (UPI ~9:38, sapato ~10:25) → B10 (Politburo, TASS, **"The clock stops here" ~12:19**); "Burned" pago em B06 (teto 05:00) e B11 (Landsat ~13:06). Fecho volta ao áudio do hook (A6) e à palavra "temporary" (B14, ~15:11).

## O que está pronto
| Arquivo | Conteúdo |
|---|---|
| `BRIEF.md`, `ANGULO.md`, `ref/` (fora do git) | pauta com os desvios aprovados pelo Rodrigo; manada (5 transcrições) e ângulo |
| `EMBALAGEM.md`, `CRIVO.md`, `embalagem/` | pesquisa, r1–r3 do vídeo (+ histórico da proposta), `variantes.json`, buscas do T1 (`t1-r2/`, `t1-r2b/`), `medianas.json` regravado |
| `SCRIPT.md` | roteiro final em inglês, 14 seções, **2.492 palavras** + **6 áudios de época** (~86 s) → **~16:15** estimado. Plantas: "temporary" (B01→B08/B12/B14), "normal" (B06→B07/B14), o satélite de terça (B01→B11) |
| `FATOS.md` / `SOURCES.md` | 42 fatos com trecho literal e status; bloco → fonte, marcação [P]/[M] |
| `SIMILARIDADE.md`, `CRIVO-ANGULO.md`, `roteiro-crivo/` | detector 3/100; crivo de ângulo r1 (reprovado) e r2 (APROVADO) |
| `qa/split_blocos.json` (fora do git), `blocos-voz.json` | 70 blocos de voz; `[[A1]]…[[A6]]` no SCRIPT = áudio de época antes do bloco (`arquivo_antes`); `VOZ_SUBS` em `tools/split_blocos.py` |
| `roteiro.py` → `STORYBOARD.md`, `storyboard.json`, `blocos.json`, `cenas.json` | **224 planos, validação OK**: **foto/vídeo real de época 42,1%** (vídeo de época 31,1%; meta do Rodrigo 40%), material real 72,4%, 0 imagem IA (`cenas.json` = `[]`), 20 docs grifados / 10 citações lidas literalmente, 73 planos de filme, 32 Ken Burns, 17 contadores, 8 mapas, 1 EntaoAgora, 1 Dupla, mural no fecho |
| `midia/` (fora do git, 228 MB) + `midia.csv` + `licencas.md` + `midia/DOCS.md` + `tools/docs_pos.json` | 127 clipes de época (Ukrkinokhronika/Shevchenko 1986, Ukrtelefilm 1982, ABC 28/04, CBS 29/04, Vremya 28/04, Reagan Library), 47 fotos de época, 19 itens de hoje (VOA, Commons, NASA), 23 documentos renderizados (INSAG-7, Wilson 208405/208406 scans, Politburo, FRUS, UPI, lei 791a-XII) com a posição exata dos grifos |

## O que a etapa 2 precisa saber
1. **Base do código:** `src/Amostra.jsx` (componentes da amostra aprovada: Contador, Regua, Mural, Onda/Legendas/Selo, Datilo, Glitch, mapa com pluma) + `src/componentes.jsx`/`Video.jsx`/`tools/build.py` do 005 (KenBurns, Filme, DocGrifo, Dupla, EntaoAgora, Cartela, Número). Tipos novos no `storyboard.json`: `Arquivo`, `Contador` (`de_t`→`ate_t`), `Datilo`, `Teletipo`, `TresRelogios`, `Mural`, `Glitch`; overlay persistente régua + contador por bloco (`relogio` = [hora, `corre|parado|hora|min|seg|dia|oculto`]). `EntaoAgora`/`Dupla` com `arq` = `filme:<arquivo>.mp4@<s>` = still extraído do clipe naquele segundo. Copiar `public/fonts` (já copiado) e os PNG/jpg da amostra se reaproveitar.
2. **Crédito NA TELA** (desvio aprovado): coluna `credito` do `midia.csv` em todo plano de foto/filme/doc com dono (canto inferior esquerdo, Plex Mono 20 px, como na amostra) **e** na descrição. Documentos: créditos em `midia/DOCS.md`.
3. **Áudios de época** (`storyboard.json` → `arquivos`): A1/A3/A6 despacho (Commons), A2/A4 rádio de Pripyat (Commons), A5 TASS **recriado** (voz sintética neutra, filtro de rádio, selo RECONSTRUCTION). **Revisar de ouvido/segunda fonte a transcrição russa do despacho antes de legendar o A3** (pendência da amostra); se "Иванков" não se confirmar, cortar a frase do B07d "Ivankov is one of the towns the fire dispatcher had called that night". Trilha para (silêncio) em 01:23:40 e sob cada áudio de época.
4. **Clipes:** 640×480/960×648/480×324 (TV): escalar com moldura/polaroid do mural (não esticar); normalizar (H.264, GOP curto) e `RFLAGS=--offthreadvideo-cache-size-in-bytes=1000000000` se precisar; o `roteiro.py` marca `vel` < 1 onde o clipe é curto (mín. 0,7×). Logos: VOA (crop ~6%), marcas já cortadas pelo acervo; conferir na contact sheet.
5. **Voz:** Fish "Narrator" (s2.1-pro, por frase). Conferir no Whisper: Pripyat, Bryukhanov, Khodemchuk, Shashenok, Kibenok, Pravik, Masik, Dymer, Ivankov, Forsmark, Chebrikov, Gromyko, Dobrynin, Vremya, INSAG-7, EPS-5, RCPS, germanium.
6. **3 thumbs, uma por conceito** (A = T1, B = T2, C = T3), condições do crivo: A — o "7" lê inteiro a 320×180 (virada ≤ 15%), nada de ":"; B — mapa vetorial no código, terra escura com contraste para a Europa ler como mapa, sapato SVG lendo como sapato a 320×180; C — base nano-banana (roda dividida, "no text"), "TEMPORARY" horizontal no código. Prévia 320×180 de cada (ao lado do selo de duração do YouTube na A).
7. **Content ID:** subir **não listado** primeiro e esperar a checagem de direitos do Studio (áudios do Commons com muitos reuploads; Ukrkinokhronika/Ukrtelefilm/Gosteleradiofond, ABC/CBS, Vremya: risco médio-alto, já com crédito). Anotar no pacote.
8. **Sem gancho de próximo vídeo**; voz sintética declarada; título/descrição/tags sem death/dead/died/killed; nenhuma imagem de vítima/hospital (acervo conferido pelo agente; as mortes estão só na narração, com contexto, sobre cartelas RECORD e paisagem da usina).
9. **Capítulos estimados** (recalcular com a voz): 0:00 The button · 1:05 Still temporary · 1:56 Friday, two in the afternoon · 3:01 Thirty megawatts · 3:59 The line in the table · 5:09 The roof fires · 6:56 Saturday, eight p.m. · 8:03 Sunday, temporarily · 9:38 Monday, Forsmark · 11:00 Monday, nine p.m. · 12:33 Tuesday, Washington · 13:26 The thirty kilometers · 14:16 One more reason · 15:11 Temporary.
10. **QA da promessa** (`legendas.srt`): frase-âncora ≤ 0:45; frase dos dois fogos, frase literal de C ("eight o'clock on Saturday night… without being told") e frase de B (Suécia) ≤ 1:00; nunca "the fire was out" sem "roof"; cada thumb final contra o seu conceito.

## Checklist da bíblia (roteiro.md)
- [x] Hook abre com documento real na tela (INSAG-7, "EPS-5 button was pressed") + número (67:36:20). [~] 4 revelações no 1º minuto (a bíblia pede ≤ 2): exigência do contrato da embalagem (A, os dois fogos, C e B até 1:00); a 3ª coisa estranha guardada é o "unable to establish why" (B05) e os três relógios (B10).
- [x] Pergunta/frase do título dita literalmente antes de 1:45 (~1:25).
- [x] 3 plantas pagas; fecho volta ao áudio do hook e à palavra "temporary".
- [x] ≥ 4 documentos lidos e grifados (20 grifados, 10 citações literais); ≥ 1 então × agora (roda-gigante 1986 × hoje) + Dupla 1986 × 2025; ≥ 3 números (15); ≥ 2 mapas (8).
- [x] Toda afirmação em `SOURCES.md`/`FATOS.md`; material com licença/crédito em `licencas.md` (desvio aprovado: material com dono com crédito na tela).
- [x] Ângulo próprio: SIMILARIDADE 3/100, CRIVO-ANGULO APROVADO (r2), ≥ 40% fora da manada.
- [~] 2.492 palavras (piso 2.600; −108): o vídeo leva ~86 s de áudio de época sem narração → duração estimada 16:15, dentro dos 16–20 min.
- [~] Material real 72,4% (bíblia 85%): a linguagem aprovada da amostra (contador, régua, mapa com pluma, teletipo, cartão, mural) ocupa ~25% por desenho; a meta do Rodrigo para este vídeo (≥ 40% de foto/vídeo de época) está cumprida (42,1%).

## Pendências (menores, contornadas)
- **Transcrição russa do despacho (A3)** a revisar de ouvido/2ª fonte antes de legendar; frase de Ivankov no B07d depende dela (cortar se não confirmar).
- **Hora do Vremya (21:00)** só em fonte jornalística (Lenta/ruwiki/DW); 21:02 sem fonte. Mantido 21:00 (é a hora do programa).
- **Wilson Center:** pede contato para uso comercial (NPIHP@wilsoncenter.org); mostramos o **scan original em russo** (ato oficial, PD-UA-exempt) com legenda nossa; tradução citada em trecho curto.
- **34 fotos do livro "Припять. Фоторозповідь" (Yevsyukov, 1986)**: o Internet Archive marca PD, mas o livro tem autor/editora; entram com crédito na tela (desvio aprovado). Se o Rodrigo preferir, há reservas de filme da Ukrtelefilm 1982 para trocar.
- **Fontes secundárias aceitas:** Pravik/Kibenok (biografias), zona de 30 km "by early May", crianças de Kyiv, grafite queimando "into May", ocupação de 2022 (WNN + BBC). Turistas de 2019 saíram do roteiro (sem fonte oficial).
- O teste A/B de thumbs tem 3 padrões de exploração (o placar do canal ainda não tem vencedora).
