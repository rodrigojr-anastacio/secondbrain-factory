# Teste de motion "mapa em relevo 3D": Remotion × Hyperframes (06/11/2026)

Teste de estilo para o **próximo canal** (padrão em `pesquisa/estilo-mapa-relevo-3d/PADRAO.md`), feito no tema do lotr-fr só para ter conteúdo. **Não é vídeo do canal**: não entra no backlog nem na bíblia.
Brief: `~/workspace/referencias/BRIEF-motion-teste-lotr.md`. Custo pago: **US$ 0** (Kokoro local, nenhuma imagem de IA, fontes OFL).

## Saída (Drive: `Youtube/Le Gardien de Valinor/teste-motion-3d/`)
| Arquivo | O quê |
|---|---|
| `out/teste-remotion.mp4` | 20 s, 1920×1080, 30 fps, 14 MB |
| `out/teste-hyperframes.mp4` | a mesma cena, 22 MB |
| `out/lado-a-lado.mp4` | os dois lado a lado com rótulo e tempo de render |
| `out/frame-remotion.jpg`, `out/frame-hyperframes.jpg` | quadro-chave (14,9 s: Mordor aceso, fio completo) |

## A cena (igual nas duas)
- Roteiro FR (~50 palavras, 18,5 s de fala + 1,5 s de respiro): "Deux mille neuf cents kilomètres. Neuf compagnons. Un seul anneau. Tout commence dans la Comté. Sept cents kilomètres plus loin, à Fondcombe, la Communauté se forme. Puis viennent les ténèbres de la Moria, la lumière de la Lórien… et, au bout de la route, le Mordor. Là où tout doit finir."
- Distâncias **aproximadas** (marcadas com ≈ e na barra de fontes): trajeto de Frodo ≈ 1 800 mi ≈ 2 900 km; Bolsão→Valfenda ≈ 458 mi ≈ 740 km; Moria ≈ 1 250 km e Lórien ≈ 1 400 km são estimativas acumuladas (Fonstad, *The Atlas of Middle-earth*).
- Voz: Kokoro `ff_siwis` 0,92 (canal.yaml), **um único** `audio/narracao.wav` nas duas; palavras alinhadas com faster-whisper (`shared/timestamps.py`).
- Visual: terreno procedural **nosso** (heightmap com ruído próprio; geografia estilizada, não copia mapa oficial nem filmes): folha de papel extrudada sobre mesa kraft, camadas de curva de nível, Monts Brumeux, Ered Nimrais, muralha em U de Mordor com Orodruin, Anduin em sulco, florestas e casinhas de miniatura (instanced). Sol baixo de fim de tarde com sombra real; **luz narrativa** (escurece em "ténèbres", clareia em "lumière", avermelha em Mordor com brasa no Orodruin). Câmera em spline contínua no tempo + deriva (nunca para, zero corte). Pinos caem com bounce, fio vermelho se desenha entre eles (passa "por dentro" da montanha em Moria), regiões acendem (Comté/Lórien rosa, Mordor coral). Camadas 2D: número grande rolando (km) + faixa navy com pop, aba de capítulo, legenda palavra a palavra em máquina de escrever com cursor vermelho e sublinhado nos lugares, etiquetas navy com pop presas aos pinos, rótulos do mapa e barra de fontes fixa.

## Arquitetura (para a comparação ser justa)
- `shared/cena3d.js` (≈400 linhas): o mundo 3D em three.js puro, com `update(t)` determinístico e `projetar()` (posição de tela dos pinos para as etiquetas 2D). **O mesmo arquivo** nas duas ferramentas.
- `shared/camadas.js` (≈60) + `shared/cues.json`: estado das camadas 2D por tempo (número, faixa, capítulo, legenda) e todos os tempos/câmera/pinos.
- `remotion/src/Teste.jsx` (138 linhas): `<ThreeCanvas>` do `@remotion/three` + camadas em React.
- `hyperframes/index.html` (≈140 linhas): `<canvas>` + three.js num `<script type=module>`, camadas em HTML/CSS, pops com GSAP, timeline pausada em `window.__timelines`.
- Resultado: **as duas saídas são praticamente idênticas quadro a quadro** (ver `lado-a-lado.mp4`). A diferença está no pipeline, não no visual.

## Comparativo
| Critério | Remotion (`@remotion/three`) | Hyperframes 0.9.19 |
|---|---|---|
| Qualidade visual vs referência | igual (mesmo mundo 3D) | igual |
| Fidelidade ao PADRAO.md | ~85%: tudo da lista menos polaroid/manchete (sem fotos reais neste tema) e objetos 3D "argila" mais ricos | idem |
| **Render 20 s** (2 vCPU, WebGL por software) | **11 min 00 s** (concurrency 2) | 11 min 49 s com `-w 2`; 13 min 44 s no padrão (1 worker) |
| Custo por quadro | ~1,1 s | ~1,2 s (modo screenshot: o BeginFrame não roda com GL por software) |
| **Projeção 8 min** (×24) | **~4,4 h** (em partes de ≤10 min: `--frames`) | ~4,7 h |
| RAM pico (sistema) | +1,6 GB (3,3 GB total) | +1,1 GB (2,8 GB total) |
| Arquivo 20 s | 14 MB (8,5 Mb/s) | 22 MB |
| Código próprio | 150 linhas + compartilhado | 150 linhas + compartilhado |
| Instalação | 803 MB de node_modules (Remotion + R3F + three) | 45 MB (gsap + three) + 264 MB de Chrome em `~/.cache/hyperframes`; CLI via `npx` |
| Still/prévia para o agente conferir | `remotion still` ≈5 s por quadro | `hyperframes snapshot` ≈40 s para 7 quadros **+ contact sheet pronta** e `lint` que pega erro de GSAP |
| Facilidade para agente | alta: a fábrica já usa (skills `montagem-render`, render em partes, áudio por `<Audio>`/`<Sequence>`, `delayRender`); React é verboso para posicionar camadas | alta para HTML simples; com WebGL é manual (ligar o render do three no `onUpdate` da timeline); pegadinhas do GSAP (`immediateRender`, `set` no tempo 0) — o lint avisou |
| Riscos | render de CPU lento (vale para os dois); `@react-three/fiber` versão casada com o three | projeto jovem (0.9.x, muda rápido); CLI empurra telemetria, "publish" na nuvem e app desktop (rodei com `DO_NOT_TRACK=1`); `init` cria `CLAUDE.md`/`AGENTS.md` mandando instalar skills globais (não instalei); áudio sai com bitrate maior/leve diferença de duração (20,011 s) |

## Recomendação: **Remotion**
1. **Mesmo resultado visual, um pouco mais rápido** (11 min × 11 min 49 s nos 20 s), e já é a ferramenta da fábrica: skills, render em partes, QA e o `build.py` com os tempos reais por bloco servem sem adaptação.
2. O que o Hyperframes faz melhor (snapshot com contact sheet, lint) não compensa trocar de stack; dá para copiar a ideia no nosso QA (`remotion still` em N tempos + montagem de grade com ffmpeg).
3. **O gargalo real é a CPU, não a ferramenta:** ~1,1 s/quadro de WebGL por software → **~4,4 h por vídeo de 8 min** na VPS, ocupando a máquina (um render por vez). Antes da fase 2 do canal novo, testar (Hipóteses, a medir): sombra 1024 em vez de 2048 e terreno com menos vértices (pode cair ~30–50%); render em 1080p só nos trechos 3D e camadas 2D por cima; ou máquina com GPU por hora só para o render.

## Como refazer
```
export PATH=$HOME/.hermes/tools/node-26.12.1-linux-x64/bin:$PATH
# voz + tempos (grátis)
~/tts/venv-kokoro/bin/python shared/gera_voz.py && tools/.venv/bin/python shared/timestamps.py
# Remotion
cd remotion && npm install && ln -f ../audio/narracao.wav public/ && npx remotion render Teste ../out/teste-remotion.mp4 --gl=swangle --concurrency=2
# Hyperframes
cd hyperframes && npm install && ./sync.sh && DO_NOT_TRACK=1 npx hyperframes@0.9.19 render -w 2 -o ../out/teste-hyperframes.mp4
```
(`remotion/public/fonts` e `hyperframes/fonts` recebem hard links de `shared/fonts/`; as fontes .ttf ficam fora do git: Anton, IBM Plex Mono, OFL, baixar do google/fonts.) Medidas brutas em `work/medida-*.txt` (fora do git).
