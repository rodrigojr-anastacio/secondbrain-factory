# Visual (em-relevo)

**Diretriz do Rodrigo (06/11/2026, prevalece):** dinâmico, **câmera sempre em movimento**, nada de vídeo estático só com imagem; transição = movimento de câmera; algo novo entra a cada 2–3 s (`pesquisa/estilo-mapa-relevo-3d/PADRAO.md`, referência @relevo.ia).
**Diretriz do Rodrigo (10/11/2026):** o mapa chapado (bege/cinza liso, extrusão simples) é "feio e cansativo de olhar por 12 min"; quer **relevo real/satélite bonito** e **fotos reais grandes** (`~/workspace/referencias/BRIEF-relevo-002-visual-fase1.md`; aprovado na fase 2, `BRIEF-relevo-002-visual-fase2.md`). Repetido como regra nos briefs do 003–005 ("mapa chapado é feio. Mapa 3D conduz, foto real dá realidade", `BRIEF-lote-relevo-003-seca-1877.md`, 13/11/2026).
**Sem IA de cena** (briefs do 003–005): tudo vem de dado real, foto licenciada ou peça desenhada em código.

## Mapa 3D (a base do vídeo)
- **Terreno real** deslocado por altura (NOAA ETOPO 2022 com batimetria; regional: SRTM/GMTED via AWS Terrain Tiles z10, ~130 m), cor NASA Blue Marble (GIBS), limites IBGE/Natural Earth (`../videos/002-el-nino-2026/visual-v2/PROPOSTA.md`; `../videos/005.../shared/baixa_relevo_rs.py`; `FONTES-E-LICENCAS.md` do 005).
- **Mistura A/B aprovada pelo Rodrigo (10/11/2026; `BRIEF-relevo-002-visual-fase2.md`):**
  - **A, satélite real:** "mundo real": Pacífico/globo, aberturas de capítulo, natureza (floresta, rios, mar), impacto.
  - **B, relevo editorial** (relevo sombreado nas cores do canal, ~28% da cor real, mar navy com batimetria): dado/explicação, regiões, contadores, setas, onde rótulo e número precisam de contraste.
  - Troca A↔B só no corte de câmera ou crossfade de 1,6–1,8 s com câmera parada; nunca piscando no meio de movimento; não mais que 1 troca a cada ~20 s. Decisão por cena em `shared/estilo_v2.json` e no `STORYBOARD.md`.
  - O estilo C (pergaminho) foi descartado: parece mapa antigo, destoa de canal de clima de hoje (`PROPOSTA.md`).
- **Foco por vinheta:** região de interesse acesa, resto escurecido; UFs tingidas, "acende Andes" como brilho na crista do relevo real (QA-visual-v2 do 002).
- **Árvore de rios real do OSM** (005, 15/11/2026): rede hidrográfica da bacia ligada nó a nó, subindo da foz (BFS contra a corrente), 5 rios principais grossos, cresce das nascentes à foz (`../videos/005.../shared/prepara_rios.py` → `shared/rios.json`; OSM ODbL). É a assinatura aprovada no crivo do 005; reutilizar em toda pauta de bacia/enchente. Rios do mapa são aproximados (dizer na descrição).
- **Dado real em 3D:** relevo de calor do Pacífico (NOAA OISST), montanhas Niño 3.4, régua/cilindros de cheia (ANA HidroWeb via `shared/baixa_ana.py`), globo, anel de meses (002–005).

## Fotos reais grandes
- A foto entra em **1240 px (65% da largura)** em quadro 16:9 com Ken Burns lento sobre o mapa escurecido, ou duas lado a lado com 860 px; legenda em faixa coral (`visual-v2/PROPOSTA.md`, aprovado 10/11/2026). Polaroid pequena (560 px) saiu.
- **Na tela só lugar e data/ano** (ex.: "CENTRO HISTÓRICO · 5 MAI 2024"); foto de outro ano sempre com o ano real na legenda (`../videos/004-el-nino-1983/pesquisa/CHECAGEM.md`).
- Foto pequena demais (retirantes de 1878, 221–400 px) entra como carte pequena, sem zoom (`../videos/003-seca-1877/ETAPA2-PRONTA.md`).
- **Ideia aprovada a discutir (Rodrigo gostou, 10/11/2026; `pesquisa/canal-clima-2026-11/IDEIAS-A-DISCUTIR.md`):** foto/vídeo real esmaecido no fundo com animação por cima; cartão de lugar quando o mapa pousa; B-roll de banco livre (risco de "conteúdo repetitivo" se virar base). **Hipótese.**

## Peças 2D (React por cima do 3D)
Legenda palavra a palavra em máquina de escrever, número/contador no topo com faixa navy, aba de capítulo, pinos com bounce e fio vermelho, manchete como recorte de papel (`PADRAO.md`); gráficos e esquemas do vídeo em `Novos*.jsx`: régua de chuva, hidrograma, antes × depois Landsat com cortina, tela partida por UF, maquete da orla, corte do sistema, perfil serra → capital, calendário de picos, papel de arquivo (003–005, `ETAPA2-PRONTA.md` de cada um). **Esquema fora de escala leva "ilustrativo" na tela** (005). Fecho útil em quadro de cortiça "O QUE FAZER" (001, 002).
Fontes: Anton (números, títulos), IBM Plex Mono (faixas, legenda), Playfair Display Italic (manchetes) (`identidade/fontes/`). Ícones em SVG (as fontes não têm ✓ ✗ ▶ □ ⚠ ◀; 001).
Áudio: trilha Kevin MacLeod (CC BY 4.0) com ducking; SFX pedidos pelo Rodrigo (08/11/2026): pino = toc seco de madeira (sem bip), número = tum abafado baixo, whoosh/papel nas transições (`shared/mix_audio.py`). Pixabay bloqueia download automatizado (001).

## Fontes de imagem permitidas
- **Sim:** Landsat/USGS (há 1983, MSS), Sentinel-2/HLS (NASA Worldview/GIBS), NOAA (OISST, GOES), NASA (Blue Marble, GIBS; **GPM/IMERG no GES DISC** com o token em `~/.segredos/nasa/earthdata.env`, desde 16/11/2026, nunca leia/imprima), INMET, ANA, IBGE, OSM (ODbL), Wikimedia Commons **com licença conferida por arquivo**, arquivos públicos com licença clara (briefs 004/005).
- **Nunca:** imagem da Globo/TV/emissora (os hits de busca são Record/Band/RBS; nenhuma licença livre) (`BRIEF-lote-relevo-004/005`; `../videos/004.../pesquisa/FOTOS.md`); foto de vítima em close/cadáver (`conhecimento/politicas-youtube.md`).
- **Decisão de risco do Rodrigo, pendente:** série PMPA no Commons com template "Attribution only" (não é CC; exige crédito ao autor/PMPA). Usada no 005 com crédito na descrição; alternativa Stuckert (CC BY-SA 2.0)/satélite (`../videos/005.../FONTES-E-LICENCAS.md`).
- Trechos de vídeo de terceiros: o 001 usou 33 trechos de redes/portais sem autorização (pedido do Rodrigo em 08/11/2026, divergindo do RELATORIO do canal, que recomendava autorização por escrito); do 003 em diante os briefs pedem só imagem com licença. **Sem trecho de terceiro sem licença** até o Rodrigo decidir o contrário.
- Cada vídeo tem `FONTES-E-LICENCAS.md` (arquivo → legenda na tela → autor → licença → URL), gerado por `shared/gera_pacote.py`/`gera_licencas.py`.

**Crédito só na descrição, nunca na tela** (Rodrigo, 13/11/2026; briefs do 003 em diante: "Créditos só na descrição, nada na tela"; confirmado em 16/11/2026, `BRIEF-em-relevo-padrao.md`). O 001 e o 002 tinham crédito na foto e rodapé "MAPA: NASA BLUE MARBLE · RELEVO: NOAA ETOPO 2022…": não repetir. Créditos completos de foto, mapa (NASA, NOAA, IBGE, OSM), música e SFX no `youtube.txt`.

## Pipeline Remotion (como o 004/005 são montados)
Copiar o vídeo anterior **sem `node_modules`** e linkar: `remotion/node_modules -> ../../002-el-nino-2026/remotion/node_modules` (003–005 assim). Node em `$HOME/.hermes/tools/node-26.12.1-linux-x64/bin`. `remotion.config.js`: OpenGL `swangle`, JPEG 92.
- `shared/roteiro.py` → `blocos.json` (`fala` limpa + `fala_tts` com tags); `storyboard.py` → `storyboard.json`/`cenas.json`.
- `gera_voz_eleven.py` → `audio/eleven-brutos/`; `monta_audio_v2.py` (atempo + Whisper por bloco → `tempos.json`, `work/confere_voz_eleven.txt`); `alinha.py` (palavras → `whisper.json`). Ver `voz.md`.
- `build_cues.py` → `cues.json`: **tudo amarrado à palavra falada**, não a segundos fixos (trocar a voz do 001 custou só ~10 âncoras; `../videos/001-tornados-sul/RELATORIO.md`).
- 3D: `cena3d_v2.js` + `terreno_v2.js` + `camadas.js`; texturas e alturas em `remotion/public/v2/` (`A_/B_/C_<regiao>.jpg`, `alt_<regiao>.png`, de `gera_texturas*.py`; regional: `baixa_relevo_rs.py`); malha reduzida (`perf: {seg: 0.3, segLargo: 0.12}`) porque vértices custam caro no SwiftShader.
- `remotion/src/`: `LongoV5.jsx` (composição `LongoV5`, `estilo: 'AB'`, `fotos: 'grande'`), `Novos*.jsx` (peças do vídeo), `Thumb.jsx` (`ThumbA/B/C`).
- Conferência: `still.sh`/`rebundle_e_stills.sh` → `grade.py`/`folha.py`; pré-QA `tools/preqa_visual.py` (~US$ 0,23–0,34 por rodada); `mix_audio.py`, `sintetiza_sfx.py`, `gera_srt.py`, `gera_pacote.py`, `thumbs.sh`; `tools/qa.sh`, `tools/whisper_final.py`.
- **Render só no Runpod** (`tools/render_runpod.sh`, em partes ≤ 10 min por comando, conferência SSIM contra stills da VPS; 003: 19.347 quadros, ~US$ 0,14; 005: 6 partes, ~US$ 0,39). Na VPS o 001 levou 2 h 48 e o 002 v2 ~10,7 h.
- Nada em `/tmp` (tmpfs): `TMPDIR=$HOME/cache/tmp`.

## Armadilhas já vistas (001–005)
| Armadilha | Como evitar | Origem |
|---|---|---|
| Seta 3D grossa atravessa a câmera no close; nuvem da supercélula no chão | cada seta com `t2` antes do próximo close; stills de toda cena 3D nova | 001 `QA.md`, `RELATORIO.md` |
| Ícones ✓ ✗ ▶ □ ⚠ ◀ viram "tofu" | SVG | 001 `QA.md` |
| Placeholder na legenda ("10H3X") | conferir stills de cada legenda | 001 `QA.md` |
| Mapa "vazio" por 2–4 s (ponto fraco do anti-monotonia) | algo novo a cada 2–3 s | 001 `QA.md` pend. 3 |
| Quadro sem 3D (cortiça) renderiza ~6× mais rápido | usar como respiro de render | 001 `RELATORIO.md` |
| Relevo do Peru alto demais; z-fighting (listras no Pacífico); setas atrás do diorama; termômetro sobre a caixa de perguntas; data vazando para a régua; Sul fora do quadro; focos em grade regular | grade de stills de cada cena e overlay; ordem de profundidade definida | 002 `QA.md` |
| **Fundo do canvas aparece como faixa bege** nas cenas de câmera baixa (diorama, globo, régua) ao trocar a paleta: 48 blocos re-renderizados (~8 h perdidas) | fundo do canvas acompanha o estilo; conferir câmera baixa em toda troca de estilo | 002 `QA-visual-v2.md`; `conhecimento/erros-qa.md` 10/11 |
| Textura do Pacífico só até 45°N → faixa escura no topo | baixar até 65°N | 002 `visual-v2/PROPOSTA.md` |
| Barra das 4 perguntas: card ativo encavala o vizinho | largura fixa por card, gap garantido; conferir os 4 estados | 002 `QA-visual-v2.md`, `BRIEF-relevo-002-visual-fase2.md` |
| Régua de montanhas mostra "0,00" no 1º segundo | esconder número < 0,1 | 002 `QA.md` pend. 2 |
| **Textura satélite some sem erro** em RTX 4090 Secure (faixas diagonais, SSIM 0,57) | blocos de 60 s com conferência a cada 10 s (já no `render_runpod.sh`); concorrência 8 | `conhecimento/erros-qa.md` 11/11; 003 `ETAPA2-PRONTA.md` (A4500 em faixas) |
| Pod sem SSH por 16–22 min; timeout do comando de 10 min; 429 do Runpod após muitas tentativas | render em partes; derrubar e trocar GPU (3090/A4000 deram certo) | 003, 004, 005 `ETAPA2-PRONTA.md` |
| Quadro reprova a prova em 2 máquinas mas passa na conferência densa em outra GPU | conferir em outra GPU antes de mexer no código | 005 `ETAPA2-PRONTA.md` |
| Fotos cobertas pelo papel de arquivo; caixas das perguntas cobrindo cartões; foto cobrindo manchete; cartões × legenda | stills + pré-QA em toda sobreposição | 003, 004 `ETAPA2-PRONTA.md` |
| **Cunha preta** em satélite (transposição no 003; Landsat no 004; Sentinel-2/HLS no 005) | recortar a área sem dados | 003, 004, 005 `ETAPA2-PRONTA.md` |
| Landsat antes × depois com brilhos diferentes; listras verticais | estiramento COMUM aos dois (`004/tools/landsat_par.py`); listras são do sensor MSS (1983) | 004 `ETAPA2-PRONTA.md` |
| Globo apontando para a África em vez da China/Pacífico | conferir a orientação da câmera do globo | 003 `ETAPA2-PRONTA.md` |
| Número na tela antes de a narração dizê-lo (mortos) | gatilho na palavra (`build_cues.py`) | 003 `ETAPA2-PRONTA.md` |
| Texto cortado ("7 campos"); rótulos encavalados no gráfico de chuva, hidrograma e barras; cilindro da régua cortado | pré-QA + stills | 003, 004 `ETAPA2-PRONTA.md`; `PREQA-visual.md` |
| Foto com marca d'água de site (1941) | recortar e usar pequena, ou trocar por tipografia | 005 `ETAPA2-PRONTA.md` |
| Nenhuma foto livre de evento antigo (enchentes de 1983 no Sul: só jornal/TV sem licença) | planejar com satélite (Landsat), gráfico e foto de outro ano com o ano na legenda | 004 `pesquisa/FOTOS.md` |
| Licença duvidosa de slide (Unicamp) | conferir na página; na dúvida, tirar | 004 `ETAPA2-PRONTA.md` |
| SFX WAV apagados pela limpeza de disco | recriar com `shared/sintetiza_sfx.py` | 005 `ETAPA2-PRONTA.md` |
| Pré-QA marca como bloqueante a faixa navy atrás de globo/régua e os picos das transições whip/nuvem | é estilo (falso positivo); anotar e seguir, mas conferir o quadro | 003, 004 `ETAPA2-PRONTA.md` |
| Crossfade deixa rótulo/cilindro/pino da cena anterior sobre a foto | conferir quadros de transição | 005 `PREQA-visual.md` (altos restantes) |
