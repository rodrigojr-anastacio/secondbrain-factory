# ETAPA 1 PRONTA · historia-ptbr/015-argentina · vídeo id 56 · 23/11/2026

Retomada da etapa 1 (BLOQUEIO de 21/11 removido). Custo pago da etapa: US$ 0.

## Embalagem aprovada (crivo 3/3)
| par | título | thumb (padrão · texto) | rodada |
|---|---|---|---|
| A | A Argentina já foi RICA. Por que apagou 13 zeros da moeda? | `rosto-emocao`: rapaz de 1992 com riso nervoso e maço de cédulas de 1969 com cinta "1.000.000" · "VALE NADA" | r2/r3 |
| B | Argentina: como a CARNE e o TRIGO decidiram quem manda | `conflito-xvy`: produtor do pampa (chapéu de aba curta, Sol de Maio no céu celeste e branco, 1 boi) × tangueiro portenho dos anos 1940 (fedora, risca de giz, cravo; Obelisco ao fundo), do peito para cima, cara a cara, puxando a mesma conta de papel, raio no meio · "QUEM PAGA?" + pílula "1946" | r5 (rodada extra autorizada pelo Rodrigo; r4 reprovou por repetir a 016-B) |
| C | Por que a Argentina trocou de dinheiro 4 vezes em 22 anos? | `numero-estatistica`: "13 ZEROS" gigante + cédula cortada por tesoura, fundo celeste profundo · "13 ZEROS" | r3 |

`embalagem/variantes.json` registrado em `youtube.embalagem_variantes` (23/11). Detalhes e prompts das bases em `EMBALAGEM.md`; pareceres em `embalagem/crivo-r1…r5.md`.

## Promessa e onde é paga
Promessa: como a Argentina, que já esteve entre os mais ricos do mundo, trocou de dinheiro 4 vezes em 22 anos e apagou 13 zeros: 200 anos de briga por quem paga a conta, com o dinheiro do pampa no meio.
- Hook N001–N003 (0:00–~0:30): gaveta do avô em 1/1/1992, maço de 1969 de um milhão (preço de uma tropa vendida no pampa) → frase-âncora "em vinte e dois anos… quatro vezes… treze zeros" (T1, T3, Thumb A).
- N004 (~0:30): "entre os mais ricos do mundo" + pergunta central **"Quem pagou por esses treze zeros?"** (trocada no crivo de ângulo r2; ver nota no `EMBALAGEM.md`).
- N005 (~0:50–1:05): "quem paga a conta… o couro, a carne, o trigo… quem fica com esse dinheiro, manda" (T2).
- Cap. 7 (~9:40–10:30): 1946, IAPI, o campo pagando a cidade, "Quem paga? O campo." (Thumb B).
- Caps. 8–9 (~11:00–14:00): as 4 trocas (1970, 1983, 1985, 1992) com motivo; o 13º zero e a volta da gaveta (T3).
- N059–N060 (~15:40): Res. 125 e o voto de Cobos (o campo decidindo quem manda); Milei em 1 frase neutra.
- Fecho N061–N064 (~16:25): resposta ("quando ninguém aceita pagar, a conta vai para quem não pode recusar: quem tem o peso no bolso") + a gaveta.
Tempos estimados a 130 ppm: conferir na `legendas.srt` (frase-âncora ≤ 0:30, pergunta ≤ 0:50, "quem paga a conta" ≤ 1:05).

## Ângulo e crivos do roteiro
- Ângulo: **os 13 zeros como a conta que ninguém quis pagar** (porto × províncias → campo × cidade → Estado × credores; quando ninguém paga, paga quem tem o peso no bolso).
- Detector de cópia (`SIMILARIDADE.md`): **1/100** (ok; cópia ≥ 30).
- Crivo de ângulo: **APROVADO na r3** (r1: fonte da abertura do cap. 9 e ponte da manada; r2: pergunta central parecida com hfMz/HX4L). `CRIVO-ANGULO.md`.
- Checklist v2: APROVADO. 64 blocos, ~2.255 palavras, ~17–17:30 min (no teto da bíblia).

## Storyboard
338 planos (média 3,2 s), 204 imagens únicas (teto da bíblia ~190–205), reuso 39,6% (0% antes de 3:00). `cenas.json`, `STORYBOARD.md`, `storyboard.json`. Riscos de época listados no `ETAPA1.md`.

## O que a etapa 2 precisa saber
- **3 thumbs, uma por conceito** (A/B/C = T1/T2/T3), nunca variações; texto e "1.000.000" só no código; bases sem letras.
- Thumb B (ressalvas do crivo r5): Obelisco inteiro, ≥ ~35% da altura e sem ficar atrás da cabeça do tangueiro; Sol de Maio ≥ ~8% da largura; conta ≥ ~25% da largura; comparar lado a lado com `videos/016-espanha/entrega/thumb-B.jpg` antes de entregar.
- Thumb A: a cinta "1.000.000" com ≥ ~25% da largura para ler a 320 px.
- Imagens: lote-prova de ~6 antes do resto; cédulas costumam sair com números/retratos inventados → pedir "completely blank".
- Pronúncias a testar antes da voz inteira (Rosas, Urquiza, Bordabehere, Cobos, Milei etc., lista `FALA` no `roteiro.py`).
- Se a voz passar de 17:30: cortes já listados no `ETAPA1.md` (N036, parte do N025, trecho do N033), sem tocar nos blocos das obrigações.
- Cartões de data de 5 blocos (1810, 1930, 1952, 1982, 2026) aparecem antes de o ano ser dito: ajustar pelo tempo real da legenda no `build.py`.

## Pendências
- Nenhuma que trave. A YouTube Data API do projeto está fora do ar (403 "Project has been deleted", 23/11): conferências de views foram feitas por yt-dlp via WARP; avisar o Rodrigo (afeta métricas/rotinas).
