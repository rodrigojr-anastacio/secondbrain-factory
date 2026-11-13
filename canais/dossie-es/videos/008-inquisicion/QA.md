# QA · dossie-es 008 · La Inquisición (13/11/2026)

**Aprovado.** `tools/qa.sh` + `tools/qa_voz_blocos.py` + pré-QA visual (2 rodadas, 120 quadros, `PREQA-visual.md`) + revisão minha de 8 folhas de contato (186 imagens), stills dos mapas e 3 thumbs.

| Item | Resultado |
|---|---|
| Arquivo | `out/video.mp4` 1920×1080, 30 fps, H.264 + AAC 48 kHz, 856,9 s (**14:17**), 512 MB |
| Render | Runpod em 4 faixas (RTX 3090 / A4500), SSIM 480p mín. 0,993, nº de quadros conferido; 2 tentativas mortas pelo timeout do meu comando (upload lento do bundle) com Pod destruído; US$ 0,28 no total |
| Áudio | −15,3 LUFS, LRA 3,4, pico −4,2 dBFS; 0 silêncios > 1,5 s |
| Telas pretas | 0 · cortes no 1º minuto: 16 (detector) / 21,0 cortes/min (build) |
| Hook | 30,4 s (alvo ≤ 35) |
| Voz (Whisper small, por bloco) | 96 blocos, média **97,9%**, mín. 81,5%. Os 8 abaixo de 93% são grafia: "Gui"→"guy", "Sambenito"→"San Benito", "Cacique"→"casique", Ometochtzin→"Ometoxin", Zumárraga→"su ma raga" (N042), números em algarismo, "IV"/"XVIII". Nenhuma frase faltando, nenhuma tag falada |
| Imagens | 186 (183 + 3 bases) · 0 recusas · moldura/faixa em 47 (25%), recortadas; falsos positivos I123, thumb-C e I160 (vinheta em fundo branco, refeita) |
| Refeitas (10) | I160 (vinheta branca), I011 (barras brancas), I006 hook (multidão de tricórnios do séc. XVIII), I048 (notário de terno), I153 (farda azul moderna + bolsa com cruz vermelha), I157 (soldados séc. XIX), mapas I022/I088/I120 (enquadramento errado, texto "PACIFIC/ATLANTIC" inventado, moldura), thumb-C (cadernos de espiral → livros costurados). I170 recortado à mão (cunha preta) |
| Mapas | `map_europa`, `map_exilio`, `map_atlantico`, `map_sudamerica`: pinos e setas no código, conferidos em stills; Chile/Río de la Plata ajustados após o pré-QA |
| Thumbs | A/B/C 1280×720, 171–189 KB; aba "EXPEDIENTE Nº 008"; sem fogo com gente, capuz pontudo ou texto inventado |

## Para ouvir (Rodrigo; timestamps conferidos na `legendas.srt`)
0:00 hook (Maldonado, Lima) · 1:02 "Gui condena a más de seiscientas" (Whisper ouviu "Guy": confira se o Gui sai /gi/) · 5:07 "Ometochtzin" e 5:12 "Zumárraga" · 7:42 "Zugarramurdi" · 9:17 «Y sin embargo, se mueve» (aspas) · 12:23 "Llorente".

## Observações (ficaram)
- Pré-QA 2ª rodada: 0 bloqueante, 1 alto (pino do Chile, corrigido). Falsos positivos: cena do papa com microfone (João Paulo II, 2000, intencional), galeria vitoriana (museu do séc. XIX), Paris 1817 com prédios um pouco haussmannianos, "1611" num pilar do Salazar (ano correto).
- I108 e I147 (livros abertos) mostram gravuras com soldados de farda do séc. XIX; passam de relance.
- I133 (efígies em varas) tem cabeças enfaixadas; sem capuz pontudo.
