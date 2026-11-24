# CTA da HQ "Expedientes Secretos" (Dossier en Minutos) · 24/11/2026

Bloco genérico de **15 s** que entra no meio de todo vídeo novo do Dossier quando existir o arquivo **`ATIVO`** nesta pasta (1ª linha = link da Hotmart). Definições do Rodrigo: `../produtos/hq/DEFINICOES.md`. Quem cria o `ATIVO` é o orquestrador, quando o Rodrigo mandar o link.

## O que tem aqui
| arquivo | o quê | git? |
|---|---|---|
| `cta-hq.mp4` | o bloco pronto (1080p30, 15,0 s, -15,7 LUFS, voz + trilha + SFX do canal) | não (mídia, só na VPS) |
| `cta-hq.wav` | só a voz (Fish "Dio Historias", s2.1-pro, 1,25×, conferida com Whisper: 100% do texto) | não |
| `cta-sfx.wav` | só os SFX (carimbos, folhas, whoosh), para o encaixe num vídeo | não |
| `cta-hq-frames.jpg` | prévia (20 quadros, 1 a cada 0,75 s) | não |
| `cta.json` | duração, texto, linhas de legenda (tempos reais), arquivos, voz | sim |
| `textos.md` | 1ª linha da descrição, comentário fixado e página da Hotmart (espanhol, `{LINK}`) | sim |
| `encaixe.py` | regras do encaixe (ATIVO, posição 35–40%, fusão) usadas pelo `tools/build.py` dos vídeos | sim |
| `pacote_cta.py` | põe a linha da descrição e o comentário no `out/youtube.txt` do vídeo | sim |
| `src/` | Remotion do bloco (`CTA.jsx`; tempos em `src/tempos.json`) | sim |
| `tools/build_cta.py` | áudio (voz, trilha com ducking, SFX), tempos sincronizados com as palavras, links das artes, `cta.json` | sim |
| `tools/render_cta.sh` | render na VPS (~30 s) + prévia | sim |
| `voz/` | entrada do Fish (`dossie-cta-hq.json`), `CTA.mp3` e `palavras.json` (Whisper) | só os .json |

Roteiro visual (tempos reais da fala): 0–3,9 s leque das capas #1/#2/#3 (CLASIFICADO com carimbo em "otros" e "llegaron"); 3,9 s zoom na #1; 4,4 s a capa abre (folha em 16 tiras 3D com curvatura, luz e sombra); 6,3 s vira a pág. 1 (aparece a pág. 2); 7,25 s parede com o pôster; 10 s celular com o wallpaper; 11 s carimbo DE REGALO; 11,6 s banner "ENLACE EN LA DESCRIPCIÓN · COMENTARIO FIJADO" com setas.

## Trocar uma capa quando sair o #2 (a narração fica)
1. Gere a capa real do #2 (mesmo layout) com o código da HQ: em `../produtos/hq/src/hq.py`, troque em `CAPAS_FUTURAS` o item `2` pela arte do #2 (ou escreva a capa do #2 como a `capa()` do #1) e rode `tools/.venv/bin/python canais/dossie-es/produtos/hq/src/hq.py --capa` (grava `capa.png/.jpg`, `capa-2/3.png/.jpg` e `hotmart/`).
2. Em `src/CTA.jsx`, a capa que **já existe** perde o carimbo: no `Leque`, a capa #2 não deve mais chamar `<Carimbo … CLASIFICADO>` (deixe só na #3) e tire o `filter` escurecido dela. Se quiser a #2 no centro, troque `capa-1.jpg` ↔ `capa-2.jpg` no `Leque`/`Parede`.
3. `tools/.venv/bin/python canais/dossie-es/cta/tools/build_cta.py` (refaz os links das artes; o áudio não muda) e `canais/dossie-es/cta/tools/render_cta.sh`.
4. Olhe `cta-hq-frames.jpg`. Pronto: o próximo `build.py` de vídeo já pega o mp4 novo.
- Mudar o **texto** = voz nova (Fish, ~US$ 0,004): edite `voz/dossie-cta-hq.json`, rode `tools/tts_fish.py dossie-es voz/dossie-cta-hq.json voz/vX --velocidade 1.25 --pausa-frase 0.25` (sem `--video`; nota = nome do json), copie `CTA.mp3`, refaça `palavras.json` com Whisper e confira que cabe em 15 s (o `build_cta.py` falha se a voz passar de 14,8 s). Texto aprovado pelo Rodrigo: não mude sem pedido dele.

## Encaixe num vídeo (resumo; procedimento na skill `montagem-render`)
- `tools/build.py` do vídeo (016 em diante) importa `encaixe.py`. **Sem `ATIVO`, a montagem é idêntica** (testado no 017: `timeline.json`, `.srt`, `capitulos.json`, `voz.wav` e `mix.wav` byte a byte iguais).
- Com `ATIVO`: o bloco entra antes do capítulo cujo início fica mais perto de 37,5% da duração (nunca antes de 2:00 nem no último minuto), com 0,5 s de silêncio antes e o 1,5 s normal de capítulo depois; voz na faixa de voz (a trilha do vídeo faz ducking), SFX na faixa de efeitos, fusão de 8 quadros na entrada/saída, linhas no `.srt`, capítulos seguintes deslocados (+15,5 s), `qa/cta.json` com a posição e o link. Teste no 017 (ATIVO de teste): CTA em 5:05,9 (36,2%), antes do "Expediente 5"; trecho de 25 s renderizado e conferido (imagem + Whisper).
- Pacote: depois do `tools/pacote.py` do vídeo, `tools/.venv/bin/python canais/dossie-es/cta/pacote_cta.py <pasta do vídeo>`.

## Custo
Voz Fish: 3 versões de teste (1,0×, 1,2×, 1,25×) × 279 bytes = **US$ 0,0126** (`financas.consumo`, nota `dossie-cta-hq.json`, sem `ref_id`). Imagens novas: zero (capas #2/#3 compostas em código com artes dos vídeos 005, 012, 015 e 003).
