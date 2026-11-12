# Teste de estilo: lugares-guerra-en (12/11/2026)

Escopo aprovado no brief: até US$ 3; 2–3 frames-chave do piloto no estilo simples (foto/documento real de domínio público com motion leve) + 3 thumbs vibrantes. **Gasto: US$ 0,95** (fal; `financas.consumo` ids 206–209, ref_id 30). Frames = US$ 0 (material público + código).

## Thumbs (base gerada)
| Modelo | Imagens | Custo real | Saída | Avaliação (visão) | Decisão |
|---|---|---|---|---|---|
| `fal-ai/nano-banana` | 3 | US$ 0,119 (0,04/img) | 1344×768 | traço chapado de desenho, pouco detalhe; T2 com o navio em pé (errado) | não |
| `openai/gpt-image-2` (fal, padrão) | 3 | US$ 0,436 (0,145/img) | **1024×768 (4:3)** | ótimo, mas 4:3 | refeito em 16:9 |
| `openai/gpt-image-2` (fal, `image_size 1536x864`) | 3 | US$ 0,391 (0,13/img) | 1536×864 | cutaway vibrante no espírito do WTS, detalhe, ciano e ferrugem corretos, sem texto inventado | **escolhido** |
- Aprendido: o `gpt-image-2` no fal ignora `aspect_ratio`; precisa de `parametros.image_size: {width: 1536, height: 864}` no `canal.yaml` (já gravado). Sugestão para `conhecimento/anti-padroes.md` (geral) no LEVANTAMENTO.
- Grade: `grade-thumbs.jpg` (nano em cima, gpt 4:3 embaixo). Finais com texto: `../amostras/thumb-A/B/C.jpg`.

## Frames (material real + Remotion, render de 8 s na VPS)
| Frame | Material (licença) | Componentes | Avaliação |
|---|---|---|---|
| `frame-DocGrifo.mp4` | NARA RG 38, CINCPAC "Battle of Midway" p. 1, 28/06/1942 (Unrestricted), 4480×5458 | DocGrifo + Número + Ficha | linha (a) legível no zoom 2,3×; grifo lê bem; papel com textura real |
| `frame-EntaoAgora.mp4` | NHHC 1942 (PD, 5717 px) × USFWS 2022 (PD, 3264 px) | EntaoAgora + KenBurns + Ficha | ângulos diferentes (não é o mesmo enquadramento): funciona como "o mesmo prédio", não como sobreposição. Na fase 2, procurar par de mesmo ângulo |
| `frame-MapaKenBurns.mp4` | Natural Earth 50m (PD) + NARA 80-G-451086 (PD, 4500 px) | Mapa2D + Número animado + KenBurns + Ficha | mapa limpo e barato; foto de 1941 aguenta zoom 1,3× |
- Nada de 3D, nada de imagem gerada no corpo. Render: 240 quadros em ~30 s cada na VPS (teste de segundos); o vídeo completo vai para o Runpod.
- Componentes prontos para a fase 2: `estilo/src/Frames.jsx` (Ficha, DocGrifo, EntaoAgora, MapaKenBurns) e `estilo/src/Thumbnail.jsx`; dados do mapa `estilo/scripts/mapa_svg.py`; downloader com licença `estilo/scripts/baixar_commons.py`.
