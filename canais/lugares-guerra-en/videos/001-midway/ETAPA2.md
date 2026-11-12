# ETAPA 2 (voz): 001-midway — 12/11/2026

| Item | Valor |
|---|---|
| Voz | Fish **Narrator** (Max N, `0327fdb5…`), `s2.1-pro`, por frase + 0,32 s (decisão do Rodrigo, 12/11) |
| Blocos | 87 mp3 em `audio/` (fora do git), 15,9 min de áudio bruto |
| Custo | US$ 0,2291 (15.271 bytes × US$ 15/M), `financas.consumo` ref 30. Crédito Fish 46,82093 → 46,59293 = US$ 0,228: **cobrado como s2.1-pro, confirmado** |
| Whisper (`tools/compara_voz.py`, small.en, VAD) | média **98,7%**, mínimo 92,1% (B14d: só "$1.2 million" × "1.2 million dollars", normalização) |
| Regerado | B09c: "Ah-kah-gee, Kaga and Soryu" saiu "Akaga" → vírgula depois de Kaga (US$ 0,001) |

Grafia fonética só na voz (`VOZ_SUBS` no `roteiro.py` → `texto_voz` no `blocos.json` → `blocos-voz.json`): "Four C-V sunk.", "Two C-A sunk.", "line A/C", Ah-kah-gee, "A-F", "I-one sixty-eight", "ten twenty", "thirteen-oh-twenty-two". Tela e .srt usam o texto original.
Falsos alertas do Whisper: B02b/B03a repetiam o bloco (alucinação; durações das frases normais; resolvido com `condition_on_previous_text=False` + VAD); B03a termina com "8 9 10 11" em 0,2 s após o fim da fala (alucinação, não há fala ali). Miniclier → "Minichlear" e Hammann → "Hammond" são grafias do Whisper.
