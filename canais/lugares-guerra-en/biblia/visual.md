# Visual (lugares-guerra-en)

**Diretriz do Rodrigo (12/11/2026, prevalece):** nada de 3D nem "viagem" visual; melhorar um pouco o que as referências fazem, simples e barato: foto/vídeo/documento real em tela com movimento leve, ritmo melhor que slideshow. A pauta nasce do material público livre.
Amostras do estilo: `../amostras/frame-DocGrifo.mp4`, `frame-EntaoAgora.mp4`, `frame-MapaKenBurns.mp4` (código em `../testes/estilo/src/Frames.jsx`).

## Matéria-prima (≥ 85% do tempo de tela)
- **Época:** NARA (fotos 80-G, filmes 428-NPC/342-USAF; conferir "Unrestricted"), NHHC, Internet Archive **só cópias do governo** (FedFlix/gov.archives.*), LoC "No known restrictions", Smithsonian Open Access (CC0), Chronicling America (jornais PD).
- **Hoje:** DVIDS (conferir etiqueta), USFWS, NPS, NASA (ISS/Landsat), USGS, Commons por arquivo (PD/CC0; CC BY só com crédito na tela e na descrição; **CC BY-SA nunca**).
- **Nunca:** Imperial War Museum, Getty/AP Images/Magnum, TV/documentário/filme de terceiros, colorização moderna, Google Earth, cópias Prelinger/Periscope com dono (Content ID).
- Cada vídeo tem `licencas.md` (arquivo → URL oficial → licença → crédito) para disputar Content ID. Regras completas: `pesquisa/lugares-guerra/material/MATERIAL.md` §Regras práticas.
- Critério de pauta: ≥ 1 filme de época PD, ≥ 15 fotos de época ≥ 3.000 px, ≥ 1 documento legível, ≥ 5 imagens atuais livres, ≥ 1 par então × agora.

## Gramática de tela (componentes Remotion reutilizáveis)
| Componente | Uso | Regra |
|---|---|---|
| **KenBurns** | toda foto | zoom 1,04→1,16 ou pan lento; nunca parada > 3 s |
| **Filme** | clipes de 4–8 s de arquivo/DVIDS | sem som original de terceiros; no hook e nas viradas |
| **DocGrifo** | documento escaneado | página inteira 0,5 s → zoom na linha → marca-texto amarelo `rgba(255,225,77,.55)` → a narração lê a linha literal |
| **Ficha** | toda imagem real | caixa escura com barra amarela: linha 1 DATA · LUGAR (mono bold), linha 2 o que é, linha 3 acervo e licença |
| **Número** | 1 por minuto | Anton amarelo, contador animado, unidade em Barlow Condensed |
| **Mapa2D** | 1 por bloco | Natural Earth (PD), terra areia `#D9CBA8`, mar `#0E2A3B`, linha amarela animada, pontos com rótulo; sem relevo |
| **EntaoAgora** | ≥ 1 por vídeo | cortina vertical amarela entre 19xx e hoje, rótulos de data grandes |
| **Selo** | imagem não fotográfica | "SCHEMATIC" / "ILLUSTRATION" / "RECONSTRUCTION" no canto |
- Fontes: Anton (números e thumb), IBM Plex Mono (fichas), Barlow Condensed (rótulos). Cores no `canal.yaml`.
- Trilha: instrumental sóbria (própria/CC0), ducking sob a voz; SFX mínimos (papel, máquina de escrever só no grifo). Nada de sello/stamp de dossiê.
- Imagem gerada: **só a thumb** e, raramente, 1–2 cortes esquemáticos rotulados "SCHEMATIC".

## Render
Remotion 1080p30; render completo no Runpod (`tools/render_runpod.sh`), VPS só stills e testes de segundos.
