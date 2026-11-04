# A/B da narração: hook de teste (vídeo 003, 04/11/2026)

**Por que:** o Rodrigo achou a narração "robótica" (feedback no `BRIEF-historia-003.md`). Antes de gerar o vídeo inteiro, testei 11 tomadas de um mesmo hook de ~60 s (anedota do cavalo de Dario, Heródoto 3.84–87). Voz do canal (clone 48613fc…, Fish s2.1-pro). Custo do experimento: **US$ 0,14** (`financas.consumo`, ref_id 5).
**Como reproduzir:** `tools/.venv/bin/python canais/historia-ptbr/videos/003-ira/amostras-voz/ab.py gerar|medir` (textos e parâmetros no próprio `ab.py`) e `melodia.py <wav>...`. Medidas em `medidas.json`.

## As amostras (ouça nesta ordem: A → G → B)
| Arquivo | Texto | Geração | Parâmetros |
|---|---|---|---|
| `A-atual.wav` | **A** = como o 002 foi escrito (blocos curtos, `[break]` dentro do bloco, 1 tag de tom por bloco) | 1 chamada por bloco; gaps de 0,35/0,9 s do `build.py` | padrão (temp 0,7, top_p 0,7, vel. 1,0) |
| `B-texto-falado.wav`, `B-take2.wav` | **B** = reescrito para a fala: frases curtas, vírgula de respiração, reticências na virada, sem `[break]` | 1 chamada por parágrafo; 0,9 s entre parágrafos | padrão |
| `C-por-frase-silencio.wav`, `C-take2.wav` | B | **1 chamada por frase**, silêncio inserido: 0,32 s entre frases, 0,75 s entre parágrafos | padrão |
| `D-temp-0.9.wav` | B | por parágrafo | temperature 0,9, top_p 0,9 |
| `E-B+pausas-alongadas.wav` | B (mesmo áudio do B) | pós-processo: toda pausa natural ≥ 0,15 s vira ≥ 0,34 s | padrão |
| `F-tags-narrador.wav`, `F-take2.wav` | B + 1 tag livre por parágrafo (`[storyteller voice, intrigued]`, `[low voice, conspiratorial]`, `[amazed]`, `[serious, calm]`) | por parágrafo + pausas alongadas | padrão |
| `G-por-frase+tags.wav` | B + as mesmas tags, só na 1ª frase do parágrafo | **por frase** + silêncio inserido (como C) | padrão |
| `H-tags-vel-0.97.wav` | F | por parágrafo + pausas alongadas | velocidade 0,97 |

## Medidas (Praat/parselmouth + Whisper small)
| Var. | dur. | ppm | pausas ≥ 0,25 s | F0 desvio (st) | F0 faixa p10–p90 (st) | **repetição melódica** ↓ | queda média no fim do trecho (st) | Whisper |
|---|---|---|---|---|---|---|---|---|
| A-atual | 57,6 | 152 | 25 | 3,26 | 8,50 | 0,14 | −2,40 | 96,2% |
| B | 64,0 | 149 | 28 | 3,09 | 8,15 | 0,11 | −1,72 | 95,8% |
| B-take2 | 64,4 | 148 | 30 | 3,25 | 8,74 | 0,10 | −2,09 | 95,8% |
| C | 66,8 | 143 | 32 | 3,34 | 8,63 | 0,12 | −2,10 | 96,5% |
| C-take2 | 66,2 | 144 | 31 | 3,16 | 8,35 | 0,11 | −1,98 | 94,9% |
| D (temp 0,9) | 64,2 | 149 | 31 | 3,10 | 7,74 | 0,10 | −1,87 | 95,2% |
| E | 65,2 | 146 | 34 | 3,09 | 8,14 | 0,14* | −1,72 | 94,6% |
| F | 63,1 | 151 | 31 | 3,54 | 9,04 | 0,16 | −2,60 | 95,8% |
| F-take2 | 65,7 | 145 | 34 | 3,16 | 8,40 | 0,17 | −2,57 | 95,8% |
| **G** | 65,5 | 146 | 32 | 3,18 | 8,42 | **0,09** | −2,06 | 95,2% |
| H (vel. 0,97) | 67,7 | 141 | 33 | 3,38 | 9,02 | 0,19 | −2,96 | 96,5% |

- **Repetição melódica** = correlação média entre os contornos de F0 (normalizados no tempo) dos trechos entre pausas. Alta = toda frase com a mesma "musiquinha" e o mesmo final caindo, que é o que soa robótico. *E sobe por artefato (o alongamento cria mais trechos curtos).
- **Ruído entre tomadas:** B × B-take2 e C × C-take2 variam ~0,15 st no F0 e ~0,01–0,02 na repetição. Diferença menor que isso não é diferença.
- Nenhuma tag foi falada em nenhuma tomada. O Whisper escreve "Irã" às vezes como "Ira"/"Irán" (ambiguidade do Whisper; confira de ouvido).

## O que concluí
1. **O texto pesa mais que o parâmetro.** Reescrever para a fala (B) baixou a repetição melódica (0,14 → 0,10–0,11) e a queda no fim de cada frase (−2,4 → −1,7/−2,1 st) em relação ao texto atual (A), nas duas tomadas.
2. **Tags de "direção" pioram.** `[serious, calm]`, `[low voice…]` e a velocidade 0,97 deixaram as frases mais parecidas entre si (0,16–0,19) e com final mais caído (−2,6/−3,0 st): o tom fica "lido". Use tag só onde a emoção muda de verdade.
3. **temperature/top_p 0,9** não mudou nada além do ruído (e estreitou a faixa de F0). Fica no padrão 0,7.
4. **Gerar por frase com silêncio inserido** dá a menor repetição (G 0,09; C 0,11–0,12), pausa previsível (0,32 s entre frases, sem depender de `[break]`, que o Fish às vezes ignora ou usa para cortar frase curta) e Whisper ≥ 95%. Bônus prático: cache por frase, então o QA regera só a frase ruim.

## Escolha: **G** (texto falado + 1 chamada por frase + silêncio inserido + tag só na virada)
Critério explícito, em ordem: (1) menor repetição melódica sem perder faixa de F0; (2) pausas presentes e controladas (≥ 30 pausas ≥ 0,25 s por minuto de hook); (3) Whisper ≥ 95%; (4) custo igual (mesmos bytes).
Implementado em `tools/tts_fish.py --por-frase` (0,32 s entre frases; frase de 1–2 palavras vai junto com a seguinte; cache em `audio/frases/`). As pausas entre blocos continuam no `build.py` (0,35/0,9/1,5 s).
**Hipótese** (sem dado de retenção): a diferença é real mas pequena na medida; a confirmação é o ouvido do Rodrigo (A × G) e a retenção do 003. Se G ainda soar robótico, o próximo passo é **regravar a referência do clone** (30–60 s de fala natural com pausas, recomendação do guia do Fish), não mexer em parâmetro.

Fontes: docs.fish.audio (API TTS: temperature, top_p, prosody, chunk_length, condition_on_previous_chunks); fish.audio/blog/how-to-use-inline-tags-in-fish-audio-s2; docs.comfy.org/tutorials/partner-nodes/fishaudio/prompt-guide (consultados em 04/11/2026).
