# ETAPA 2 · dossie-es 017 El Gulag (23/11/2026)
Voz Fish (64 blocos, US$ 0,18; glossário só na voz em `blocos-voz.json`), 192 imagens (189 + 3 bases de thumb), build 13:49 (258 planos), pré-QA (101 quadros), render Runpod RTX 3090 (US$ 0,15), QA, thumbs A/B/C, pacote e `entrega/` (sem Drive). `youtube.videos` id 64 = `pronto`.
- **Imagens:** Codex sem cota (limite 5 h/semanal já no 1º lote): **0 Codex × 192 Gemini** (`gemini-nano-banana-2.1`, ~US$ 0,049/img, US$ 9,63 total no banco). O 1º comando morreu no timeout com 121 imagens no `.gemini-fallback/` sem registrar custo: movi para `imagens/` e lancei à mão US$ 5,94 em `financas.consumo`; as 71 restantes direto por `img_gemini.py`. I104 com moldura recortada; I038/I102/I128/I144 regeradas (texto inventado). 2 bloqueios de segurança no Gemini (retry sem nome ok).
- **Mapas** (`src/labels.jsx`): pinos de Moscú/Kolimá/Norilsk/Karagandá, Magadán, Norilsk, Krasni Bor e 28 pontos de campos (pino pequeno sem rótulo).
- **Custo total do vídeo:** ≈ US$ 10,4 (Gemini 9,63 + Fish 0,18 + Runpod 0,15 + Anthropic API 0,49 incl. pré-QA) ≤ teto US$ 12.
- **Promessa paga:** 0:22,7 (frase-âncora "Esta es TODA la historia del Gulag…").
- **Lições:** (1) `img_codex.py` com cota esgotada manda tudo ao fallback e, se o comando passar de 10 min, mata o processo sem registrar custo: com Codex sem cota, chame `img_gemini.py` direto em lotes. (2) Render em `nohup … &` com `run_in_background` e laço de espera funcionou (935 s de render).
- Pendências: nomes de ouvido (Iordache, Jlevniuk, Vadillo, Joublanc, Salejard); acento nos rótulos de lugar.
