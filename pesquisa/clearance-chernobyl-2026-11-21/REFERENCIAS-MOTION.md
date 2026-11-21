# Referências de motion: Chernobyl, "as horas finais" (Clearance Required)

Data: 21/11/2026. Fonte: 6 pins do Pinterest enviados pelo Rodrigo. Mídia em `refs/`.
Todos abriram com `curl` direto e User-Agent de navegador (sem WARP). Metadados vieram das meta tags `og:*` e do JSON embutido; vídeo pelo MP4 `v1.pinimg.com/videos/.../720p/...mp4` e, no pin 939865, pelo HLS (`.m3u8`, via ffmpeg).
Quadros: 1 por segundo (4/s no vídeo de 5 s) e grades extras a 10 fps nas transições (`*-detalhe-transicao.jpg`). Cortes medidos com `select=gt(scene,X)`.

**Atenção:** os pins **940006 e 939879 são o mesmo vídeo** (mesmo pin de origem `in.pinterest.com/pin/21532904465384206`, mesmo hash `ebad7e32…`). Baixei uma cópia só (`pin-520799144435940006.mp4`). Na prática são 5 referências.

## Tabela-resumo

| Pin | O que é | Tipo / duração | Fonte original | Lição principal | Serve para Chernobyl? |
|---|---|---|---|---|---|
| 940006 (= 939879) | "Vintage Documentary Slideshow" (template After Effects) | vídeo 1280×720, 24 fps, 31,0 s, 4 cenas | VideoHive item 50333064 (pinado por `jthemesco`) | colagem de fotos/papéis sobre fundo escuro, com fita adesiva, Polaroid, filme 35 mm e data datilografada | **Muito** (dossiê de documentos e fotos de época) |
| 939887 | "Corporate Timeline History" (template AE, autor `byungchan`) | vídeo 960×540, 29,97 fps, 60,0 s, ~13 blocos de ~4,3 s | VideoHive item 23191838 | linha do tempo de ano + etiqueta, entrada por **blocos de pixel**, transição por **glitch/VHS** com aberração cromática | **Muito** (cronologia das 01:23, glitch de sinal) |
| 939890 | "The Slideshow, Religion and Documentary" (template AE) | vídeo 960×540, 29,97 fps, 87,3 s, ~13 slides de ~6 s | VideoHive item 22699101 (pinado por Frank White) | foto emoldurada por **fumaça/nuvem** que abre e fecha; mosaico de quadradinhos flutuando; citação + etiqueta vermelha de fonte | **Parcial** (fumaça vira vapor/fumaça do reator; citação vira depoimento) |
| 939865 | "The mystery of time": mapa antigo amassado com papel e "?" vermelho | vídeo vertical 720×1280, 24 fps, 5,2 s, 0 cortes | upload de usuário (`kresensuki`) | um único plano com **dolly lento** + luz quente rasante; papel de mapa com textura | **Médio** (plano de mapa com "?" no hook / mistério) |
| 939924 | Pôster "The Most Dangerous Animal of All" (FX/Hulu) | imagem 736×1073 | upload de usuário (`pur0_play`) | **rosto rasgado ao meio**: metade P&B, metade vermelho chapado com documento manuscrito por trás | **Muito** (thumb e cartão de capítulo "antes/depois") |

---

## 1. Pin 940006 (e 939879): Vintage Documentary Slideshow

- **Origem:** template AE da VideoHive "Vintage Documentary Slideshow" (item 50333064), pin de `jthemesco` (Best Graphic Design Trends). Descrição: "Capture the essence of the past…".
- **Técnico:** 31,0 s, 24 fps, 1280×720. Scene detect com limiar 0,3 e 0,12: **0 cortes secos**. As 4 cenas (0–8 s, 8–15 s, 16–23 s, 23–31 s) trocam por saída e entrada de elementos, sem corte.
- **O que vejo:** fundo de **lousa/papelão preto texturizado** com uma **tira de filme 35 mm** na diagonal. Sobre ele entram fotos P&B sépia em **moldura Polaroid** (borda creme grossa), levemente giradas (±5–10°), presas com **fita crepe** amarelada. Há uma foto de mãos numa **máquina de escrever** (o elemento-assinatura), papel kraft rasgado com nome em serifa slab ("DR. MATTHEW EARNSHAW", "BASIL DODGER") + texto corrido pequeno, e **datas em fonte de máquina de escrever** ("20.4.1985", "13.4.1982") que aparecem letra a letra (aos 19–21 s o "20.4.198" ainda está incompleto). Uma data em **blocos tipo flip/etiqueta de régua** ("20 | OCT | 1985", fundo escuro e números claros).
- **Transição (detalhe a 10 fps, 6,8–8,8 s):** os elementos **saem deslizando em bloco** para a direita/baixo, todos juntos, com easing ease-in (~0,4 s). Fica ~0,3 s só o fundo com o filme; depois a fita entra sozinha e a Polaroid **cai de cima** e "assenta" sob a fita (ease-out com pouco overshoot, ~0,5 s). Cada elemento entra num tempo diferente (stagger de ~3–6 quadros). Dentro da cena há **parallax/zoom lento** (Ken Burns de ~3–5 % por cena).
- **Cor e textura:** quase monocromático (preto, sépia, creme, kraft). Grão leve, papel amassado com sombra suave embaixo das fotos (drop shadow difuso).
- **Ensina:** colagem de dossiê com "objetos físicos" (fita, Polaroid, papel rasgado, filme), texto datilografado, stagger nas entradas e saída em bloco. É exatamente a gramática "documento real" do canal.
- **Componentes Remotion:**
  - `ColagemDossie` — props: `itens: {tipo: 'foto'|'papel'|'recorte', src, x, y, rot, largura, legenda?, fita?: 'topo'|'canto'|null, entraEm}`, `fundo: 'tinta'|'papel'`, `kenBurns: 0.04`, `saida: 'bloco-direita'|'bloco-baixo'`, `staggerQuadros: 4`. Entrada por `spring({damping: 14, mass: 0.6})` com queda de −40 px e rotação final; saída comum com `interpolate` + `Easing.in(Easing.cubic)` em 12 quadros.
  - `FotoPolaroid` — props `src`, `rot`, `legendaManuscrita?`, `sepia: 0–1`, `borda: '#EDE6D6'`; sombra `0 8px 18px rgba(17,20,24,.45)`.
  - `FitaAdesiva` — SVG com borda serrilhada, cor `#EDE6D6` a 80 % com tom ferrugem leve; entra 2 quadros antes da foto.
  - `TextoDatilografado` — props `texto`, `fonte: 'IBM Plex Mono'`, `cps: 18`, `cursor: true`, `somTecla?` (SFX de máquina por letra). Para horários: "26.04.1986 — 01:23:04".
  - `TiraFilme35mm` — elemento decorativo de fundo (SVG com perfurações), deslizando devagar; pode conter 3–4 quadros de footage real.
  - Paleta: fundo `#111418` com textura de papelão, papel `#EDE6D6`, datas em `#FDD505` só no destaque, legendas em ferrugem `#C8561E`.

## 2. Pin 939887: Corporate Timeline History

- **Origem:** VideoHive "Corporate Timeline History", autor `byungchan` (item 23191838). Pin com título "Corporate Timeline History [Video]".
- **Técnico:** 60,0 s, 29,97 fps, 960×540. Scene detect a 0,3: 6 picos (todos dentro das transições glitch aos 28,5 s, 41,5 s, 54,5 s); a 0,12: picos em 2,6; 11,1; 15,4; 24,2; 28,4; 37,1; 41,4; 50,1; 54,4 s. Ritmo: **um bloco a cada ~4,3 s** (cartela de abertura 0–2,6 s, 12 anos de 2008 a 2019, logo envato no fim).
- **O que vejo:** fundo **escuro com vinheta ferrugem/vermelho-tijolo** (gradiente quente que vem de um canto), linhas finas de **grade/cruz de mira** (linha vertical e horizontal finas que cruzam o quadro) e **blocos de texto miúdo** desfocados como "documento" ao fundo. No centro, retrato P&B recortado em retângulo; ao lado, **ano grande em serifa** ("2008", "2010"…) e uma **etiqueta vermelha** com palavra em caixa alta sem serifa ("EMOTIONAL", "UNIVERSAL") + subtítulo minúsculo. Brilho de lens flare pontual perto da etiqueta.
- **Transição (detalhe a 10 fps, 10,4–12,4 s):** a etiqueta e o ano **tremem e se duplicam** (0,3–0,4 s), depois a imagem inteira vira **glitch horizontal**: rasgos de linha, deslocamento RGB (vermelho/azul separados), borrão de movimento lateral (0,5–1,0 s), ~0,3 s de **ruído escuro** quase vazio, e a nova foto **se monta por blocos de pixel** (quadrados que aparecem em posições aleatórias e se juntam, ~0,5 s) antes de estabilizar. Total ~1,5 s. Em 3 transições o glitch é mais forte (faixas verticais coloridas, 28 s/41 s/54 s).
- **Ensina:** cronologia legível (ano grande + rótulo curto + foto); glitch como "sinal falhando"; montagem por blocos (pixel assembly); fundo com camadas de documento desfocado e grade fina dão profundidade sem 3D.
- **Componentes Remotion:**
  - `TransicaoGlitchSinal` — props `duracao: 36` quadros, `intensidade: 0–1`, `corA: '#2BCEE2'`, `corB: '#C8561E'` (substitui o RGB vermelho/azul), `ruido: true`. Implementação: 2–3 cópias da cena com `translateX` por faixas (clip-path de N faixas horizontais com deslocamento por `random(seed+frame)`), `mix-blend-mode: screen`, + quadro de ruído (canvas/noise). Ideal para "o sinal cai" e para cortes entre horários.
  - `MontagemBlocos` (pixel assembly) — props `src`, `grade: 16×9`, `duracao: 15`, `seed`. Cada célula aparece com opacidade 0→1 em atraso aleatório; células com leve deslocamento. Serve para entrada de foto de arquivo "sendo recuperada".
  - `MarcoCronologia` — props `ano|hora` (ex.: "01:23:40"), `rotulo` ("AZ-5 PRESSED"), `subtitulo`, `foto`, `lado: 'esq'|'dir'`. Hora em **Anton** grande `#EDE6D6`; rótulo em **Barlow Condensed** caixa alta sobre tarja `#C8561E` (ou `#FDD505` com texto `#111418` no momento crítico); subtítulo em IBM Plex Mono 14 px.
  - `FundoArquivoGrade` — fundo `#111418` com vinheta ferrugem num canto (radial `#C8561E` a 25 %), linhas de mira finas ciano `#2BCEE2` a 20 %, blocos de texto de documento desfocados (blur 3 px) se movendo devagar. Fundo padrão de capítulo.

## 3. Pin 939890: The Slideshow, Religion and Documentary

- **Origem:** VideoHive "The Slideshow | Religion and Documentary" (item 22699101), pinado por Frank White; repinado por Rodrigo Junior. Título SEO: "American revolution slideshow [Video]".
- **Técnico:** 87,3 s, 29,97 fps, 960×540. **0 cortes** detectados (limiar 0,3 e 0,12): tudo é dissolvido por fumaça. ~13 slides de ~5–6 s + cartela final "GOD IS LOVE" (75–87 s).
- **O que vejo:** cada foto aparece **dentro de um buraco de nuvem/fumaça** branca e escura; as bordas da fumaça se mexem o tempo todo. Por cima, **quadradinhos semitransparentes** com recortes da própria foto flutuam (efeito mosaico). Texto de citação em serifa branca, centralizado em 3–5 linhas, e logo abaixo uma **mini-etiqueta vermelha** com a referência ("Matthew 5:7"). Fotos com color grading suave e dessaturado.
- **Transição (detalhe a 10 fps, 18,4–20,4 s):** a fumaça **avança e cobre** o quadro (~0,5 s), a foto nova aparece em **dissolve cruzado através da fumaça** (as duas visíveis por ~0,4 s, texto antigo e novo sobrepostos) e a fumaça recua. Total ~1,2 s, easing suave (ease-in-out), sem nenhum corte seco.
- **Ensina:** fumaça como máscara e transição orgânica; citação + etiqueta de fonte (atribuição visível); ritmo lento e contemplativo. O estilo religioso/"nuvem do céu" **não** serve; a mecânica sim.
- **Componentes Remotion:**
  - `TransicaoFumaca` — props `video: 'fumaca-alpha.webm'` (stock de fumaça com alpha ou luma matte, sem IA), `duracao: 36`, `tom: 'escuro'|'claro'`. Usa o vídeo de fumaça como máscara de luminância entre cena A e B. Em Chernobyl: vapor/fumaça preta do reator, tingida `#111418`/cinza, nunca branca de "céu".
  - `CitacaoDepoimento` — props `texto`, `quem` ("Anatoly Dyatlov, deputy chief engineer"), `fonteDoc` ("Trial transcript, 1987"), `entrada: 'linha-a-linha'`. Texto em Barlow Condensed/IBM Plex Mono `#EDE6D6`; etiqueta da fonte em tarja `#C8561E` pequena (como a referência bíblica vermelha). Serve para falas reais de operadores e relatórios.
  - `MosaicoFlutuante` (opcional) — quadradinhos recortados da foto de fundo flutuando com opacidade 30–60 %; dá profundidade 2D. Prioridade baixa.

## 4. Pin 939865: "The mystery of time" (mapa com "?")

- **Origem:** upload do usuário `kresensuki` (sem link externo). Título do pin: "The mystery of time | Mystery aesthetic, God illustrations, Video". Descrição automática: "An old, crumpled map with a red question mark on top of it… laid out on a wooden surface".
- **Técnico:** 5,2 s, 24 fps, **vertical** 720×1280, um único plano (0 cortes). Melhor rendição do HLS = 720×1280. Aparência de vídeo gerado por IA ou render; não é material de época.
- **O que vejo:** mapa antigo (papel amarelado, linhas de costa e relevo a traço) sobre mesa de madeira, com um papel retangular por cima e um **"?" vermelho-sangue pincelado**. Câmera em **dolly/push-in lento e levemente lateral** (o papel cresce e desce no quadro ao longo dos 5 s), luz quente rasante que muda o reflexo do papel. Sem texto, sem tipografia.
- **Ensina:** movimento de câmera contínuo e lento num objeto físico já basta para um plano de hook; luz rasante e textura de papel vendem "documento". Como o canal proíbe 3D e mapa em relevo, a lição é **aplicar o mesmo push-in a um mapa real escaneado (2D)**.
- **Componentes Remotion:**
  - `MapaUsinaZoom` — props `mapa: 'mapa-pripyat-1986.jpg'` (mapa/planta real escaneada, domínio público ou com crédito), `de: {x,y,escala}`, `para: {x,y,escala}`, `duracao`, `marcadores: [{x,y,rotulo,entraEm,cor}]`, `luzRasante: true`. Push-in 2D com `interpolate` e `Easing.inOut(Easing.sin)`; sobreposição de gradiente quente simulando luz; marcadores desenhados à mão (círculo traçado com `strokeDashoffset`, `#C8561E`), rótulos em IBM Plex Mono. Usos: Reator 4, Pripyat a 3 km, zona de 10/30 km (círculos crescendo).
  - `MarcaInterrogacao`/`AnotacaoPincel` — SVG de traço de pincel que se desenha (stroke animation), `#C8561E`; para o hook ("o que aconteceu às 01:23?").
  - Para Shorts: a mesma cena em 1080×1920.

## 5. Pin 939924: pôster "The Most Dangerous Animal of All"

- **Origem:** upload de `pur0_play`; é o pôster oficial da série documental da FX/Hulu (2020). Imagem 736×1073 (a original do pin; `originals/` devolveu o mesmo tamanho).
- **O que vejo:** dois retratos (o homem hoje, à esquerda, P&B dessaturado; o suposto pai, à direita) unidos por um **rasgo de papel vertical** irregular com fibra branca aparente. A metade direita é **vermelho chapado** (duotone vermelho/preto) com **cifra manuscrita e letras do Zodíaco** em textura por trás. Tipografia: tagline condensada em caixa alta espaçada no topo ("SEARCHING FOR MY FATHER AND FINDING THE ZODIAC KILLER."), título em fonte "de máquina/estêncil" com o O virado em mira. Grão e textura de papel na imagem toda.
- **Ensina:** **dualidade numa imagem só** (antes/depois, homem/sistema), rasgo de papel como transição e moldura, duotone de uma cor forte + P&B, documento manuscrito como textura de fundo. Fala direto com a thumb e com cartões de capítulo.
- **Componentes Remotion:**
  - `RetratoRasgado` — props `esquerda: {src, tratamento: 'pb'}`, `direita: {src, tratamento: 'duotone', cor: '#C8561E'|'#2BCEE2'}`, `texturaDoc?: 'log-turno.jpg'`, `animarRasgo: true`. Rasgo = SVG de borda irregular com fibra `#EDE6D6`; animação: o rasgo "abre" de cima para baixo (clip-path por path, ~20 quadros) e as metades se afastam 6–10 px. Usos: Akimov × Dyatlov; "a sala de controle antes × depois"; thumb.
  - `DuotoneArquivo` — filtro (SVG `feColorMatrix`/`feComponentTransfer`) para levar foto de época a duotone `#111418`/`#C8561E` ou `#111418`/`#2BCEE2`, com grão.
  - `TaglineEspacada` — Barlow Condensed caixa alta, `letterSpacing: 0.18em`, palavras de destaque em `#FDD505`.

---

## Componentes consolidados (priorizados)

Escala de esforço: P = até 2 h, M = meio dia, G = 1 dia ou mais (inclui testar no Remotion e gerar still de conferência).

| Prioridade | Componente | Vem de | Uso em Chernobyl | Esforço |
|---|---|---|---|---|
| P1 | `RelogioContagem` (cronômetro em tela; não há na referência, é pedido do vídeo) | — (gramática do 939887: Anton + tarja) | "01:23:04 → 01:23:44" sempre visível; dígitos em Anton/Plex Mono `#FDD505` em caixa `#111418`; troca de dígito com flip curto (6 quadros) ou só corte seco com SFX de tique | M |
| P1 | `MarcoCronologia` | 939887 | cada evento da noite: hora + rótulo ("AZ-5") + foto/documento | P |
| P1 | `ColagemDossie` (+ `FotoPolaroid`, `FitaAdesiva`) | 940006 | fotos de operadores, páginas do log, relatórios do INSAG sobre fundo tinta | G |
| P1 | `TextoDatilografado` | 940006 | datas, horários, trechos do log de turno, com SFX de máquina | P |
| P1 | `TransicaoGlitchSinal` | 939887 | virada de capítulo; momento da explosão; "o sinal cai" | M |
| P1 | `MapaUsinaZoom` | 939865 | planta da usina, Pripyat, zonas de exclusão; push-in 2D em mapa escaneado | M |
| P2 | `RetratoRasgado` + `DuotoneArquivo` | 939924 | Akimov × Dyatlov, antes × depois; thumb e cartão de capítulo | M |
| P2 | `FundoArquivoGrade` | 939887 | fundo padrão das cartelas (tinta + vinheta ferrugem + mira ciano) | P |
| P2 | `MontagemBlocos` | 939887 | entrada de foto/footage de arquivo "recuperada" | P |
| P2 | `CitacaoDepoimento` | 939890 | falas reais (julgamento, entrevistas) com tarja de fonte | P |
| P2 | `PainelMedidores` (painel de controle; não há na referência, é pedido do vídeo) | — (linhas de mira e etiquetas do 939887) | potência do reator (MW) caindo e disparando; 2D plano, ponteiros/barras em ciano, alarme em amarelo/ferrugem; números de fonte com crédito | G |
| P3 | `TransicaoFumaca` | 939890 | fumaça do reator entre cenas (precisa de stock de fumaça com alpha) | M |
| P3 | `TiraFilme35mm` | 940006 | footage de época passando dentro da tira | P |
| P3 | `AnotacaoPincel` / `MarcaInterrogacao` | 939865 | hook e pontos de pergunta | P |
| P3 | `MosaicoFlutuante` | 939890 | profundidade 2D em cartelas longas | P |

**Ordem sugerida de construção:** `FundoArquivoGrade` → `RelogioContagem` → `MarcoCronologia` → `TextoDatilografado` → `TransicaoGlitchSinal` → `MapaUsinaZoom` → `ColagemDossie`. Esses 7 já cobrem o esqueleto "as horas finais" (relógio sempre presente, eventos marcados, documentos e mapa).

**Notas gerais:**
- Nenhuma referência tem 3D real nem mapa satélite: tudo é 2D em camadas, compatível com as regras do canal.
- As 3 referências da VideoHive são **templates pagos**: copiar a mecânica é ok; não usar arquivos, fotos nem layout literal deles. As fotos dos templates são banco de imagem genérico; no nosso vídeo, só foto/filme/documento real com crédito.
- Ritmo das referências: 4–8 s por bloco, transições de 1,2–1,5 s. Para YouTube documental de 10+ min isso é lento demais para manter o tempo todo: usar como ritmo de "respiro" entre trechos mais rápidos (2–4 s por plano).
- Transições das referências não usam corte seco; para o relógio de Chernobyl, o **corte seco com SFX** no minuto crítico contrasta melhor com essas transições suaves (Hipótese, sem dado).
