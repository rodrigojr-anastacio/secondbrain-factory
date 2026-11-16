# Voz (em-relevo)

## Motor e voz (em uso do 001 v2 ao 005)
- **ElevenLabs, voz "Fernanda" `7iqXtOF3wl3pomwXFY7G`, modelo `eleven_v3`**, `voice_settings` `{"stability": 0.0, "similarity_boost": 0.8}`, `output_format=mp3_44100_128`, **um request por bloco** com o texto de `fala_tts`. Fonte: `../videos/005-enchente-porto-alegre-2024/shared/gera_voz_eleven.py` (idêntico no 001 v2, 002, 003 e 004); escolha do Rodrigo em 08/11/2026 (`~/workspace/referencias/BRIEF-clima-longo-01-v2.md`; modelo aprovado: `pesquisa/canal-clima-2026-11/voz-eleven/hook-v3-1.2.mp3`).
- Chave em `~/.segredos/elevenlabs/api_key` (header `xi-api-key`; lida pelo script, nunca impressa, nunca em arquivo/log; começa com `sk_`, então `git grep` antes do push).
- **Custo:** assinatura (`financas.lancamentos` id 51), lançada em `financas.consumo` com custo 0 e `--video <id>`. Plano de **38.634 caracteres/mês, reset dia 08** (`../videos/004-el-nino-1983/ETAPA1-PRONTA.md`). O v3 conta menos que o texto enviado: 003 = 3.163 do plano para ~10 mil caracteres; 004 = 3.480 (`ETAPA2-PRONTA.md` de cada). O script imprime o contador antes e depois (`/v1/user/subscription`). **Confira o saldo antes de gerar**; se não couber, avise (o 005 previa Fish como saída, mas o canal **não tem voz Fish escolhida**).
- Brutos em `audio/eleven-brutos/<bloco>.mp3` (fora do git) com `log.json` dos textos enviados; `gera_voz_eleven.py b05 b12` refaz só esses blocos.

### Como se chegou aqui (não repetir os testes)
| Data | Voz | Resultado | Fonte |
|---|---|---|---|
| até 08/11 | Kokoro `pf_dora` (local, grátis), 2 marchas (183 → 165 pal/min) | piloto e 001 v1; Rodrigo: "robótica em alguns momentos", sem entonação nas perguntas (6/10 com "?") | `../videos/001-tornados-sul/RELATORIO.md`, `QA.md`; `BRIEF-clima-voz-5-femininas.md` |
| 08/11 | Fish `1d8cb595…` (s2.1-pro e drama-3) e 5 femininas pt-BR em drama-3 | Rodrigo achou as Fish **lentas**; prefere ritmo dinâmico | `pesquisa/canal-clima-2026-11/voz-fish/LEIA.md`, `voz-fish/femininas/` |
| 08/11 | ElevenLabs `eleven_multilingual_v2` × `eleven_v3` | aprovado v3 com tags (`hook-v3-1.2.mp3`) | `pesquisa/canal-clima-2026-11/voz-eleven/` |
| 08/11 → 16/11 | Fernanda `eleven_v3` | 10/10 perguntas com "?" no 001 v2; usada em todos os longos desde então | `../videos/001-tornados-sul/QA-v2.md` |
Kokoro `pf_dora` só como provisória (`VOZ=kokoro` no `monta_audio_v2.py`, sem atempo).

## Tags e texto
- Tags de emoção do v3 em `fala_tts` (a `fala` fica limpa para legenda e Whisper): `[serious]` no início dos fatos, `[curious]`/`[intrigued]` antes das perguntas. Uso real: 003 = 13/9/2, 004 = 17/7/3, 005 = 8/3/1 (serious/curious/intrigued; `shared/blocos.json`).
- Menos `[serious]` no hook: pausas dramáticas comem o ritmo (001 v2: hook a 144 pal/min) (`../videos/001-tornados-sul/RELATORIO.md`). **Hipótese.**
- Números por extenso quando ajudar ("cento e sessenta mil", "quarenta mil cento e noventa e nove"); siglas com a leitura desejada; lista de pronúncia no `ETAPA1-PRONTA.md` (ex. 005: Guaíba "Gua-í-ba", DMAE "dê-ême-a-é", UFRGS "ufergis", CEP "cep").
- Sem gancho de próximo vídeo no fecho (regra de 13/11/2026; `../videos/003-seca-1877/ETAPA2-PRONTA.md`).

## Ritmo (o v3 não tem parâmetro de velocidade: `atempo` no ffmpeg)
- **Hook b01–b06 1,36×, resto 1,1×** (`../videos/005.../shared/monta_audio_v2.py`, mesmo valor no 003–005). Nesta fase a Fernanda veio mais rápida que no 001: com 1,4/1,2 dava 178/190 pal/min. Alvo ~173 pal/min no corpo.
- Medido (`work/confere_voz_eleven.txt`): 003 hook 198 / corpo 170 pal/min; 004 189 / 173; 005 202 / 172. Duração final 9:48–10:45.
- Histórico: 001 v2 com 1,3/1,2 deu hook 144 × corpo 173 (hook lento demais, pendência do QA-v2); 002 corrigiu para 174/174.
- Ajuste de atempo não gasta crédito, mas muda os tempos: decidir **antes** do render (`conhecimento/erros-qa.md`, 08/11/2026).
- Pausa entre blocos e encaixe em janela fixa (`EXTRA`, `slot`) ficam no `monta_audio_v2.py`.

## Conferência com Whisper (obrigatória antes de montar)
1. `monta_audio_v2.py` transcreve **cada bloco** (faster-whisper small, pt) e grava `work/confere_voz_eleven.txt`: razão Whisper × roteiro por bloco, **tags faladas**, nº de perguntas e de "?" no Whisper, pal/min por trecho, lista de blocos < 0,95.
2. Compare com números normalizados (`shared/normaliza_pt.py`: "250 km" = "duzentos e cinquenta quilômetros"), senão a nota cai sem erro de fala.
3. Bloco < 0,95 ou com tag falada: ouça/leia o diff; se for erro de fala, refaça **só o bloco** (~200 caracteres). Grafia do Whisper não é erro: "NOA" (NOAA), "Uninho"/"elninho" (El Niño), "Chanchere" (Xanxerê), "Inmete", "Dnócs", "Iguaçu" (001 v2, 002, 003, 004).
4. `shared/alinha.py` → `whisper.json` (tempo por palavra para `build_cues.py`); no fim, `tools/whisper_final.py out/video.mp4` → `qa/transcricao.json` + `qa/voz_diff.txt`. Meta ≥ 0,95 ponderado (003: 0,969/0,973; 004: 0,963/0,965; 005: 0,967).
5. Antes de pedir ao Rodrigo para ouvir um trecho, confira o tempo na `legendas.srt`.

## O que já deu errado
| Problema | Correção | Origem |
|---|---|---|
| v3 troca ou inventa palavra em ~1 de cada 8 blocos ("Santa Augusto", "arrasou", "o Araciaba", "Exposure" no começo; "faz portas", "recebemos") | Whisper por bloco + retake do bloco (7 retakes no 001 v2, 8 no 002) | `../videos/001-tornados-sul/QA-v2.md`; `../videos/002-el-nino-2026/QA.md` |
| Pergunta sem entonação de pergunta (001 v2 b06, b36; 002 b37 e b42 "E depois?" sem "?" em 3 takes) | `[curious]` antes; retake; pergunta curta demais o Whisper não marca: ouvir | 001 `QA-v2.md`; 002 `QA.md` |
| Hook lento (144 pal/min) com muitas perguntas e tags | atempo maior no hook ou menos tags | 001 `QA-v2.md` |
| Kokoro: `speed` muda pouco o ritmo percebido; loudnorm de uma passada não chega a −14 LUFS | (histórico) pausa medida entre frases; compressor + limitador antes do loudnorm | 001 `RELATORIO.md` |
| Fish: com header de modelo errado cai calado em s2.1-pro; tags `female` pouco confiáveis | conferir o modelo cobrado (se um dia voltar ao Fish) | `voz-fish/LEIA.md`; `CLAUDE.md` do workspace |

## Transparência
`youtube.txt` sem menção a IA/voz sintética (padrão de `conhecimento/politicas-youtube.md`, 14/11/2026); a descrição do canal declara "Narração com voz sintética" (`identidade/LEIA.md`). Marcar conteúdo alterado/sintético no upload quando aplicável (decisão do Rodrigo no upload).

## Voz de reserva (amostras Fish, 16/11/2026)
Se o plano da ElevenLabs acabar, há amostras prontas em `../amostras-voz-reserva/` (`todas.mp3` + `LEIA.md`): Fernanda (referência) × 4 femininas e 1 masculina no Fish (drama-3) e a melhor também em s2.1-pro, no trecho hook + transição do 005, com o ritmo casado ao da Fernanda. **Aguardando o ouvido do Rodrigo; nenhuma foi escolhida.** Pelas medidas, a #NATASHA (`e8bccb7beecd46c6a1c64813e0238fa9`, drama-3) é a mais rápida de natural (163–176 pal/min) e marcou as perguntas. No s2.1-pro, a mesma voz soltou um ruído entre blocos: fique no drama-3. O drama-3 ainda foi cobrado a US$ 10/M em 16/11 (crédito conferido). A troca exige tirar as tags do v3 do `fala_tts` (ver o `LEIA.md`).
