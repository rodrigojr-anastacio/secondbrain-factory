# ETAPA 2 PRONTA — 006-chernobyl (21/11/2026, Sonnet)

**youtube.videos id 55 → `pronto`.** Vídeo **16:37** (997 s), 1920×1080 30 fps, −15,2 LUFS (pico −2,5 dBFS), 0 silêncios > 1,5 s, 12 cortes detectados no 1º min (18 planos; abaixo de 21, como 004/005). Entrega em `entrega/` e no Drive (`Youtube/Clearance Required/006-chernobyl/`: video.mp4, legendas.srt, thumb-A/B/C, thumbnail, pacote/).

**Custo etapa 2 ≈ US$ 1,67** (teto 6): Runpod 0,78 (inclui 2 Pods perdidos: sem IP 0,09; upload do bundle travado 0,44) · Anthropic API pré-QA 0,63 · Fish 0,22 (narração + TASS) · fal 0,04 (1 base).

## Promessa paga (conferido na `out/legendas.srt`)
- Áudio real do despacho 0:00,8; frase-âncora ("Between that button… sixty-seven hours and thirty-six minutes") **0:23,4**; dois fogos ("fires on the roof were out by five… graphite core kept burning") **0:32,1–0:37**; C literal ("At eight o'clock on Saturday night… without being told") **0:42,9–0:48**; B (Suécia, "first public alarm… Sweden") **0:59,9**; frase do título dita ~**1:30**. Ajustei pausas em torno dos áudios de época para a Suécia entrar antes de 1:00.
- Thumbs: A "67 HOURS" (cartões flip, numero-estatistica), B "ON A SHOE" (mapa vetorial, terra escura, Suécia ciano, sapato SVG, mapa-lugar), C "“TEMPORARY”" (roda-gigante 1986 × hoje, base nano-banana, antes-depois). 3 padrões distintos, = conceitos do crivo; A/B/C = T1/T2/T3; pares no banco. QA 6b/6c: SIMILARIDADE 3/100 (roteiro não mudou), CRIVO-ANGULO aprovado r2.

## Voz
Fish Narrator s2.1-pro por frase, 70 blocos, 14,5 min. Whisper média 97,5%, mínimo 88,5% (só números/"Kiev", nomes ucranianos e 2 caudas alucinadas de ≤0,3 s: "thanks for watching", "my name is", sem energia real). TASS: Fish "news reporter" + filtro de rádio, rotulado RECONSTRUCTION.

## Áudios de época (`tools/epoca.py`)
A1–A6 cortados de tel/evac (Commons). Transcrição russa conferida por Whisper multilíngue: **"Алло, Иванков?" confirmado** (frase do B07d mantida); as outras legendas russas do despacho são nossa tradução com reticências onde a ASR é incerta. Trilha muda sob cada áudio, no botão (01:23:40) e no "LOG ENDS".

## Pré-QA e render
275 stills + 12 grades + `PREQA-visual.md` (rodada 1: 2 bloqueantes = rótulos PRIPYAT/CHERNOBYL NPP encavalados no mapa; corrigidos). Corrigidos também: contador cobria texto de documento (contador some nos DocGrifo, página desce 36 px), crédito mais opaco, logo VOA recortado, rótulo/selo do Arquivo abaixo do contador, mural e cartões. Não refeita a rodada automática depois dos ajustes (conferi as grades). Render Runpod em 5 partes (4090/A5000), SSIM ≥ 0,98, 29.912 quadros.

## Pendências / para o Rodrigo
- **Content ID:** subir NÃO LISTADO e esperar (no `checklist-publicacao.txt`).
- Foto de 2016/2025 com o quadrado cinza do scan Bryukhanov é do original; 0:27 de preto no A6 (início do plano escuro) aceito; 12 cortes no 1º min.
- Wilson Center pede contato para uso comercial; "250 FIREMEN · 04:00" mostra fato das 04:00 com relógio em 06:00 (intencional).
- Uso de IA = Sim no Studio. Janela sugerida: dom 22/11 ou seg 23/11.
