# BLOQUEIO: CTA v2 não cabe em 15 s com ≤ 1,35× (24/11/2026)

Texto v2 (aprovado, sem mudar palavra) gerado no Fish (s2.1-pro, mesma voz da v1, `--por-frase`, 3 frases):

| velocidade | pausa entre frases | duração da voz |
|---|---|---|
| 1,25× | 0,20 s | 15,95 s |
| 1,35× (máximo do brief) | 0,15 s | **14,94 s** |

- As 3 frases em 1,35× somam ~14,64 s de fala já sem pausa (o Fish corta o silêncio das pontas). Mesmo com pausa 0, a voz + 0,25 s de entrada (`VOZ_OFF`) dá ~14,89 s, acima do limite de 14,8 s do `build_cta.py`, e ficaria sem respiro entre frases (atropelado).
- Não renderizei nada; `cta.json`, `tempos.json`, `CTA.jsx` e o mp4 seguem na v1 (o encaixe continua igual, sem `ATIVO`).
- Custo gasto: US$ 0,0065 (Fish, `financas.consumo`, sem `ref_id`). Teto US$ 0,20.
- `voz/dossie-cta-hq.json` já tem o texto v2; amostras em `voz/v2a` (1,25×) e `voz/v2b` (1,35×), só local.

## Opções para o Rodrigo
1. Cortar uma frase curta do texto (ex.: "Historias reales de espionaje y," ou "en el comentario fijado"), que dá ~1 s.
2. Aceitar bloco de ~16,5 s (muda `DUR` em `build_cta.py`; o encaixe lê a duração do `cta.json`).
3. Pedir ≥ 1,4× (risco de ficar atropelado; fora do brief).
